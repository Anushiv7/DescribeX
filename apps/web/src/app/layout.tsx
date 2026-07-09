import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import "./globals.css";

export const metadata: Metadata = {
  title: "DescribeX — Create Once. Caption Everywhere.",
  description: "AI-Powered Accessible Video Captioning",
  icons: {
    icon: [
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" }],
  },
  manifest: "/site.webmanifest",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`dark ${GeistSans.variable}`}>
      <body className={`${GeistSans.className} bg-[var(--color-bg)] text-[var(--color-fg)] antialiased`}>
        {children}
      </body>
    </html>
  );
}
