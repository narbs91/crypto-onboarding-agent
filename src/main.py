import os
import asyncio
from eth_account import Account
from web3 import Web3
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from bitcoinlib.wallets import Wallet, wallet_delete_if_exists
from bitcoinlib.mnemonic import Mnemonic

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Initialize Rich console for better formatting
console = Console()

ethWalletInfo = {}
btcWalletInfo = {}

@function_tool
def create_btc_wallet() -> dict:
    """Create a new Bitcoin wallet and return its details."""
    try:
        # Generate a new mnemonic (seed phrase)
        words = Mnemonic().generate()
        
        # Delete wallet if it exists (for demo purposes)
        wallet_delete_if_exists('btc_wallet')
        
        # Create a new wallet
        wallet = Wallet.create('btc_wallet', keys=words)
        key = wallet.get_key()
        address = key.address
        
        # Store wallet info
        btcWalletInfo.update({
            "address": address,
            "mnemonic": words,
            "network": "btc"
        })
        
        return {
            "address": address,
            "mnemonic": words,
            "network": "btc"
        }
    except Exception as e:
        console.print(f"[red]Error creating Bitcoin wallet: {str(e)}[/red]")
        return {"error": f"Failed to create Bitcoin wallet: {str(e)}"}

@function_tool
def get_btc_wallet_address() -> str:
    """Get the Bitcoin wallet address."""
    return btcWalletInfo.get("address", "No Bitcoin wallet created yet")

@function_tool
def get_btc_wallet_mnemonic() -> str:
    """Get the Bitcoin wallet mnemonic phrase."""
    return btcWalletInfo.get("mnemonic", "No Bitcoin wallet created yet")

@function_tool
def get_btc_wallet_balance() -> str:
    """Get the balance of the Bitcoin wallet."""
    try:
        if "address" not in btcWalletInfo:
            return "No Bitcoin wallet created yet"
            
        wallet = btcWalletInfo["wallet"]
        wallet.scan()  # Scan for transactions and update balance
        balance_btc = wallet.balance() / 100000000  # Convert satoshis to BTC
        return f"{balance_btc:.8f} BTC"
    except Exception as e:
        console.print(f"[red]Error getting Bitcoin wallet balance: {str(e)}[/red]")
        return f"Error retrieving balance: {str(e)}"

@function_tool
def create_eth_wallet() -> dict:
    acct = Account.create()
    ethWalletInfo["address"] = acct.address
    ethWalletInfo["private_key"] = acct.key.hex()
    return ethWalletInfo

@function_tool
def get_eth_wallet_address() -> str:
    return ethWalletInfo.get("address", "No Ethereum wallet created yet")

@function_tool
def get_eth_wallet_private_key() -> str:
    return ethWalletInfo.get("private_key", "No Ethereum wallet created yet")

@function_tool
def get_eth_wallet_balance() -> str:
    return ethWalletInfo.get("balance", "No Ethereum wallet created yet")

@function_tool
def get_eth_price() -> str:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("ethereum", {}).get("usd", "Price not found")

@function_tool
def get_btc_price() -> str:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("bitcoin", {}).get("usd", "Price not found")

def print_welcome_message():
    console.print("""
[bold blue]Welcome to the Crypto Assistant![/bold blue]
I can help you with:
• Creating Ethereum and Bitcoin wallets
• Checking wallet balances
• Getting crypto prices
• Explaining crypto concepts

Type 'exit' or 'quit' to end the conversation.
Type 'clear' to clear all wallet info.
    """)

async def chat_loop():
    # Set up the configuration
    set_default_openai_api("chat_completions")
    
    # Initialize the OpenAI client
    custom_client = AsyncOpenAI(
        base_url=os.getenv("OPENAI_API_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    set_default_openai_client(custom_client)
    
    # Create the agent
    crypto_agent = Agent(
        name="Crypto Assistant",
        instructions="""You are a helpful crypto assistant that helps users create wallets, get balances, check prices, and explain concepts in a simple way.

        For technical operations:
        1. Ethereum Operations:
           - Use create_eth_wallet to create a new Ethereum wallet
           - Use get_eth_wallet_address to get the Ethereum address
           - Use get_eth_wallet_private_key to get the Ethereum private key
           - Use get_eth_wallet_balance to get the Ethereum balance

        2. Bitcoin Operations:
           - Use create_btc_wallet to create a new Bitcoin wallet
           - Use get_btc_wallet_address to get the Bitcoin address
           - Use get_btc_wallet_mnemonic to get the Bitcoin seed phrase
           - Use get_btc_wallet_balance to get the Bitcoin balance

        3. Price Checking:
           - Use get_eth_price to get ETH price
           - Use get_btc_price to get BTC price
        
        Important notes:
        - Always warn users to keep their private keys and mnemonics secure
        - Do not tell the user what tools and functions you are using
        - When explaining concepts, be educational but approachable
        
        Style guidelines:
        - Maintain a friendly, conversational tone
        - Use markdown formatting for better readability
        - Do not tell the user what functions you are using
        - Provide the answer in a simple and easy to understand way
        - Break up long explanations into sections
        - Include relevant examples when helpful
        - Be encouraging and supportive of learning""",
        model=os.getenv("MODEL"),
        tools=[
            create_eth_wallet, get_eth_wallet_address, get_eth_wallet_private_key, get_eth_wallet_balance,
            create_btc_wallet, get_btc_wallet_address, get_btc_wallet_mnemonic, get_btc_wallet_balance,
            get_eth_price, get_btc_price
        ]
    )

    print_welcome_message()

    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]")
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold blue]Goodbye! Have a great day![/bold blue]")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                ethWalletInfo.clear()
                btcWalletInfo.clear()
                wallet_delete_if_exists('btc_wallet')
                console.print("[bold yellow]All wallet information cleared![/bold yellow]")
                continue

            # Show typing indicator
            with console.status("[bold blue]Thinking...[/bold blue]"):
                # Get response from agent
                result = await Runner.run(crypto_agent, user_input)
            
            # Print the response with markdown formatting
            console.print("\n[bold blue]Assistant[/bold blue]")
            console.print(Markdown(result.final_output))

        except KeyboardInterrupt:
            console.print("\n[bold blue]Goodbye! Have a great day![/bold blue]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred: {str(e)}[/bold red]")

async def main():
    await chat_loop()

if __name__ == "__main__":
    asyncio.run(main()) 