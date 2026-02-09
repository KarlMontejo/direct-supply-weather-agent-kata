// the main chat interface. manages the session id and message list.
// the backend owns the conversation state — we send our message,
// get back the full history, and just render whatever it gives us.

"use client";

import { useState, useRef, useEffect } from "react";
import type { Message } from "../services/apiClient";
import { sendChat } from "../services/apiClient";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // scroll to bottom whenever the messages change or loading state flips
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    // optimistically show the user's message right away
    const optimistic: Message = { role: "user", content: text, tools_used: [] };
    setMessages((prev) => [...prev, optimistic]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChat(sessionId, text);

      // the backend gives us the full history — replace our local copy
      setSessionId(res.session_id);
      setMessages(res.messages);
    } catch (err) {
      // if something breaks, show the error as a fake assistant message
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `something went wrong. please try again.\n\n${err}`,
          tools_used: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex h-screen flex-col">
      {/* header */}
      <header className="flex items-center gap-3 border-b border-[#e9ecef] bg-white px-6 py-4">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#0059b3] text-sm font-bold text-white">
          DS
        </div>
        <div>
          <h1 className="text-base font-semibold text-[#212529]">
            Procurement Assistant
          </h1>
          <p className="text-xs text-[#6c757d]">
            Karl&apos;s Senior Living of Dallas
          </p>
        </div>
      </header>

      {/* message area */}
      <main className="flex-1 overflow-y-auto px-6 py-6">
        <div className="mx-auto flex max-w-2xl flex-col gap-4">
          {messages.length === 0 && !loading && (
            <div className="py-24 text-center">
              <p className="text-lg font-medium text-[#343a40]">
                How can I help with procurement today?
              </p>
              <p className="mt-2 text-sm text-[#6c757d]">
                Ask about product availability, order drafts, or compliance
                checks.
              </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="rounded-2xl rounded-bl-md bg-[#f1f3f5] px-4 py-3 text-sm text-[#6c757d]">
                <span className="inline-flex gap-1">
                  <span className="animate-bounce">.</span>
                  <span className="animate-bounce [animation-delay:0.15s]">
                    .
                  </span>
                  <span className="animate-bounce [animation-delay:0.3s]">
                    .
                  </span>
                </span>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </main>

      {/* input bar */}
      <footer className="border-t border-[#e9ecef] bg-white px-6 py-4">
        <div className="mx-auto flex max-w-2xl gap-3">
          <textarea
            className="flex-1 resize-none rounded-xl border border-[#e9ecef] bg-[#f8f9fa] px-4 py-3 text-[15px] text-[#212529] placeholder-[#adb5bd] outline-none transition-colors focus:border-[#0059b3] focus:bg-white"
            rows={1}
            placeholder="Ask about products, orders, or compliance..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="flex h-[46px] w-[46px] shrink-0 items-center justify-center rounded-xl bg-[#0059b3] text-white transition-colors hover:bg-[#004a99] disabled:opacity-40 disabled:cursor-not-allowed"
            aria-label="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="h-5 w-5"
            >
              <path d="M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z" />
            </svg>
          </button>
        </div>
      </footer>
    </div>
  );
}
