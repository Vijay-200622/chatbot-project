import { useState, useEffect } from 'react';
import { LayoutDashboard, Loader2, Lock, Download } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts';
import { api } from '../lib/api';

interface TeacherPageProps {
  showToast: (msg: string, type: 'success' | 'error' | 'info') => void;
}

export default function TeacherPage({ showToast }: TeacherPageProps) {
  const [loggedIn, setLoggedIn] = useState(false);
  const [loginUser, setLoginUser] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  const [weeklyData, setWeeklyData] = useState<{ topic: string; count: number }[]>([]);
  const [confusedData, setConfusedData] = useState<{ topic: string; repeat_count: number }[]>([]);
  const [dailyData, setDailyData] = useState<{ date: string; count: number }[]>([]);
  const [dataLoading, setDataLoading] = useState(false);

  const handleLogin = async () => {
    if (!loginUser || !loginPass) return;
    setLoginLoading(true);
    try {
      const res = await api.teacherLogin(loginUser, loginPass);
      if (res.success) {
        setLoggedIn(true);
        showToast('Logged in as teacher', 'success');
      } else {
        showToast(res.message || 'Invalid credentials', 'error');
      }
    } catch {
      showToast('Invalid credentials', 'error');
    } finally {
      setLoginLoading(false);
    }
  };

  useEffect(() => {
    if (!loggedIn) return;
    loadData();
  }, [loggedIn]);

  const loadData = async () => {
    setDataLoading(true);
    try {
      const [w, c, d] = await Promise.all([
        api.weeklyTopics(),
        api.confusedTopics(),
        api.dailyCounts(),
      ]);
      setWeeklyData(w);
      setConfusedData(c);
      setDailyData(d);
    } catch {
      showToast('Failed to load analytics', 'error');
    } finally {
      setDataLoading(false);
    }
  };

  const exportCSV = () => {
    const rows = [['Topic', 'Weekly Count'], ...weeklyData.map(d => [d.topic, d.count.toString()])];
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'weekly_topics.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Login screen
  if (!loggedIn) {
    return (
      <div className="max-w-sm mx-auto px-4 py-20">
        <div className="bg-card rounded-xl border border-border p-8 text-center">
          <Lock size={40} className="mx-auto mb-4 text-primary" />
          <h2 className="text-xl font-bold text-slate mb-1">Teacher Login</h2>
          <p className="text-sm text-slate-light mb-6">Enter credentials to access analytics</p>
          <div className="space-y-3">
            <input
              type="text"
              value={loginUser}
              onChange={e => setLoginUser(e.target.value)}
              placeholder="Username"
              className="w-full px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
            />
            <input
              type="password"
              value={loginPass}
              onChange={e => setLoginPass(e.target.value)}
              placeholder="Password"
              className="w-full px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
            />
            <button
              onClick={handleLogin}
              disabled={loginLoading}
              className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary-dark transition-colors disabled:opacity-50"
            >
              {loginLoading ? <Loader2 size={18} className="animate-spin" /> : <Lock size={18} />}
              Login
            </button>
          </div>
          <p className="text-xs text-slate-light/50 mt-4">Default: teacher / teach123</p>
        </div>
      </div>
    );
  }

  // Dashboard
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate flex items-center gap-2">
            <LayoutDashboard size={28} className="text-primary" />
            Teacher Dashboard
          </h1>
          <p className="text-slate-light">Analytics on student activity and topics</p>
        </div>
        <button
          onClick={exportCSV}
          className="inline-flex items-center gap-2 px-4 py-2 bg-surface-dark border border-border rounded-lg text-sm font-medium text-slate-light hover:border-primary/40 hover:text-primary transition-colors"
        >
          <Download size={16} />
          Export CSV
        </button>
      </div>

      {dataLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 size={32} className="animate-spin text-primary" />
        </div>
      ) : (
        <div className="space-y-6">
          {/* KPI cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-card rounded-xl border border-border p-5">
              <p className="text-sm text-slate-light">Topics This Week</p>
              <p className="text-2xl font-bold text-primary">{weeklyData.length}</p>
            </div>
            <div className="bg-card rounded-xl border border-border p-5">
              <p className="text-sm text-slate-light">Confused Topics</p>
              <p className="text-2xl font-bold text-coral">{confusedData.length}</p>
            </div>
            <div className="bg-card rounded-xl border border-border p-5">
              <p className="text-sm text-slate-light">Total Questions (7d)</p>
              <p className="text-2xl font-bold text-teal">
                {dailyData.reduce((s, d) => s + d.count, 0)}
              </p>
            </div>
          </div>

          {/* Top Topics Bar Chart */}
          <div className="bg-card rounded-xl border border-border p-6">
            <h2 className="text-lg font-semibold text-slate mb-4">Top Asked Topics This Week</h2>
            {weeklyData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={weeklyData.slice(0, 10)}>
                  <XAxis dataKey="topic" tick={{ fontSize: 12, fill: '#8B949E' }} angle={-20} textAnchor="end" height={80} />
                  <YAxis tick={{ fontSize: 12, fill: '#8B949E' }} />
                  <Tooltip contentStyle={{ backgroundColor: '#161B22', border: '1px solid #30363D', borderRadius: '8px', color: '#E6EDF3' }} />
                  <Bar dataKey="count" fill="#58A6FF" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-sm text-slate-light py-10 text-center">No data yet — students need to ask questions!</p>
            )}
          </div>

          {/* Confused Topics */}
          <div className="bg-card rounded-xl border border-border p-6">
            <h2 className="text-lg font-semibold text-slate mb-4">Most Confusing Concepts</h2>
            {confusedData.length > 0 ? (
              <div className="space-y-2">
                {confusedData.slice(0, 10).map((t, i) => (
                  <div key={i} className="flex items-center justify-between py-2 border-b border-border last:border-0">
                    <span className="text-sm text-slate">{t.topic}</span>
                    <span className="text-sm font-medium text-coral">{t.repeat_count} repeated asks</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-light py-10 text-center">No confused topics detected yet</p>
            )}
          </div>

          {/* Daily Question Counts */}
          <div className="bg-card rounded-xl border border-border p-6">
            <h2 className="text-lg font-semibold text-slate mb-4">Daily Question Counts</h2>
            {dailyData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={dailyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#30363D" />
                  <XAxis dataKey="date" tick={{ fontSize: 12, fill: '#8B949E' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#8B949E' }} />
                  <Tooltip contentStyle={{ backgroundColor: '#161B22', border: '1px solid #30363D', borderRadius: '8px', color: '#E6EDF3' }} />
                  <Line type="monotone" dataKey="count" stroke="#3FB950" strokeWidth={2} dot={{ fill: '#3FB950' }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-sm text-slate-light py-10 text-center">No daily data yet</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
