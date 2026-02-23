// Credits: Erwin Lejeune — 2026-02-23
import { useCallback, useEffect, useRef, useState } from "react";
import MessageBubble, { type Message } from "./MessageBubble";
import SuggestionChips from "./SuggestionChips";

function generateFingerprint(): string {
  const raw = [
    navigator.userAgent,
    screen.width,
    screen.height,
    screen.colorDepth,
    Intl.DateTimeFormat().resolvedOptions().timeZone,
    navigator.language,
  ].join("|");

  let hash = 0;
  for (let i = 0; i < raw.length; i++) {
    hash = (hash << 5) - hash + raw.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash).toString(16).padStart(8, "0");
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fingerprintRef = useRef(generateFingerprint());

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = useCallback(
    async (text: string) => {
      if (!text.trim() || loading) return;

      const userMsg: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content: text.trim(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setInput("");
      setLoading(true);

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: userMsg.content,
            conversation_id: conversationId,
            fingerprint: fingerprintRef.current,
          }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const reader = res.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) throw new Error("No response body");

        let buffer = "";
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed.startsWith("data:")) continue;
            const payload = trimmed.slice(5).trim();
            if (!payload) continue;

            try {
              const event = JSON.parse(payload);
              if (event.type === "message") {
                setMessages((prev) => [
                  ...prev,
                  {
                    id: crypto.randomUUID(),
                    role: "assistant",
                    content: event.content,
                  },
                ]);
              }
              if (event.conversation_id) {
                setConversationId(event.conversation_id);
              }
            } catch {
              /* skip malformed SSE */
            }
          }
        }
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: `Error: ${err instanceof Error ? err.message : "Unknown error"}`,
          },
        ]);
      } finally {
        setLoading(false);
      }
    },
    [loading, conversationId],
  );

  return (
    <div className="flex flex-1 flex-col">
      <div className="flex flex-1 flex-col overflow-y-auto px-4 py-6">
        {messages.length === 0 ? (
          <div className="flex flex-1 items-center justify-center">
            <SuggestionChips onSelect={send} />
          </div>
        ) : (
          <div className="mx-auto flex w-full max-w-3xl flex-col gap-4">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} {...msg} />
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="rounded-2xl border border-border bg-deep px-4 py-3 text-sm text-muted">
                  <span className="inline-flex gap-1">
                    <span className="animate-pulse">●</span>
                    <span className="animate-pulse" style={{ animationDelay: "0.15s" }}>●</span>
                    <span className="animate-pulse" style={{ animationDelay: "0.3s" }}>●</span>
                  </span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Input bar */}
      <div className="border-t border-border/50 bg-deep/60 px-4 py-3 backdrop-blur-sm">
        <form
          className="mx-auto flex max-w-3xl gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about the Epstein files..."
            disabled={loading}
            className="flex-1 rounded-xl border border-border bg-panel px-4 py-2.5 text-sm text-text placeholder-muted outline-none transition focus:border-cyan/50 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="rounded-xl bg-cyan px-5 py-2.5 text-sm font-medium text-ink transition hover:bg-cyan/80 disabled:opacity-40"
          >
            Send
          </button>
        </form>
        <p className="mx-auto mt-2 max-w-3xl text-center text-[11px] text-muted">
          Data sourced from publicly released government records via{" "}
          <a href="https://epsteinexposed.com" className="text-subtle hover:text-cyan" target="_blank" rel="noopener noreferrer">
            epsteinexposed.com
          </a>
          . Inclusion does not imply guilt.
        </p>
      </div>
    </div>
  );
}
