const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatResponse {
  reply: string;
}

/**
 * Send the full conversation history to the backend and get the
 * assistant's reply.
 */
export async function sendChat(messages: Message[]): Promise<string> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Chat request failed (${res.status}): ${detail}`);
  }

  const data: ChatResponse = await res.json();
  return data.reply;
}
