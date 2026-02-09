// talks to the backend's /chat endpoint.
// the backend owns the conversation history — we just send the new message
// and a session id, and get back the full chat with tool annotations.

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Message {
  role: "user" | "assistant";
  content: string;
  tools_used: string[];
}

interface ChatResponse {
  session_id: string;
  messages: Message[];
}

// sends a new message to the backend and gets the updated conversation
export async function sendChat(
  sessionId: string | null,
  message: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      message,
    }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`chat request failed (${res.status}): ${detail}`);
  }

  return res.json();
}
