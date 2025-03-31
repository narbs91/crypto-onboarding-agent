# Crypto Onboarder AI Agent

This repo represents the foundations for a simple, yet powerful agent who can be used to onboard a non-crypto native person to crypto from creating their first wallet to helping them interact on-chain.

## Features

- 🤖 AI-powered crypto assistant using OpenAI Agents
- 💰 Bitcoin and Ethereum wallet creation and management
- 💱 Real-time cryptocurrency price checking
- 📚 Educational explanations of crypto concepts
- 🔄 AI inference powered by Lilypad's Anura API and Ollama

You can read how I built this by reading the accompanying blog post I wrote

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your custom OpenAPI configuration and a public Ethereum RPC URL:
   ```
   OPENAI_URL=your_url_here
   OPENAI_API_KEY=your_api_key_here
   MODEL=your_model_here

   ETH_RPC_URL=your_rpc_url_here   
   ```

## Running the Application

To run the application:

```bash
python src/main.py
```

## Project Structure

- `src/main.py`: Main application entry point
- `.env`: Environment variables (not tracked in git)
- `requirements.txt`: Project dependencies 