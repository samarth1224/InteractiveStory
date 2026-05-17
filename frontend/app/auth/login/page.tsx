"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    LogIn,
    UserPlus,
    Ghost,
    Eye,
    EyeOff,
    ArrowRight,
    Loader2,
    AlertCircle,
    Sparkles,
} from "lucide-react";

type AuthTab = "login" | "signup";

export default function LoginPage() {
    const router = useRouter();
    const { login, signup, continueAsGuest } = useAuth();

    const [tab, setTab] = useState<AuthTab>("login");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [guestLoading, setGuestLoading] = useState(false);

    const resetForm = () => {
        setUsername("");
        setPassword("");
        setConfirmPassword("");
        setError("");
    };

    const switchTab = (newTab: AuthTab) => {
        resetForm();
        setTab(newTab);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (!username.trim() || !password.trim()) {
            setError("Please fill in all fields");
            return;
        }

        if (tab === "signup" && password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        if (password.length < 4) {
            setError("Password must be at least 4 characters");
            return;
        }

        setLoading(true);
        try {
            if (tab === "login") {
                await login(username, password);
            } else {
                await signup(username, password);
            }
            router.push("/");
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    const handleGuest = async () => {
        setGuestLoading(true);
        setError("");
        try {
            await continueAsGuest();
            router.push("/");
        } catch {
            setError("Guest login failed. Please try again.");
        } finally {
            setGuestLoading(false);
        }
    };

    return (
        <main className="min-h-screen pt-[72px] flex items-center justify-center px-6 py-16 relative overflow-hidden">
            {/* ── Ambient gradient orbs ───────────────────────── */}
            <div className="absolute -top-32 -left-40 w-[700px] h-[700px] rounded-full pointer-events-none blur-[140px] animate-[orbFloat_18s_ease-in-out_infinite] bg-[radial-gradient(circle,rgba(99,102,241,0.10)_0%,transparent_70%)]" />
            <div className="absolute bottom-0 right-0 w-[500px] h-[500px] rounded-full pointer-events-none blur-[120px] animate-[orbFloat_22s_ease-in-out_-8s_infinite] bg-[radial-gradient(circle,rgba(56,189,248,0.07)_0%,transparent_70%)]" />

            <motion.div
                initial={{ opacity: 0, y: 40, scale: 0.97 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                className="w-full max-w-md relative z-10"
            >
                <Card className="border-border/60 shadow-2xl backdrop-blur-sm bg-card/80">
                    <CardHeader className="text-center pb-2">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: 0.2, type: "spring", stiffness: 200, damping: 15 }}
                            className="mx-auto w-14 h-14 rounded-2xl bg-foreground/5 border border-border/60 flex items-center justify-center mb-4"
                        >
                            <Sparkles className="w-6 h-6 text-foreground/70" strokeWidth={1.5} />
                        </motion.div>
                        <CardTitle className="text-2xl font-bold tracking-tight">
                            {tab === "login" ? "Welcome Back" : "Create Account"}
                        </CardTitle>
                        <CardDescription className="text-muted-foreground mt-1">
                            {tab === "login"
                                ? "Sign in to continue your adventure"
                                : "Join StoryForge and start crafting tales"}
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="space-y-6 pt-4">
                        {/* ── Tab Switcher ──────────────────────────── */}
                        <div className="flex rounded-xl bg-muted/50 p-1 gap-1">
                            {(["login", "signup"] as const).map((t) => (
                                <button
                                    key={t}
                                    onClick={() => switchTab(t)}
                                    className={`
                    relative flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200
                    ${tab === t
                                            ? "text-foreground"
                                            : "text-muted-foreground hover:text-foreground/80"
                                        }
                  `}
                                >
                                    {tab === t && (
                                        <motion.div
                                            layoutId="auth-tab-bg"
                                            className="absolute inset-0 bg-background rounded-lg shadow-sm border border-border/40"
                                            transition={{ type: "spring", stiffness: 400, damping: 30 }}
                                        />
                                    )}
                                    <span className="relative z-10 flex items-center gap-2">
                                        {t === "login" ? (
                                            <LogIn className="w-3.5 h-3.5" strokeWidth={2} />
                                        ) : (
                                            <UserPlus className="w-3.5 h-3.5" strokeWidth={2} />
                                        )}
                                        {t === "login" ? "Sign In" : "Sign Up"}
                                    </span>
                                </button>
                            ))}
                        </div>

                        {/* ── Error Banner ──────────────────────────── */}
                        <AnimatePresence mode="wait">
                            {error && (
                                <motion.div
                                    key="error"
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: "auto" }}
                                    exit={{ opacity: 0, height: 0 }}
                                    className="flex items-center gap-2.5 px-4 py-3 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm"
                                >
                                    <AlertCircle className="w-4 h-4 flex-shrink-0" strokeWidth={2} />
                                    <span>{error}</span>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* ── Form ──────────────────────────────────── */}
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={tab}
                                    initial={{ opacity: 0, x: tab === "login" ? -16 : 16 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: tab === "login" ? 16 : -16 }}
                                    transition={{ duration: 0.25, ease: "easeOut" }}
                                    className="space-y-4"
                                >
                                    {/* Username */}
                                    <div className="space-y-2">
                                        <Label htmlFor="username">Username</Label>
                                        <Input
                                            id="username"
                                            type="text"
                                            placeholder="Enter your username"
                                            value={username}
                                            onChange={(e) => setUsername(e.target.value)}
                                            autoComplete="username"
                                            className="h-11"
                                        />
                                    </div>

                                    {/* Password */}
                                    <div className="space-y-2">
                                        <Label htmlFor="password">Password</Label>
                                        <div className="relative">
                                            <Input
                                                id="password"
                                                type={showPassword ? "text" : "password"}
                                                placeholder="Enter your password"
                                                value={password}
                                                onChange={(e) => setPassword(e.target.value)}
                                                autoComplete={tab === "login" ? "current-password" : "new-password"}
                                                className="h-11 pr-10"
                                            />
                                            <button
                                                type="button"
                                                onClick={() => setShowPassword(!showPassword)}
                                                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                                                tabIndex={-1}
                                            >
                                                {showPassword ? (
                                                    <EyeOff className="w-4 h-4" strokeWidth={1.75} />
                                                ) : (
                                                    <Eye className="w-4 h-4" strokeWidth={1.75} />
                                                )}
                                            </button>
                                        </div>
                                    </div>

                                    {/* Confirm Password (signup only) */}
                                    {tab === "signup" && (
                                        <motion.div
                                            initial={{ opacity: 0, height: 0 }}
                                            animate={{ opacity: 1, height: "auto" }}
                                            exit={{ opacity: 0, height: 0 }}
                                            className="space-y-2"
                                        >
                                            <Label htmlFor="confirmPassword">Confirm Password</Label>
                                            <Input
                                                id="confirmPassword"
                                                type={showPassword ? "text" : "password"}
                                                placeholder="Confirm your password"
                                                value={confirmPassword}
                                                onChange={(e) => setConfirmPassword(e.target.value)}
                                                autoComplete="new-password"
                                                className="h-11"
                                            />
                                        </motion.div>
                                    )}
                                </motion.div>
                            </AnimatePresence>

                            {/* Submit */}
                            <motion.div whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }}>
                                <Button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full h-11 bg-foreground text-background hover:bg-foreground/90 font-semibold text-sm rounded-xl transition-all"
                                >
                                    {loading ? (
                                        <Loader2 className="w-4 h-4 animate-spin" />
                                    ) : (
                                        <>
                                            {tab === "login" ? "Sign In" : "Create Account"}
                                            <ArrowRight className="w-4 h-4 ml-1.5" strokeWidth={2} />
                                        </>
                                    )}
                                </Button>
                            </motion.div>
                        </form>

                        {/* ── Divider ───────────────────────────────── */}
                        <div className="flex items-center gap-4">
                            <div className="flex-1 h-px bg-border" />
                            <span className="text-xs text-muted-foreground font-medium uppercase tracking-wider">
                                or
                            </span>
                            <div className="flex-1 h-px bg-border" />
                        </div>

                        {/* ── Guest button ──────────────────────────── */}
                        <motion.div whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }}>
                            <Button
                                type="button"
                                variant="outline"
                                onClick={handleGuest}
                                disabled={guestLoading}
                                className="w-full h-11 rounded-xl text-sm font-medium gap-2 border-border hover:bg-foreground/5 hover:border-foreground/30 transition-all"
                            >
                                {guestLoading ? (
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                ) : (
                                    <>
                                        <Ghost className="w-4 h-4" strokeWidth={1.75} />
                                        Continue as Guest
                                    </>
                                )}
                            </Button>
                        </motion.div>

                        {/* ── Footer note ───────────────────────────── */}
                        <p className="text-center text-xs text-muted-foreground/70 pt-2">
                            Guest accounts are temporary. Sign up to save your stories.
                        </p>
                    </CardContent>
                </Card>
            </motion.div>
        </main>
    );
}
