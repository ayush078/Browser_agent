from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from nlu import extract_intent
from browser_automation import BrowserAutomation
from ai_content_generation import generate_email_content

app = Flask(__name__)
CORS(app)

browser_automation = BrowserAutomation()
conversation_context = {}

@app.route("/")
def home():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'test.html')

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response_messages = []

    intent = extract_intent(user_message)

    if intent == "send_email":
        if "email_state" not in conversation_context:
            conversation_context["email_state"] = {"step": "ask_email"}
            response_messages.append({"type": "text", "content": "I\"ll help you send that email. To access your email, I\"ll need your Gmail credentials. What\"s your email address?"})
        elif conversation_context["email_state"]["step"] == "ask_email":
            conversation_context["email_state"]["email"] = user_message
            conversation_context["email_state"]["step"] = "ask_password"
            response_messages.append({"type": "text", "content": "Thanks! And what\"s the password for this account? (Please use only a test account for this assignment)"})
        elif conversation_context["email_state"]["step"] == "ask_password":
            conversation_context["email_state"]["password"] = user_message
            conversation_context["email_state"]["step"] = "ask_leave_dates"
            response_messages.append({"type": "text", "content": "Great! Now, when will you be taking leave?"})
        elif conversation_context["email_state"]["step"] == "ask_leave_dates":
            conversation_context["email_state"]["leave_dates"] = user_message
            conversation_context["email_state"]["step"] = "ask_manager_email"
            response_messages.append({"type": "text", "content": "And what\"s your manager\"s email address?"})
        elif conversation_context["email_state"]["step"] == "ask_manager_email":
            conversation_context["email_state"]["manager_email"] = user_message
            conversation_context["email_state"]["step"] = "ready_to_send"
            response_messages.append({"type": "text", "content": "Perfect! I\"ll now open Gmail and send a professional leave application. Let me show you what I\"m doing..."})

            # Browser automation steps
            screenshot = browser_automation.launch_browser()
            response_messages.append({"type": "screenshot", "content": screenshot})
            response_messages.append({"type": "text", "content": "I\"m at the Gmail login page. Entering your credentials..."})

            screenshot = browser_automation.navigate("https://mail.google.com/")
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.type_text("input[type=\"email\"]", conversation_context["email_state"]["email"])
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.click_element("div[id=\"identifierNext\"]")
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.type_text("input[type=\"password\"]", conversation_context["email_state"]["password"])
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.click_element("div[id=\"passwordNext\"]")
            response_messages.append({"type": "screenshot", "content": screenshot})
            response_messages.append({"type": "text", "content": "Successfully logged in! Now composing your leave application..."})

            # Wait for inbox to load and click compose
            screenshot = browser_automation.click_element("div[role=\"button\"][gh=\"cm\"]") # Compose button
            response_messages.append({"type": "screenshot", "content": screenshot})

            # AI content generation
            email_prompt = f"""Draft a professional leave application email for {conversation_context["email_state"]["leave_dates"]}. The recipient is {conversation_context["email_state"]["manager_email"]}. The sender is {conversation_context["email_state"]["email"]}."""
            generated_email_body = generate_email_content(email_prompt)
            subject = f"Leave Application - {conversation_context['email_state']['leave_dates']}"

            screenshot = browser_automation.type_text("textarea[name=\"to\"]", conversation_context["email_state"]["manager_email"])
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.type_text("input[name=\"subjectbox\"]", subject)
            response_messages.append({"type": "screenshot", "content": screenshot})

            screenshot = browser_automation.type_text("div[aria-label=\"Message Body\"]", generated_email_body)
            response_messages.append({"type": "screenshot", "content": screenshot})
            response_messages.append({"type": "text", "content": f"I\"ve drafted a professional leave application. Here\"s what I wrote:\nSubject: {subject}\n{generated_email_body}\nSending now..."})

            screenshot = browser_automation.click_element("div[role=\"button\"][aria-label*=\"Send\"]")
            response_messages.append({"type": "screenshot", "content": screenshot})
            response_messages.append({"type": "text", "content": f"✓ Email sent successfully! Your leave application has been sent to {conversation_context['email_state']['manager_email']}."}
)

            browser_automation.close_browser()
            conversation_context.clear() # Clear context after task completion

    else:
        response_messages.append({"type": "text", "content": "I\"m sorry, I can only help with sending emails at the moment. Please tell me if you need to send an email."})
        conversation_context.clear() # Clear context if intent is not send_email

    return jsonify(response_messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


