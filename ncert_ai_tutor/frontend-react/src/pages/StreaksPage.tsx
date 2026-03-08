import { useState, useEffect } from 'react';
import { Flame, Loader2, Trophy, Calendar, Target } from 'lucide-react';
import { api } from '../lib/api';

interface StreaksPageProps {
  username: string;
  showToast: (msg: string, type: 'success' | 'error' | 'info') => void;
}

export default function StreaksPage({ username, showToast }: StreaksPageProps) {
  const [streakData, setStreakData] = useState<{
    current_streak: number;
    longest_streak: number;
    today_questions: number;
    streak_active_today: boolean;
    history: { date: string; question_count: number; streak_active: boolean }[];
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStreak();
  }, [username]);

  const loadStreak = async () => {
    setLoading(true);
    try {
      const data = await api.getStreaks(username);
      setStreakData(data);
    } catch {
      showToast('Failed to load streak data', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 size={32} className="animate-spin text-primary" />
      </div>
    );
  }

  if (!streakData) return null;

  const questionsNeeded = Math.max(0, 3 - streakData.today_questions);
  const progress = Math.min(100, (streakData.today_questions / 3) * 100);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate mb-2 flex items-center gap-2">
          <Flame size={28} className="text-amber" />
          Study Streaks
        </h1>
        <p className="text-slate-light">
          Ask 3+ questions daily to keep your streak alive!
        </p>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="bg-card rounded-xl border border-border p-5 text-center">
          <Flame size={32} className="mx-auto mb-2 text-amber" />
          <p className="text-3xl font-bold text-slate">{streakData.current_streak}</p>
          <p className="text-sm text-slate-light">Current Streak</p>
        </div>
        <div className="bg-card rounded-xl border border-border p-5 text-center">
          <Trophy size={32} className="mx-auto mb-2 text-primary" />
          <p className="text-3xl font-bold text-slate">{streakData.longest_streak}</p>
          <p className="text-sm text-slate-light">Longest Streak</p>
        </div>
        <div className="bg-card rounded-xl border border-border p-5 text-center">
          <Target size={32} className="mx-auto mb-2 text-teal" />
          <p className="text-3xl font-bold text-slate">{streakData.today_questions}</p>
          <p className="text-sm text-slate-light">Today's Questions</p>
        </div>
      </div>

      {/* Progress */}
      <div className="bg-card rounded-xl border border-border p-6 mb-8">
        <h2 className="text-lg font-semibold text-slate mb-4">Today's Progress</h2>
        <div className="flex items-center gap-6">
          <div className="flex-1">
            <div className="w-full h-4 bg-surface-dark rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${
                  progress >= 100 ? 'bg-teal' : 'bg-primary'
                }`}
                style={{ width: `${progress}%` }}
              />
            </div>
            <div className="flex justify-between mt-2">
              <span className="text-sm text-slate-light">
                {streakData.today_questions} / 3 questions
              </span>
              {streakData.streak_active_today ? (
                <span className="text-sm font-medium text-teal">🔥 Streak active!</span>
              ) : (
                <span className="text-sm text-slate-light">
                  {questionsNeeded} more to activate streak
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* History */}
      {streakData.history.length > 0 && (
        <div className="bg-card rounded-xl border border-border p-6">
          <h2 className="text-lg font-semibold text-slate mb-4 flex items-center gap-2">
            <Calendar size={20} />
            Recent History
          </h2>
          <div className="grid grid-cols-7 gap-2">
            {streakData.history.slice(-28).map((day, i) => (
              <div
                key={i}
                className={`aspect-square rounded-lg flex items-center justify-center text-xs font-medium ${
                  day.streak_active
                    ? 'bg-teal/20 text-teal'
                    : day.question_count > 0
                    ? 'bg-primary/15 text-primary'
                    : 'bg-surface-dark text-slate-light/30'
                }`}
                title={`${day.date}: ${day.question_count} questions`}
              >
                {day.question_count || '·'}
              </div>
            ))}
          </div>
          <div className="flex items-center gap-4 mt-3 text-xs text-slate-light">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-sm bg-teal/20" /> Streak active
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-sm bg-primary/15" /> Questions asked
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-sm bg-surface-dark" /> No activity
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
