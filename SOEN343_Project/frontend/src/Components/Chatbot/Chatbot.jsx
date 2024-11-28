import React, { useState } from "react";
import "./Chatbot.css";
import chat_icon from "../Assets/Chat.png";
import axios from "axios";

export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false); // Track message sending state
  const [context, setContext] = useState({}); // Maintain the context dynamically

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const newMessage = e.target.value.trim();

      // Retrieve user ID from localStorage
      const userId = localStorage.getItem("user_id");

      if (!userId) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            text: "Error: User ID is not set. Please log in again.",
            user: "Bot",
          },
        ]);
        return;
      }

      if (newMessage) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: newMessage, user: "You" },
        ]);
        e.target.value = "";

        try {
          setIsSending(true);

          // Build payload with current context
          const payload = {
            message: newMessage,
            context: {
              ...context,
              user_id: userId,
            },
          };

          console.log("Payload being sent to backend:", payload);

          // Send request to backend
          const response = await axios.post(
            "http://localhost:5000/chatbot/ask",
            payload
          );

          if (response.data.reply) {
            setMessages((prevMessages) => [
              ...prevMessages,
              { text: response.data.reply, user: "Bot" },
            ]);

            // Update context based on backend response if necessary
            const pendingCommand = response.data.pending_command;
            if (pendingCommand) {
              // Store pending command context if backend indicates it's needed
              setContext((prevContext) => ({
                ...prevContext,
                pending_command: pendingCommand,
              }));
            } else {
              // Clear pending command when fulfilled
              setContext((prevContext) => ({
                ...prevContext,
                pending_command: null,
              }));
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
