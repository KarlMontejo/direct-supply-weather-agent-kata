// renders a single chat message — user messages on the right in blue,
// assistant messages on the left in gray. if the agent used any tools
// to produce the response, we show them as a small italic label at
// the bottom of the bubble so the user knows what happened behind the scenes.

import type { Message } from "../services/apiClient";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const hasTools = !isUser && message.tools_used.length > 0;

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

        {hasTools && (
          <p className="mt-2 border-t border-[#d4d4d4] pt-2 text-xs italic text-[#868e96]">
            {message.tools_used.join(", ")}
          </p>
        )}
      </div>
    </div>
  );
}
