# Browser Agent - Email Automation Bot

A Python Flask-based browser automation agent that can send emails through Gmail using natural language processing and AI-powered content generation.

## Features

- 🤖 **Natural Language Understanding** - Recognizes email sending intents
- 🌐 **Browser Automation** - Uses Playwright to automate Gmail interactions
- 🤖 **AI Content Generation** - Generates professional emails using Google Gemini AI
- 📧 **Email Automation** - Complete workflow for sending leave applications
- 💬 **Interactive Chat Interface** - Web-based testing interface

## Tech Stack

- **Backend**: Python Flask
- **Browser Automation**: Playwright
- **AI**: Google Generative AI (Gemini)
- **Frontend**: HTML/CSS/JavaScript
- **Environment**: Virtual Environment with pip

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ayush078/Browser_agent.git
cd Browser_agent
```

### 2. Set up Virtual Environment
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 4. Configure Environment Variables
Create a `.env` file in the `backend` directory:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Application
```bash
cd src
python main.py
```

The application will be available at: http://127.0.0.1:5000

## API Endpoints

### POST /api/chat
Send messages to interact with the browser agent.

**Request Body:**
```json
{
  "message": "I want to send an email"
}
```

**Response:**
```json
[
  {
    "type": "text",
    "content": "I'll help you send that email. What's your email address?"
  }
]
```

## Usage Example

1. **Start the conversation:**
   - "I want to send an email"
   - "Send email to my manager"

2. **Follow the prompts:**
   - Enter your Gmail credentials (use test account)
   - Provide leave dates
   - Enter manager's email

3. **Watch the automation:**
   - Browser launches automatically
   - Logs into Gmail
   - Composes professional email using AI
   - Sends the email

## Project Structure

```
browser_agent/
├── backend/
│   ├── src/
│   │   ├── main.py              # Flask application
│   │   ├── nlu.py               # Natural Language Understanding
│   │   ├── browser_automation.py # Playwright automation
│   │   └── ai_content_generation.py # Google Gemini integration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables (not tracked)
│   └── test.html               # Testing interface
└── frontend/                   # React frontend components
```

## Security Notes

- ⚠️ **Use only test Gmail accounts** for this demonstration
- 🔒 **API keys are stored in .env** and not committed to version control
- 🛡️ **Enable 2FA and app passwords** for Gmail authentication

## Requirements

- Python 3.8+
- Google Generative AI API key
- Gmail account (preferably test account)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Author

Created by Ayush Kumar
