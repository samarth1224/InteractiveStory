"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { LogOut, User, Ghost } from "lucide-react";

export default function Navbar() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push("/auth/login");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-3.5 bg-background/80 backdrop-blur-xl border-b border-border">
      {/* Brand */}
      <Link
        href="/"
        className="font-bold tracking-widest text-xl text-foreground hover:text-muted-foreground transition-colors"
      >
        StoryForge
      </Link>

      {/* Nav Links */}
      <div className="flex items-center gap-7">
        <Link href="/" className="text-muted-foreground text-sm font-medium hover:text-foreground transition-colors">
          Home
        </Link>
        <Link href="/explore" className="text-muted-foreground text-sm font-medium hover:text-foreground transition-colors">
          Explore
        </Link>
        <Link href="/my-stories" className="text-muted-foreground text-sm font-medium hover:text-foreground transition-colors">
          My Stories
        </Link>
        <Link
          href="/new"
          className="bg-foreground text-background text-sm font-semibold px-5 py-2 rounded-xl hover:-translate-y-0.5 hover:opacity-90 transition-all"
        >
          Start Writing
        </Link>

        {/* Auth state */}
        <AnimatePresence mode="wait">
          {!loading && (
            <motion.div
              key={user ? "user" : "login"}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
              className="flex items-center gap-3"
            >
              {user ? (
                <>
                  {/* User badge */}
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-muted/50 border border-border/50">
                    {user.is_guest ? (
                      <Ghost className="w-3.5 h-3.5 text-muted-foreground" strokeWidth={1.75} />
                    ) : (
                      <User className="w-3.5 h-3.5 text-muted-foreground" strokeWidth={1.75} />
                    )}
                    <span className="text-xs font-medium text-muted-foreground max-w-[100px] truncate">
                      {user.is_guest ? "Guest" : user.username}
                    </span>
                  </div>

                  {/* Logout */}
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                    className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
                    title="Log out"
                  >
                    <LogOut className="w-3.5 h-3.5" strokeWidth={1.75} />
                  </motion.button>
                </>
              ) : (
                <Link
                  href="/auth/login"
                  className="text-muted-foreground text-sm font-medium hover:text-foreground transition-colors"
                >
                  Login
                </Link>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  );
}
