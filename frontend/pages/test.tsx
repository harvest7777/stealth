"use client";
import { useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

export default function WebSocketDemo() {
  const [messages, setMessages] = useState<string[]>([]);

  const { sendMessage, lastMessage, readyState } = useWebSocket(`ws://127.0.0.1:8000/ws
`, {
    onOpen: () => console.log("✅ Connected to WebSocket"),
    onClose: () => console.log("❌ WebSocket closed"),
    onError: (event) => console.error("WebSocket error:", event),
    shouldReconnect: () => true, // Auto reconnect
  });

  // Track incoming messages
  if (lastMessage !== null && !messages.includes(lastMessage.data)) {
    setMessages((prev) => [...prev, lastMessage.data]);
  }
  useEffect(()=>{
    if (lastMessage) {
      console.log("New message:", lastMessage.data);
    } 
  },[lastMessage])

  return (
    <div>
      <h2>Messages</h2>
      <button onClick={() => sendMessage("Hello from React!")}>Send Hello</button>
      <p>Status: {ReadyState[readyState]}</p>
      <ul>
        {messages.map((msg, i) => (
          <li key={i}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}
