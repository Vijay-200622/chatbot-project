import { NavLink } from 'react-router-dom';
import {
  Home, MessageCircle, ClipboardList, Flame,
  LayoutDashboard, X, BookOpen,
} from 'lucide-react';

const NAV_ITEMS = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/chat', label: 'AI Chat', icon: MessageCircle },
  { to: '/practice', label: 'Practice', icon: ClipboardList },
  { to: '/mistakes', label: 'Mistake Analyzer', icon: BookOpen },
  { to: '/streaks', label: 'Streaks', icon: Flame },
  { to: '/teacher', label: 'Teacher Dashboard', icon: LayoutDashboard },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  username?: string;
}

export default function Sidebar({ open, onClose, username }: SidebarProps) {
  return (
    <>
      {/* Overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-sm"
          onClick={onClose}
        />
      )}

      {/* Drawer */}
      <aside
        className={`fixed top-0 left-0 h-full w-72 bg-sidebar-bg text-slate z-50 transform transition-transform duration-300 ease-in-out flex flex-col border-r border-border ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-border">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🎓</span>
            <div>
              <h2 className="text-base font-semibold leading-tight text-slate">StudyMate AI</h2>
              <p className="text-xs text-slate-light">NCERT AI Tutor</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-sidebar-hover transition-colors text-slate-light hover:text-slate"
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        </div>

        {/* User quick-profile */}
        {username && (
          <div className="px-5 py-3 border-b border-border">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-primary/20 text-primary flex items-center justify-center text-sm font-bold">
                {username[0].toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-medium text-slate">{username}</p>
                <p className="text-xs text-slate-light">Student</p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-3 px-3">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors mb-0.5 ${
                  isActive
                    ? 'bg-primary/15 text-primary'
                    : 'text-slate-light hover:bg-sidebar-hover hover:text-slate'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-border text-xs text-slate-light/60">
          Built for NCERT students
        </div>
      </aside>
    </>
  );
}
