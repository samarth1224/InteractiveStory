"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import {
  fetchCurrentUser,
  loginUser,
  signupUser,
  loginAsGuest,
  logoutUser,
} from "@/lib/auth";
import { UserPublic } from "@/interfaces/user.type";

/* ── Context shape ─────────────────────────────────────────── */
interface AuthContextValue {
  /** The currently authenticated user, or `null` if not logged in. */
  user: UserPublic | null;
  /** `true` while the initial check is in progress. */
  loading: boolean;
  /** Log in with credentials; throws on failure. */
  login: (username: string, password: string) => Promise<void>;
  /** Register a new account; throws on failure. */
  signup: (username: string, password: string) => Promise<void>;
  /** Continue as guest. */
  continueAsGuest: () => Promise<void>;
  /** Log out and clear the session. */
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/* ── Provider ──────────────────────────────────────────────── */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserPublic | null>(null);
  const [loading, setLoading] = useState(true);

  // On mount, attempt to fetch the current user from the cookie.
  useEffect(() => {
    fetchCurrentUser()
      .then(setUser)
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    await loginUser(username, password);
    const u = await fetchCurrentUser();
    setUser(u);
  }, []);

  const signup = useCallback(async (username: string, password: string) => {
    await signupUser(username, password);
    const u = await fetchCurrentUser();
    setUser(u);
  }, []);

  const continueAsGuest = useCallback(async () => {
    await loginAsGuest();
    const u = await fetchCurrentUser();
    setUser(u);
  }, []);

  const logout = useCallback(async () => {
    await logoutUser();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, login, signup, continueAsGuest, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

/* ── Hook ──────────────────────────────────────────────────── */
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an <AuthProvider>");
  }
  return ctx;
}
