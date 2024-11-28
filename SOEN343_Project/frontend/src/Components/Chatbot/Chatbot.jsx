import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Chatbot.css";
import chat_icon from "../Assets/Chat.png";
import axios from "axios";

export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const navigate = useNavigate();

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const newMessage = e.target.value.trim();

      const userId = parseInt(localStorage.getItem("user_id"), 10);

      if (newMessage) {
        setMessages([...messages, { text: newMessage, user: "You" }]);
        e.target.value = "";

        try {
          setIsSending(true);

          const payload = {
            message: newMessage,
            context: {
              user_id: userId || null,
            },
          };

          const response = await axios.post(
            "http://localhost:5000/chatbot/ask",
            payload
          );

          if (response.data.reply) {
            const botMessage = response.data.reply;

            // Handle navigation commands
            if (botMessage.includes("navigate:update_delivery_request")) {
              setIsOpen(false); // Close chatbot
              navigate("/viewDeliveryRequest");
              window.location.reload(); // Force reload
            } else if (botMessage.includes("navigate:create_delivery")) {
              setIsOpen(false); // Close chatbot
              navigate("/dashboard");
              window.location.reload(); // Force reload
            } else {
              setMessages((prevMessages) => [
                ...prevMessages,
                { text: botMessage, user: "Bot" },
              ]);
            }
          } else {
            setMessages((prevMessages) => [
              ...prevMessages,
              {
                text: "Error: Could not get a response from the server.",
                user: "Bot",
              },
            ]);
          }
        } catch (error) {
          console.error("Error sending message:", error);
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              text: "Error: Failed to communicate with the server.",
              user: "Bot",
            },
          ]);
        } finally {
          setIsSending(false);
        }
      }
    }
  };

  return (
    <div className="chatbot">
      <div className={`chatbot ${isOpen ? "open" : "closed"}`}>
        <div className="chat-header">Wheels Up Chatbot</div>
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.user === "You" ? "user" : "bot"}`}
            >
              <strong>{msg.user}:</strong> {msg.text}
            </div>
          ))}
          {isSending && (
            <div className="chat-message bot">Bot is typing...</div>
          )}
        </div>
        <textarea
          placeholder="Type your message..."
          onKeyDown={handleSendMessage}
        />
      </div>
      <img src={chat_icon} alt="Chat Icon" onClick={toggleChat} />
    </div>
  );
};
