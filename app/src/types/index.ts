// ─── Auth ──────────────────────────────────────────────────────────────────
export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// ─── Subjects / Topics ────────────────────────────────────────────────────
export interface Topic {
  id: number;
  subject_id: number;
  title: string;
  notes: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  order_index: number;
  completed: boolean;
}

export interface SubjectListItem {
  id: number;
  name: string;
  description: string;
  icon: string;
  topic_count: number;
  completed_count: number;
  progress_pct: number;
}

export interface SubjectDetail {
  id: number;
  name: string;
  description: string;
  icon: string;
  topics: Topic[];
  progress_pct: number;
}

// ─── Quizzes ───────────────────────────────────────────────────────────────
export interface QuizListItem {
  id: number;
  subject_id: number;
  subject_name: string;
  title: string;
  question_count: number;
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  options: string[];
}

export interface QuizDetail {
  id: number;
  subject_id: number;
  title: string;
  questions: QuizQuestion[];
}

export interface AnswerResult {
  question_id: number;
  question_text: string;
  selected: number;
  correct: number;
  is_correct: boolean;
  explanation?: string;
}

export interface QuizSubmitResponse {
  attempt_id: number;
  score: number;
  total_questions: number;
  accuracy_pct: number;
  results: AnswerResult[];
}

export interface QuizAttempt {
  id: number;
  quiz_id: number;
  quiz_title: string;
  subject_name: string;
  score: number;
  total_questions: number;
  accuracy_pct: number;
  attempted_at: string;
}

// ─── Dashboard ────────────────────────────────────────────────────────────
export interface DashboardData {
  student_name: string;
  enrolled_subjects: number;
  quiz_average_pct: number;
  completed_lessons: number;
  total_lessons: number;
  subject_progress: SubjectListItem[];
  recent_attempts: QuizAttempt[];
  recommended_topic: string | null;
}

// ─── Recommendations ─────────────────────────────────────────────────────
export interface Recommendation {
  subject_name: string;
  topic_title: string;
  reason: string;
  action: string;
  accuracy_pct: number | null;
}
