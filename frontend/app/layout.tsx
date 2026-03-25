import type { Metadata } from "next";
import { Cormorant_Garamond, DM_Mono, Bebas_Neue } from "next/font/google";
import "./globals.css";

const cormorantGaramond = Cormorant_Garamond({
  weight: ["300", "400", "600"],
  subsets: ["latin"],
  variable: "--font-cormorant",
});

const dmMono = DM_Mono({
  weight: ["300", "400", "500"],
  subsets: ["latin"],
  variable: "--font-dm-mono",
});

const bebasNeue = Bebas_Neue({
  weight: ["400"],
  subsets: ["latin"],
  variable: "--font-bebas",
});

export const metadata: Metadata = {
  title: "StratosAI — Startup Intelligence Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${cormorantGaramond.variable} ${dmMono.variable} ${bebasNeue.variable} min-h-screen bg-[#0a0a0b] text-[#f0ede6] antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
