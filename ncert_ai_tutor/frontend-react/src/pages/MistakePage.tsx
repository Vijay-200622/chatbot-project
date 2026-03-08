import { useState } from 'react';
import { BookOpen, Loader2, ChevronDown } from 'lucide-react';
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

interface MistakePageProps {
  showToast: (msg: string, type: 'success' | 'error' | 'info') => void;
}

export default function MistakePage({ showToast }: MistakePageProps) {
  const [topic, setTopic] = useState('');
  const [questionContext, setQuestionContext] = useState('');
  const [studentAnswer, setStudentAnswer] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!topic || !studentAnswer.trim()) return;
    setLoading(true);
    setAnalysis('');
    try {
      const data = await api.analyzeMistake(studentAnswer, topic, questionContext || undefined);
      setAnalysis(data.analysis);
      showToast('Mistake analysis complete!', 'success');
    } catch {
      showToast('Failed to analyze — try again', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate mb-2 flex items-center gap-2">
          <BookOpen size={28} className="text-coral" />
          Mistake Analyzer
        </h1>
        <p className="text-slate-light">
          Paste your wrong answer — get targeted correction with explanations
        </p>
      </div>

      <div className="bg-card rounded-xl border border-border p-6 space-y-4">
        {/* Topic */}
        <div>
          <label className="block text-sm font-medium text-slate mb-1.5">Topic</label>
          <div className="relative">
            <select
              value={topic}
              onChange={e => setTopic(e.target.value)}
              className="w-full appearance-none px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary pr-10"
            >
              <option value="">Select topic...</option>
              {TOPICS.map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            <ChevronDown size={18} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-light pointer-events-none" />
          </div>
        </div>

        {/* Question context */}
        <div>
          <label className="block text-sm font-medium text-slate mb-1.5">
            Question (optional)
          </label>
          <input
            type="text"
            value={questionContext}
            onChange={e => setQuestionContext(e.target.value)}
            placeholder="e.g. What is the formula for photosynthesis?"
            className="w-full px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
          />
        </div>

        {/* Student answer */}
        <div>
          <label className="block text-sm font-medium text-slate mb-1.5">
            Your Answer <span className="text-coral">*</span>
          </label>
          <textarea
            value={studentAnswer}
            onChange={e => setStudentAnswer(e.target.value)}
            placeholder="Paste your answer here..."
            rows={5}
            className="w-full px-4 py-3 bg-surface-dark border border-border rounded-xl text-sm text-slate placeholder:text-slate-light/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary resize-none"
          />
        </div>

        <button
          onClick={analyze}
          disabled={!topic || !studentAnswer.trim() || loading}
          className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 bg-coral text-white rounded-xl font-medium hover:bg-coral-dark transition-colors disabled:opacity-50"
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <BookOpen size={18} />}
          Analyze My Answer
        </button>
      </div>

      {/* Analysis result */}
      {analysis && (
        <div className="mt-6 bg-card rounded-xl border border-border p-6 animate-fade-in-up">
          <h2 className="text-lg font-semibold text-slate mb-3 flex items-center gap-2">
            📝 Analysis Result
          </h2>
          <div className="text-sm text-slate-light leading-relaxed whitespace-pre-wrap">
            {analysis}
          </div>
        </div>
      )}
    </div>
  );
}
