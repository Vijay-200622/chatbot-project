import { Link } from 'react-router-dom';
import { MessageCircle, ClipboardList, Flame, BookOpen, LayoutDashboard } from 'lucide-react';

const FEATURES = [
  {
    icon: MessageCircle,
    title: 'AI Chat',
    desc: 'Ask any doubt — in English, Hinglish, or Tanglish',
    to: '/chat',
    color: 'text-primary',
  },
  {
    icon: ClipboardList,
    title: 'Practice Questions',
    desc: 'Easy, Medium, Hard — NCERT-aligned questions per concept',
    to: '/practice',
    color: 'text-teal',
  },
  {
    icon: BookOpen,
    title: 'Mistake Analyzer',
    desc: 'Paste your wrong answer — get targeted correction',
    to: '/mistakes',
    color: 'text-coral',
  },
  {
    icon: Flame,
    title: 'Study Streaks',
    desc: 'Track your daily study streak and stay consistent',
    to: '/streaks',
    color: 'text-amber',
  },
  {
    icon: LayoutDashboard,
    title: 'Teacher Dashboard',
    desc: 'Analytics on top topics, confused concepts, and more',
    to: '/teacher',
    color: 'text-purple',
  },
];

interface HomePageProps {
  username?: string;
  onStartChat: () => void;
}

export default function HomePage({ username }: HomePageProps) {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Hero */}
      <div className="text-center mb-10">
        <div className="text-6xl mb-4">🎓</div>
        <h1 className="text-3xl sm:text-4xl font-bold text-slate mb-3">
          StudyMate AI
        </h1>
        <p className="text-lg text-slate-light mb-2">NCERT AI Tutor for Class 9–10</p>
        <p className="text-base text-slate-light/70 mb-8">
          Your personal AI study companion — learn any NCERT concept easily
        </p>

        <div className="flex items-center justify-center gap-3">
          <Link
            to="/chat"
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary-dark transition-colors shadow-lg shadow-primary/20"
          >
            <MessageCircle size={20} />
            Start Chat
          </Link>
          <Link
            to="/practice"
            className="inline-flex items-center gap-2 px-6 py-3 bg-surface-dark text-primary border border-border rounded-xl font-semibold hover:bg-surface-mid transition-colors"
          >
            <ClipboardList size={20} />
            Practice Now
          </Link>
        </div>
      </div>

      {/* Greeting */}
      {username && (
        <div className="bg-teal/10 border border-teal/20 rounded-xl px-5 py-4 mb-8 text-center">
          <p className="text-teal font-medium">
            Welcome back, <span className="font-bold">{username}</span>! Ready to study?
          </p>
        </div>
      )}

      {/* Feature cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {FEATURES.map(f => (
          <Link
            key={f.to}
            to={f.to}
            className="group bg-card rounded-xl border border-border p-5 hover:border-primary/40 transition-all"
          >
            <div className={`w-10 h-10 rounded-lg bg-surface-dark flex items-center justify-center mb-3 ${f.color}`}>
              <f.icon size={20} />
            </div>
            <h3 className="font-semibold text-slate mb-1 group-hover:text-primary transition-colors">
              {f.title}
            </h3>
            <p className="text-sm text-slate-light">{f.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
