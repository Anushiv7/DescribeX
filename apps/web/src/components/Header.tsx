import Image from 'next/image';

interface HeaderProps {
  variant?: 'default' | 'minimal';
}

export default function Header({ variant = 'default' }: HeaderProps) {
  if (variant === 'minimal') {
    return <header className="h-6" aria-hidden />;
  }

  return (
    <header className="w-full border-b border-[var(--color-border)] bg-[var(--color-bg)]/80 backdrop-blur-md sticky top-0 z-10">
      <div className="max-w-[1240px] mx-auto flex items-center justify-between px-6 h-16">
        <a href="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-80">
          <Image
            src="/describex-logo-without_bg.png"
            alt="DescribeX"
            width={34}
            height={34}
            className="object-contain"
          />
          <span className="text-[18px] font-semibold tracking-tight text-[var(--color-fg)]">DescribeX</span>
        </a>
        <p className="hidden sm:block text-[15px] text-[#B5B5B5] tracking-tight">
          Create Once. Caption Everywhere.
        </p>
      </div>
    </header>
  );
}
