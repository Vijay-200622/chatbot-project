import { useState, useEffect, useRef } from 'react';
import { ClipboardList, Loader2, ChevronDown, Timer, Brain, CheckCircle, Trophy } from 'lucide-react';
import { api } from '../lib/api';

const TOPICS = [
  'Photosynthesis', 'Cell Structure', 'Tissues', 'Atoms and Molecules',
  'Force and Laws of Motion', 'Gravitation', 'Work and Energy',
  'Sound', 'Light Reflection', 'Electricity', 'Magnetic Effects',
  'Chemical Reactions', 'Acids Bases and Salts', 'Metals and Non-metals',
  'Carbon Compounds', 'Periodic Classification',
  'Linear Equations', 'Quadratic Equations', 'Triangles', 'Circles',
  'Statistics', 'Probability', 'Polynomials', 'Coordinate Geometry',
  'Trigonometry', 'Surface Areas and Volumes', 'Arithmetic Progressions',
  'French Revolution', 'Nazism', 'Indian National Movement',
  'Democracy', 'Indian Constitution', 'Poverty',
];

type PracticeMode = 'questions' | 'timed';

interface Question {
  difficulty: string;
  question: string;
}

interface PracticePageProps {
  showToast: (msg: string, type: 'success' | 'error' | 'info') => void;
}

