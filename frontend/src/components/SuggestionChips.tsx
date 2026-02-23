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
    <div className="flex flex-col items-center gap-6 px-4">
      <div className="text-center">
        <h2 className="mb-2 text-2xl font-bold tracking-tight text-white">
          Explore the Epstein Files
        </h2>
        <p className="text-sm text-subtle">
          Ask anything about persons, documents, flights, and emails from the case files.
        </p>
      </div>
      <div className="flex max-w-2xl flex-wrap justify-center gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => onSelect(s)}
            className="rounded-full border border-border bg-panel px-4 py-2 text-sm text-subtle transition hover:border-cyan/40 hover:text-cyan"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
