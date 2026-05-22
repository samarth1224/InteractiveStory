import { AuthResponse } from "@/interfaces/auth.type";
import { UserPublic } from "@/interfaces/user.type";

const API_BASE = process.env.NEXT_PUBLIC_API_URL;

/**
 * Log in with username + password.
 * The backend sets an HTTP-only cookie automatically.
 */
export async function loginUser(
  username: string,
  password: string
): Promise<AuthResponse> {
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${API_BASE}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    credentials: "include",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail || "Login failed");
  }
  return res.json();
}

/**
 * Register a new account.
 * The backend sets an HTTP-only cookie automatically.
 */
export async function signupUser(
  username: string,
  password: string
): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Signup failed" }));
    throw new Error(err.detail || "Signup failed");
  }
  return res.json();
}

/**
 * Continue as guest — creates a temporary account on the backend.
 */
export async function loginAsGuest(): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/auth/guest`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error("Guest login failed");
  }
  return res.json();
}

/**
 * Clear the HTTP-only cookie on the backend.
 */
export async function logoutUser(): Promise<void> {
  await fetch(`${API_BASE}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
}

/**
 * Fetch the current user's profile using the cookie.
 * Returns `null` if unauthenticated.
 */
export async function fetchCurrentUser(): Promise<UserPublic | null> {
  try {
    const res = await fetch(`${API_BASE}/users/me`, {
      credentials: "include",
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}
