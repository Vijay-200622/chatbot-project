import { Menu, User, LogOut } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

interface TopBarProps {
  onMenuClick: () => void;
  username?: string;
  onLogout: () => void;
  pageTitle?: string;
}

export default function TopBar({ onMenuClick, username, onLogout, pageTitle }: TopBarProps) {
  const [profileOpen, setProfileOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setProfileOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  return (
    <header className="sticky top-0 z-30 bg-surface-mid border-b border-border px-4 h-14 flex items-center justify-between">
      {/* Left: hamburger + title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="p-2 rounded-lg hover:bg-surface-dark transition-colors"
          aria-label="Open menu"
        >
          <Menu size={22} className="text-slate-light" />
        </button>
        <div className="flex items-center gap-2">
          <span className="text-xl">🎓</span>
          <span className="font-semibold text-base text-slate hidden sm:inline">StudyMate AI</span>
        </div>
        {pageTitle && (
          <span className="text-sm text-slate-light font-medium ml-2 hidden md:inline">
            / {pageTitle}
          </span>
        )}
      </div>

      {/* Right: profile */}
      <div className="relative" ref={dropdownRef}>
        {username ? (
          <button
            onClick={() => setProfileOpen(p => !p)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-surface-dark transition-colors"
          >
            <div className="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center text-sm font-bold">
              {username[0].toUpperCase()}
            </div>
            <span className="text-sm font-medium text-slate hidden sm:inline">{username}</span>
          </button>
        ) : (
          <div className="flex items-center gap-2 px-3 py-1.5 text-slate-light">
            <User size={20} />
            <span className="text-sm">Not logged in</span>
          </div>
        )}

        {/* Dropdown */}
        {profileOpen && username && (
          <div className="absolute right-0 top-full mt-1 w-48 bg-surface-mid border border-border rounded-lg shadow-xl py-1 z-50">
            <div className="px-4 py-2 border-b border-border">
              <p className="text-sm font-medium text-slate">{username}</p>
              <p className="text-xs text-slate-light">Student</p>
            </div>
            <button
              onClick={() => { onLogout(); setProfileOpen(false); }}
              className="w-full flex items-center gap-2 px-4 py-2 text-sm text-coral hover:bg-surface-dark transition-colors"
            >
              <LogOut size={16} />
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
