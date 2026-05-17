import type { Metadata } from "next";
import { Geist, Geist_Mono, Raleway } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { AuthProvider } from "@/lib/auth-context";
import Navbar from "@/components/Navbar";

const ralewayHeading = Raleway({ subsets: ['latin'], variable: '--font-heading' });
const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "StoryForge — Craft Your Interactive Tale",
  description:
    "An AI-powered interactive storytelling platform. Begin your adventure, shape the narrative, and explore worlds born from your imagination.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={cn(ralewayHeading.variable, "dark")}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased text-foreground min-h-screen`}
      >
        <AuthProvider>
          <Navbar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
