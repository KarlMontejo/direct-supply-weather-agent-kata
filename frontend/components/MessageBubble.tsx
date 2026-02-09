import type { Message } from "../services/apiClient";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`
          max-w-[75%] rounded-2xl px-4 py-3 text-[15px] leading-relaxed
          ${
            isUser
              ? "bg-[#0059b3] text-white rounded-br-md"
              : "bg-[#f1f3f5] text-[#212529] rounded-bl-md"
          }
        `}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}
