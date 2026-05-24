import type { Metadata } from "next";
import { Outfit, Cinzel, EB_Garamond } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { AuthProvider } from "@/lib/auth-context";
import Navbar from "@/components/Navbar";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-sans",
});
const cinzel = Cinzel({
  subsets: ["latin"],
  variable: "--font-cinzel",
});
const ebGaramond = EB_Garamond({
  subsets: ["latin"],
  variable: "--font-garamond",
});

export const metadata: Metadata = {
  title: "InteractiveStory",
  description:
    "An AI-powered interactive story creation platform. Begin your adventure, shape the narrative, and explore worlds born from your imagination.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={cn(cinzel.variable, "dark")}>
      <body
        className={`${outfit.variable} ${cinzel.variable} ${ebGaramond.variable} antialiased text-foreground min-h-screen font-sans`}
      >
        <AuthProvider>
          <Navbar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
