import { useState, useEffect, useCallback } from 'react';
import type { ChatMessage, User } from './types';

// ---------- user store (localStorage-backed) ----------
const USER_KEY = 'studymate_ai_user';

export function useUser() {
  const [user, setUserState] = useState<User | null>(() => {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  });

  const setUser = useCallback((u: User | null) => {
    if (u) localStorage.setItem(USER_KEY, JSON.stringify(u));
    else localStorage.removeItem(USER_KEY);
    setUserState(u);
  }, []);

  return { user, setUser };
}

// ---------- sidebar state ----------
export function useSidebar() {
  const [open, setOpen] = useState(false);
  const toggle = useCallback(() => setOpen(p => !p), []);
  return { open, setOpen, toggle };
}

// ---------- chat history (session-scoped) ----------
export function useChatHistory() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const addMessage = useCallback((msg: ChatMessage) => {
    setMessages(prev => [...prev, msg]);
  }, []);

  const clearMessages = useCallback(() => setMessages([]), []);

  return { messages, loading, setLoading, addMessage, clearMessages };
}

// ---------- audio playback ----------
export function useAudioPlayer() {
  const [playing, setPlaying] = useState<string | null>(null);

  const playBase64 = useCallback((base64: string, id: string) => {
    const audio = new Audio(`data:audio/mp3;base64,${base64}`);
    setPlaying(id);
    audio.onended = () => setPlaying(null);
    audio.play();
  }, []);

  return { playing, playBase64 };
}

// ---------- toast notifications ----------
export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const show = useCallback((message: string, type: Toast['type'] = 'info') => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 5000);
  }, []);

  return { toasts, show };
}

// ---------- debounced value ----------
export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}
