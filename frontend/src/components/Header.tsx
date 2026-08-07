// Credits: Erwin Lejeune — 2026-02-23
export default function Header() {
  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-line bg-deep/85 px-6 py-3 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <h1 className="font-mono text-base font-bold tracking-tight text-bright">
          Epstein<span className="text-ember">Explorer</span>
        </h1>
        <span className="stamp">beta</span>
      </div>
      <div className="flex items-center gap-4">
        <span className="hidden font-mono text-[11px] uppercase tracking-[0.12em] text-muted sm:inline">
          Public records · research tool
        </span>
        <a
          href="https://github.com/guilyx/epsteinexplorer"
          target="_blank"
          rel="noopener noreferrer"
          className="font-mono text-xs text-subtle transition-colors duration-150 hover:text-ember"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}
