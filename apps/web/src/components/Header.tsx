import Image from 'next/image';

export default function Header() {
  return (
    <header className="w-full py-6 px-8 border-b border-zinc-800 bg-black sticky top-0 z-10 transition-all">
      <div className="max-w-[1280px] mx-auto flex items-center justify-between">
        <a href="/" className="flex items-center gap-3 group transition-opacity hover:opacity-80">
          <Image 
            src="/describex-logo-without_bg.png" 
            alt="DescribeX Logo" 
            width={40} 
            height={40} 
            className="object-contain"
          />
          <h1 className="text-2xl font-bold tracking-tight text-white">
            DescribeX
          </h1>
        </a>
        <p className="text-zinc-400 text-sm hidden sm:block font-medium">AI-Powered Multi-Style Video Captioning</p>
      </div>
    </header>
  );
}
