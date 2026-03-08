import { useState, useRef, useEffect } from 'react';
import { Send, Volume2, Loader2 } from 'lucide-react';
import { api } from '../lib/api';
import type { ChatMessage } from '../lib/types';
import TypingIndicator from '../components/TypingIndicator';

interface ChatPageProps {
  username: string;
  showToast: (msg: string, type: 'success' | 'error' | 'info') => void;
}

export default function ChatPage({ username, showToast }: ChatPageProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [playingId, setPlayingId] = useState<number | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async () => {
    const q = input.trim();
    if (!q || loading) return;

    const userMsg: ChatMessage = { role: 'user', content: q, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const data = await api.chat(q, username);
      const botMsg: ChatMessage = {
        role: 'assistant',
        content: data.answer,
        timestamp: new Date().toISOString(),
        topic: data.detected_topic ?? undefined,
      };
      setMessages(prev => [...prev, botMsg]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, couldn\'t get a response from AI. Please try again!', timestamp: new Date().toISOString() },
      ]);
      showToast('Failed to get response from AI', 'error');
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const playVoice = async (text: string, idx: number) => {
    if (playingId !== null) return;
    setPlayingId(idx);
    try {
      const data = await api.voice(text);
      const audio = new Audio(`data:audio/mp3;base64,${data.audio_base64}`);
      audio.onended = () => setPlayingId(null);
      audio.onerror = () => setPlayingId(null);
      audio.play();
    } catch {
      setPlayingId(null);
      showToast('Voice playback failed', 'error');
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)]">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.length === 0 && !loading && (
            <div className="text-center py-20">
              <div className="text-5xl mb-4">💬</div>
              <h2 className="text-xl font-semibold text-slate mb-2">Start a conversation</h2>
              <p className="text-slate-light">
                Ask any NCERT doubt — in English, Hinglish, or Tanglish!
              </p>
              <div className="flex flex-wrap justify-center gap-2 mt-6">
                {[
                  'Explain photosynthesis simply',
                  'What is Newton\'s second law?',
                  'Solve a quadratic equation',
                  'Causes of the French Revolution',
                ].map(suggestion => (
                  <button
                    key={suggestion}
                    onClick={() => { setInput(suggestion); inputRef.current?.focus(); }}
                    className="px-3 py-2 bg-surface-dark border border-border rounded-lg text-sm text-slate-light hover:border-primary/40 hover:text-primary transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 animate-fade-in-up ${
                msg.role === 'user' ? 'flex-row-reverse' : ''
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-teal/20 text-teal font-bold'
                    : 'bg-primary/15 text-primary'
                }`}
              >
                {msg.role === 'user' ? username[0].toUpperCase() : '🎓'}
              </div>

              {/* Bubble */}
              <div className={`max-w-[75%] ${msg.role === 'user' ? 'text-right' : ''}`}>
                <div
                  className={`inline-block rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                    msg.role === 'user'
                      ? 'bg-primary/15 text-slate rounded-tr-sm'
                      : 'bg-surface-dark border border-border text-slate rounded-tl-sm'
                  }`}
                >
                  {msg.content}
                </div>

                {/* Voice button for assistant */}
                {msg.role === 'assistant' && (
                  <div className="flex items-center gap-2 mt-1">
                    <button
                      onClick={() => playVoice(msg.content, idx)}
                      disabled={playingId !== null}
                      className="inline-flex items-center gap-1 text-xs text-slate-light hover:text-primary transition-colors disabled:opacity-50"
                    >
                      {playingId === idx ? (
                        <Loader2 size={14} className="animate-spin" />
                      ) : (
                        <Volume2 size={14} />
                      )}
                      {playingId === idx ? 'Playing...' : 'Listen'}
                    </button>
                    {msg.topic && (
                      <span className="text-xs text-slate-light/60">
                        Topic: {msg.topic}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Composer */}
      <div className="border-t border-border bg-surface-mid px-4 py-3">
        <div className="max-w-3xl mx-auto">
          <form
            onSubmit={e => { e.preventDefault(); sendMessage(); }}
            className="flex items-center gap-2"
          >
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Type your question here..."
              className="flex-1 px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="p-3 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} />}
            </button>
          </form>
          <p className="text-xs text-slate-light/50 mt-2 text-center">
            StudyMate AI answers NCERT Class 9–10 questions only
          </p>
        </div>
      </div>
    </div>
  );
}
