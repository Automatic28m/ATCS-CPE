"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Image from "next/image";

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "👋 Hello! I am Phanlop Boonluea. I'm excited to share my portfolio and experience with you. Feel free to ask me anything!" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    if (input.trim() === "/clear") {
      setMessages([{ role: "assistant", content: "👋 Hello! I am Phanlop Boonluea. I'm excited to share my portfolio and experience with you. Feel free to ask me anything!" }]);
      setInput("");
      try {
        await fetch("http://localhost:8000/reset", { method: "POST" });
      } catch (e) {
        console.error("Failed to reset backend memory", e);
      }
      return;
    }

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      const data = await res.json();
      
      if (res.ok && !data.error) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.answer },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `Error: ${data.error || "Failed to fetch response"}` },
        ]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: Unable to connect to the backend. Is the backend running on port 8000?" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[var(--color-brand-light)] font-sans">
      <header className="bg-[var(--color-brand-darkred)] shadow-md p-4 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="relative w-10 h-10 rounded-full overflow-hidden border-2 border-[var(--color-brand-beige)]">
            <Image src="/avatar.png" alt="Phanlop Avatar" fill className="object-cover" />
          </div>
          <h1 className="text-xl font-bold text-[var(--color-brand-light)]">
            Phanlop Boonluea
          </h1>
        </div>
        <button 
          onClick={async () => {
            setMessages([{ role: "assistant", content: "👋 Hello! I am Phanlop Boonluea. I'm excited to share my portfolio and experience with you. Feel free to ask me anything!" }]);
            try { await fetch("http://localhost:8000/reset", { method: "POST" }); } catch (e) {}
          }}
          className="text-[var(--color-brand-light)] hover:text-[var(--color-brand-beige)] text-sm px-3 py-1.5 rounded-full border border-transparent hover:border-[var(--color-brand-beige)] transition-colors"
          title="Clear Conversation"
        >
          Clear Chat
        </button>
      </header>

      <main className="flex-1 overflow-y-auto p-4 w-full">
        <div className="max-w-3xl mx-auto flex flex-col gap-5 pb-4 mt-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex w-full ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {msg.role === "assistant" && (
                <div className="relative w-12 h-16 shrink-0 mr-2 mt-0">
                  <Image src="/avatar.png" alt="AI Avatar" fill className="object-contain object-top drop-shadow-sm" />
                </div>
              )}
              
              <div
                className={`max-w-[80%] rounded-2xl px-5 py-4 shadow-sm ${
                  msg.role === "user"
                    ? "bg-[var(--color-brand-rose)] text-[var(--color-brand-light)] rounded-br-sm"
                    : "bg-[var(--color-brand-beige)] text-[var(--color-brand-darkred)] rounded-bl-sm prose prose-sm max-w-none prose-p:leading-relaxed prose-a:text-[var(--color-brand-darkred)] prose-a:underline prose-strong:text-[var(--color-brand-darkred)] prose-ul:text-[var(--color-brand-darkred)] prose-ol:text-[var(--color-brand-darkred)]"
                }`}
              >
                {msg.role === "user" ? (
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                ) : (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start w-full">
              <div className="relative w-12 h-16 shrink-0 mr-2 mt-0">
                <Image src="/avatar.png" alt="AI Avatar" fill className="object-contain object-top drop-shadow-sm" />
              </div>
              <div className="rounded-2xl px-5 py-4 bg-[var(--color-brand-beige)] rounded-bl-sm shadow-sm flex space-x-2 items-center h-12">
                <div className="w-2 h-2 bg-[var(--color-brand-darkred)] rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-[var(--color-brand-darkred)] rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-[var(--color-brand-darkred)] rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      <footer className="bg-white border-t border-[var(--color-brand-beige)] p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <form
          onSubmit={sendMessage}
          className="max-w-3xl mx-auto flex gap-3 items-center relative"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything..."
            className="flex-1 p-3 pl-5 pr-14 border border-[var(--color-brand-beige)] rounded-full bg-[var(--color-brand-light)] text-[var(--color-brand-darkred)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-rose)] transition-all placeholder:text-[var(--color-brand-darkred)]/50"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 bg-[var(--color-brand-darkred)] hover:bg-[var(--color-brand-rose)] text-[var(--color-brand-light)] rounded-full p-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-sm"
            aria-label="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-5 h-5 -ml-0.5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
              />
            </svg>
          </button>
        </form>
      </footer>
    </div>
  );
}
