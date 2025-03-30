# OpenAI Agents Demo

This project demonstrates the usage of OpenAI's Agents SDK for building AI-powered applications.

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
4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_URL=your_url_here
   OPENAI_API_KEY=your_api_key_here
   MODEL=your_model_here
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