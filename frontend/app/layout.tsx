import type { Metadata } from "next";
import { type ReactNode } from "react";

import { AppShell } from "@/components/shell/app-shell";

import "./globals.css";

export const metadata: Metadata = {
  title: "Cognitive Deception | Cyber Intelligence Console",
  description: "AI-powered adaptive honeypot intelligence dashboard"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="font-body antialiased">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
