import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = { type: 'text', content: input, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');

    try {
      const response = await fetch('https://5000-io3p0pmyffwr5rdt2vnca-cc6d2f2e.manusvm.computer/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages, ...data.map(msg => ({...msg, sender: 'agent'}))]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [...prevMessages, { type: 'text', content: 'Error: Could not connect to the agent.', sender: 'agent' }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Conversational Browser Agent</h1>
      </header>
      <div className="chat-window">
        <div className="messages-display">
          {messages.map((msg, index) => (
            <div key={index} className={`message-bubble ${msg.sender}`}>
              {msg.type === 'text' ? (
                <p>{msg.content}</p>
              ) : (
                <img src={`data:image/png;base64,${msg.content}`} alt="Screenshot" className="screenshot" />
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="message-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;