export default function PracticePage({ showToast }: PracticePageProps) {
  const [topic, setTopic] = useState('');
  const [mode, setMode] = useState<PracticeMode>('questions');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [conceptSvg, setConceptSvg] = useState('');
  const [loadingMap, setLoadingMap] = useState(false);

  // Quiz state
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState<Record<number, boolean>>({});

  // Timed challenge state
  const [timerActive, setTimerActive] = useState(false);
  const [timeLeft, setTimeLeft] = useState(120); // 2 minutes
  const [, setTimedScore] = useState(0);
  const [timedCompleted, setTimedCompleted] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (timerActive && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            setTimerActive(false);
            setTimedCompleted(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [timerActive, timeLeft]);

  const generate = async () => {
    if (!topic) return;
    setLoading(true);
    setQuestions([]);
    setAnswers({});
    setSubmitted({});
    setTimedCompleted(false);
    setTimedScore(0);
    try {
      const data = await api.practice(topic);
      setQuestions(data.questions);
      showToast(`Generated ${data.questions.length} questions on ${topic}`, 'success');
      if (mode === 'timed') {
        setTimeLeft(120);
        setTimerActive(true);
      }
    } catch {
      showToast('Failed to generate questions', 'error');
    } finally {
      setLoading(false);
    }
  };

  const generateMap = async () => {
    if (!topic) return;
    setLoadingMap(true);
    setConceptSvg('');
    try {
      const data = await api.conceptMap(topic);
      setConceptSvg(data.svg);
    } catch {
      showToast('Failed to generate concept map', 'error');
    } finally {
      setLoadingMap(false);
    }
  };

  const submitAnswer = (idx: number) => {
    setSubmitted(prev => ({ ...prev, [idx]: true }));
    if (mode === 'timed') {
      setTimedScore(prev => prev + 1);
      if (Object.keys(submitted).length + 1 >= questions.length) {
        setTimerActive(false);
        setTimedCompleted(true);
      }
    }
  };

  const difficultyColor = (d: string) => {
    switch (d.toLowerCase()) {
      case 'easy': return 'border-teal/30 bg-teal/5';
      case 'medium': return 'border-amber/30 bg-amber/5';
      case 'hard': return 'border-coral/30 bg-coral/5';
      default: return 'border-border bg-surface-dark';
    }
  };

  const difficultyBadge = (d: string) => {
    switch (d.toLowerCase()) {
      case 'easy': return 'text-teal';
      case 'medium': return 'text-amber';
      case 'hard': return 'text-coral';
      default: return 'text-slate-light';
    }
  };

  const formatTime = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate mb-2 flex items-center gap-2">
          <ClipboardList size={28} className="text-primary" />
          Practice Questions
        </h1>
        <p className="text-slate-light">
          Select a topic and generate NCERT-aligned practice questions
        </p>
      </div>

      {/* Mode selector */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setMode('questions')}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            mode === 'questions'
              ? 'bg-primary/15 text-primary border border-primary/30'
              : 'bg-surface-dark text-slate-light border border-border hover:border-primary/20'
          }`}
        >
          <Brain size={16} />
          Practice Mode
        </button>
        <button
          onClick={() => setMode('timed')}
          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            mode === 'timed'
              ? 'bg-coral/15 text-coral border border-coral/30'
              : 'bg-surface-dark text-slate-light border border-border hover:border-coral/20'
          }`}
        >
          <Timer size={16} />
          Timed Challenge
        </button>
      </div>

      {/* Controls */}
      <div className="bg-card rounded-xl border border-border p-5 mb-6">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <select
              value={topic}
              onChange={e => setTopic(e.target.value)}
              className="w-full appearance-none px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary pr-10"
            >
              <option value="">Select a topic...</option>
              {TOPICS.map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            <ChevronDown size={18} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-light pointer-events-none" />
          </div>

          <button
            onClick={generate}
            disabled={!topic || loading}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary-dark transition-colors disabled:opacity-50"
          >
            {loading ? <Loader2 size={18} className="animate-spin" /> : <ClipboardList size={18} />}
            {mode === 'timed' ? 'Start Challenge' : 'Generate Questions'}
          </button>

          <button
            onClick={generateMap}
            disabled={!topic || loadingMap}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-surface-dark text-primary border border-border rounded-xl font-medium hover:border-primary/40 transition-colors disabled:opacity-50"
          >
            {loadingMap ? <Loader2 size={18} className="animate-spin" /> : '🗺️'}
            Concept Map
          </button>
        </div>
      </div>

      {/* Timed challenge header */}
      {mode === 'timed' && questions.length > 0 && (
        <div className={`rounded-xl border p-4 mb-6 flex items-center justify-between ${
          timedCompleted ? 'bg-teal/10 border-teal/30' : 'bg-surface-dark border-border'
        }`}>
          <div className="flex items-center gap-3">
            <Timer size={20} className={timedCompleted ? 'text-teal' : timeLeft <= 30 ? 'text-coral' : 'text-primary'} />
            <span className={`text-lg font-bold font-mono ${
              timedCompleted ? 'text-teal' : timeLeft <= 30 ? 'text-coral' : 'text-slate'
            }`}>
              {timedCompleted ? 'Completed!' : formatTime(timeLeft)}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Trophy size={18} className="text-amber" />
            <span className="text-sm font-medium text-slate">
              {Object.keys(submitted).length} / {questions.length} answered
            </span>
          </div>
        </div>
      )}

      {/* Timed challenge results */}
      {mode === 'timed' && timedCompleted && (
        <div className="bg-card rounded-xl border border-border p-6 mb-6 text-center animate-fade-in-up">
          <Trophy size={40} className="mx-auto mb-3 text-amber" />
          <h2 className="text-xl font-bold text-slate mb-2">Challenge Complete!</h2>
          <p className="text-slate-light mb-4">
            You answered {Object.keys(submitted).length} of {questions.length} questions
            {timeLeft > 0 ? ` with ${formatTime(timeLeft)} remaining` : ' — time ran out!'}
          </p>
          <button
            onClick={generate}
            disabled={loading}
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-medium hover:bg-primary-dark transition-colors"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Questions */}
      {questions.length > 0 && (
        <div className="space-y-4 mb-8">
          <h2 className="text-lg font-semibold text-slate">
            Questions on "{topic}"
          </h2>
          {questions.map((q, i) => (
            <div
              key={i}
              className={`rounded-xl border p-5 animate-fade-in-up ${difficultyColor(q.difficulty)}`}
            >
              <div className="flex-1">
                <span className={`inline-block text-xs font-bold uppercase tracking-wider mb-2 ${difficultyBadge(q.difficulty)}`}>
                  {q.difficulty}
                </span>
                <p className="text-sm leading-relaxed text-slate">{q.question}</p>

                {/* Answer input */}
                <div className="mt-3">
                  {!submitted[i] ? (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={answers[i] || ''}
                        onChange={e => setAnswers(prev => ({ ...prev, [i]: e.target.value }))}
                        placeholder="Type your answer..."
                        className="flex-1 px-3 py-2 bg-surface-dark border border-border rounded-lg text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30"
                        disabled={mode === 'timed' && (timedCompleted || timeLeft <= 0)}
                      />
                      <button
                        onClick={() => submitAnswer(i)}
                        disabled={!answers[i]?.trim() || (mode === 'timed' && (timedCompleted || timeLeft <= 0))}
                        className="px-4 py-2 bg-primary/15 text-primary rounded-lg text-sm font-medium hover:bg-primary/25 transition-colors disabled:opacity-50"
                      >
                        <CheckCircle size={16} />
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-sm text-teal">
                      <CheckCircle size={16} />
                      <span>Answer submitted</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Concept Map */}
      {conceptSvg && (
        <div className="bg-card rounded-xl border border-border p-5">
          <h2 className="text-lg font-semibold text-slate mb-4">
            Concept Map: {topic}
          </h2>
          <div
            className="overflow-auto"
            dangerouslySetInnerHTML={{ __html: conceptSvg }}
          />
        </div>
      )}
    </div>
  );
}
