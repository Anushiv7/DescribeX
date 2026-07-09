export default function Footer() {
  return (
    <footer className="w-full py-8 mt-12 border-t border-zinc-800 text-center">
      <p className="text-zinc-500 text-sm">
        DescribeX &copy; {new Date().getFullYear()}. Built for AMD Developer Hackathon: ACT II.
      </p>
    </footer>
  );
}
