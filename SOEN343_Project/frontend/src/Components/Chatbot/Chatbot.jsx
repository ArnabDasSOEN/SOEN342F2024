import React, {useState} from 'react'
import './Chatbot.css'
import chat_icon from '../Assets/Chat.png'

export const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    }

    const handleSendMessage = (e)  => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const newMessage = e.target.value.trim();
            if (newMessage) {
                setMessages([...messages, { text: newMessage, user: 'You' }]);
                e.target.value = '';
            }
        }
    }
  return (
    <div className='chatbot'>
        <div className={`chatbot ${isOpen ? 'open' : 'closed'}`}>
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div key={index} className="chat-message">
              <strong>{msg.user}:</strong> {msg.text}
            </div>
          ))}
        </div>
            <textarea
            placeholder="Type your message..."
            onKeyDown={handleSendMessage}
            />
        </div>
        <img src={chat_icon} alt="" onClick={toggleChat}/>
    </div>
  )
}
