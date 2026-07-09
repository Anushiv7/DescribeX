export default function Footer() {
  return (
    <footer className="w-full py-8 border-t border-[var(--color-border)] text-center">
      <p className="text-xs text-[var(--color-muted)] tracking-tight">
        DescribeX © {new Date().getFullYear()} · Built for AMD Developer Hackathon: ACT II
      </p>
    </footer>
  );
}
