export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  topic?: string;
  audioUrl?: string;
}

export interface ChatResponse {
  answer: string;
  detected_topic: string;
  difficulty_used: string;
}

export interface VoiceResponse {
  audio_base64: string;
  language_used: string;
}

export interface PracticeQuestion {
  difficulty: string;
  question: string;
}

export interface PracticeResponse {
  topic: string;
  questions: PracticeQuestion[];
}

export interface ConceptMapResponse {
  topic: string;
  svg_content: string;
}

export interface MistakeResponse {
  analysis: string;
  topic: string;
}

export interface StreakData {
  current_streak: number;
  longest_streak: number;
  today_questions: number;
  streak_active_today: boolean;
  history: { date: string; question_count: number; streak_active: boolean }[];
}

export interface AnalyticsWeekly {
  topic_frequency: { topic: string; count: number }[];
}

export interface AnalyticsConfused {
  confused_topics: { topic: string; repeat_count: number }[];
}

export interface AnalyticsDailyCounts {
  daily_counts: { date: string; count: number }[];
}

export interface User {
  username: string;
  role: 'student' | 'teacher';
}
