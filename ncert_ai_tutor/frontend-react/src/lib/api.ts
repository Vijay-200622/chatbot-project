const BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  chat(question: string, username: string) {
    return request<{ answer: string; detected_topic: string | null; difficulty_level: string; within_syllabus: boolean }>(
      '/chat', { method: 'POST', body: JSON.stringify({ question, username }) }
    );
  },

  async voice(text: string): Promise<{ audio_base64: string }> {
    const res = await fetch(`${BASE}/chat/voice`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    const blob = await res.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const dataUrl = reader.result as string;
        resolve({ audio_base64: dataUrl.split(',')[1] });
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  },

  async practice(topic: string): Promise<{ topic: string; questions: { difficulty: string; question: string }[] }> {
    const raw = await request<{ easy: string; medium: string; hard: string }>(
      '/practice', { method: 'POST', body: JSON.stringify({ topic }) }
    );
    return {
      topic,
      questions: [
        { difficulty: 'Easy', question: raw.easy },
        { difficulty: 'Medium', question: raw.medium },
        { difficulty: 'Hard', question: raw.hard },
      ],
    };
  },

  conceptMap(topic: string) {
    return request<{ svg: string; edges: string[][]; dot_source: string }>(
      '/concept-map', { method: 'POST', body: JSON.stringify({ topic }) }
    );
  },

  analyzeMistake(student_answer: string, topic: string, question_context?: string) {
    return request<{ analysis: string }>(
      '/analyze-mistake', { method: 'POST', body: JSON.stringify({ student_answer, question: question_context ?? '', topic }) }
    );
  },

  async getStreaks(username: string) {
    const raw = await request<{
      current_streak: number; longest_streak: number;
      today_count: number;
      history: { date: string; question_count: number; streak_active: number }[];
    }>(`/streaks/${encodeURIComponent(username)}`);
    return {
      current_streak: raw.current_streak,
      longest_streak: raw.longest_streak,
      today_questions: raw.today_count,
      streak_active_today: raw.today_count >= 3,
      history: raw.history.map(h => ({
        date: h.date,
        question_count: h.question_count,
        streak_active: !!h.streak_active,
      })),
    };
  },

  weeklyTopics() {
    return request<{ topic: string; count: number }[]>('/analytics/weekly-topics');
  },

  confusedTopics() {
    return request<{ topic: string; user_id: number; repeat_count: number }[]>('/analytics/confused-topics');
  },

  dailyCounts() {
    return request<{ date: string; count: number }[]>('/analytics/daily-counts');
  },

  teacherLogin(username: string, password: string) {
    return request<{ success: boolean; message: string; user_id: number | null }>(
      '/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }
    );
  },
};
