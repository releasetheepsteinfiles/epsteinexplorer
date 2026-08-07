// Credits: Erwin Lejeune — 2026-02-23

const SUGGESTIONS = [
  "Who flew on Epstein's planes the most?",
  "Search for documents about Little St. James",
  "Tell me about Ghislaine Maxwell's role",
  "What are the flight logs for 2002?",
  "Find court filings mentioning Bill Clinton",
  "Who is in Epstein's black book?",
];

interface Props {
  onSelect: (prompt: string) => void;
}

export default function SuggestionChips({ onSelect }: Props) {
  return (
    <div className="flex flex-col items-center gap-7 px-4">
      <div className="text-center">
        <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.14em] text-muted">
          Natural language research interface
        </p>
        <h2 className="mb-3 font-mono text-2xl font-bold tracking-tight text-bright">
          Explore the Epstein Files
        </h2>
        <div className="mx-auto mb-3 h-px w-16 bg-ember-dim" />
        <p className="max-w-md text-sm text-subtle">
          Ask anything about persons, documents, flights, and emails from the
          case files.
        </p>
      </div>
      <div className="flex max-w-2xl flex-wrap justify-center gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => onSelect(s)}
            className="rounded-md border border-line bg-panel px-3.5 py-2 text-left text-sm text-subtle transition-colors duration-150 hover:border-ember-dim hover:text-ember"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
