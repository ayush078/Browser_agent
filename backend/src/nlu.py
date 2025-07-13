
import re

def extract_intent(message):
    if re.search(r'send.*email|email.*send', message, re.IGNORECASE):
        return 'send_email'
    return None


