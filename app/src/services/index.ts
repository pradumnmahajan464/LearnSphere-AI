import api from './api';
import type {
  User, TokenResponse, DashboardData,
  SubjectListItem, SubjectDetail,
  QuizListItem, QuizDetail, QuizSubmitResponse, QuizAttempt,
  Recommendation,
} from '../types';

// ─── Auth ─────────────────────────────────────────────────────────────────
export const authService = {
  register: (name: string, email: string, password: string) =>
    api.post<User>('/api/auth/register', { name, email, password }),

  login: async (email: string, password: string): Promise<string> => {
    const res = await api.post<TokenResponse>('/api/auth/login', { email, password });
    localStorage.setItem('token', res.data.access_token);
    return res.data.access_token;
  },

  me: () => api.get<User>('/api/auth/me'),

  logout: () => {
    localStorage.removeItem('token');
  },
};

// ─── Dashboard ────────────────────────────────────────────────────────────
export const dashboardService = {
  get: () => api.get<DashboardData>('/api/dashboard'),
};

// ─── Subjects ─────────────────────────────────────────────────────────────
export const subjectService = {
  list: () => api.get<SubjectListItem[]>('/api/subjects'),
  get: (id: number) => api.get<SubjectDetail>(`/api/subjects/${id}`),
  completeTopic: (topicId: number) =>
    api.post(`/api/topics/${topicId}/complete`),
};

// ─── Quizzes ──────────────────────────────────────────────────────────────
export const quizService = {
  list: () => api.get<QuizListItem[]>('/api/quizzes'),
  get: (id: number) => api.get<QuizDetail>(`/api/quizzes/${id}`),
  submit: (id: number, answers: number[]) =>
    api.post<QuizSubmitResponse>(`/api/quizzes/${id}/submit`, { answers }),
  attempts: () => api.get<QuizAttempt[]>('/api/quiz-attempts'),
};

// ─── Recommendations ──────────────────────────────────────────────────────
export const recommendationService = {
  list: () => api.get<Recommendation[]>('/api/recommendations'),
};
