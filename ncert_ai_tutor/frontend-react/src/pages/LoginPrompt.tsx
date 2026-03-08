import { useState } from 'react';
import { User, ArrowRight } from 'lucide-react';

interface LoginPromptProps {
  onLogin: (username: string) => void;
}

export default function LoginPrompt({ onLogin }: LoginPromptProps) {
  const [name, setName] = useState('');

  const submit = () => {
    const trimmed = name.trim();
    if (trimmed) onLogin(trimmed);
  };

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        <div className="text-6xl mb-6">🎓</div>
        <h1 className="text-3xl font-bold text-slate mb-2">StudyMate AI</h1>
        <p className="text-slate-light mb-1">NCERT AI Tutor for Class 9–10</p>
        <p className="text-sm text-slate-light/60 mb-8">
          Your personal AI study companion — learn NCERT concepts easily
        </p>

        <div className="bg-card rounded-2xl border border-border p-8">
          <div className="w-16 h-16 rounded-full bg-primary/15 flex items-center justify-center mx-auto mb-4">
            <User size={28} className="text-primary" />
          </div>
          <h2 className="text-lg font-semibold text-slate mb-1">What's your name?</h2>
          <p className="text-sm text-slate-light mb-5">Enter your name to start studying</p>

          <form
            onSubmit={e => { e.preventDefault(); submit(); }}
            className="space-y-3"
          >
            <input
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Vijay, Hema, Arjun..."
              autoFocus
              className="w-full px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-center text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
            />
            <button
              type="submit"
              disabled={!name.trim()}
              className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Start Learning
              <ArrowRight size={18} />
            </button>
          </form>
        </div>

        <p className="text-xs text-slate-light/40 mt-6">
          No sign-up needed — just enter a name and go!
        </p>
      </div>
    </div>
  );
}
