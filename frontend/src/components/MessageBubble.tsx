// Credits: Erwin Lejeune — 2026-02-23
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function MessageBubble({ role, content }: Message) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-panel text-text"
            : "border border-border bg-deep text-text"
        }`}
      >
        {isUser ? (
          <p>{content}</p>
        ) : (
          <div className="msg-prose">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
