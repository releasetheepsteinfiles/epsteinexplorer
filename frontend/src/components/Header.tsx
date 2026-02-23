// Credits: Erwin Lejeune — 2026-02-23
export default function Header() {
  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-border/50 bg-deep/80 px-6 py-3 backdrop-blur-md">
      <div className="flex items-center gap-2">
        <h1 className="text-lg font-bold tracking-tight text-white">
          Epstein<span className="text-cyan">Explorer</span>
        </h1>
        <span className="rounded-full bg-cyan/10 px-2 py-0.5 text-[10px] font-medium text-cyan">
          beta
        </span>
      </div>
      <a
        href="https://github.com/guilyx/epsteinexplorer"
        target="_blank"
        rel="noopener noreferrer"
        className="text-xs text-muted transition hover:text-cyan"
      >
        GitHub
      </a>
    </header>
  );
}
