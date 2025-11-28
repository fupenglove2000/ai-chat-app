# AI Chat Application

A Streamlit-based chat application powered by OpenAI GPT with multiple conversation modes.

## Features

- Streamlit-based chat interface
- OpenAI GPT integration with streaming responses
- Multiple chat modes (Assistant, Coder, Writer, Translator)
- Token counting with tiktoken
- Session state management
- Real-time response streaming

## Tech Stack

- **Frontend**: Streamlit
- **AI**: OpenAI GPT API
- **Token Counting**: tiktoken

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API Key

### Installation

1. Clone the repository
```bash
git clone https://github.com/fupenglove2000/ai-chat-app.git
cd ai-chat-app
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. Run the application
```bash
streamlit run app.py
```

## Chat Modes

- **Assistant**: General-purpose helpful AI assistant
- **Coder**: Expert programmer for coding tasks
- **Writer**: Creative writing assistant
- **Translator**: Professional translation assistant

## Configuration

Edit `.env` file to customize:
- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_NAME`: GPT model to use (default: gpt-3.5-turbo)
- `MAX_TOKENS`: Maximum tokens per response
- `TEMPERATURE`: Response creativity (0-1)
