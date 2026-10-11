import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ClipboardList, ChevronRight, Clock } from 'lucide-react';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { quizService } from '../services';
import type { QuizListItem, QuizAttempt } from '../types';

export default function QuizzesPage() {
  const [quizzes, setQuizzes] = useState<QuizListItem[]>([]);
  const [attempts, setAttempts] = useState<QuizAttempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([quizService.list(), quizService.attempts()])
      .then(([q, a]) => {
        setQuizzes(q.data);
        setAttempts(a.data);
      })
      .catch(() => setError('Failed to load quizzes.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout title="Quizzes"><LoadingSpinner /></Layout>;
  if (error) return <Layout title="Quizzes"><ErrorMessage message={error} /></Layout>;

  // Group quizzes by subject
  const bySubject: Record<string, QuizListItem[]> = {};
  quizzes.forEach((q) => {
    if (!bySubject[q.subject_name]) bySubject[q.subject_name] = [];
    bySubject[q.subject_name].push(q);
  });

  // Last attempt per quiz
  const lastAttempt: Record<number, QuizAttempt> = {};
  attempts.forEach((a) => {
    if (!lastAttempt[a.quiz_id] || a.attempted_at > lastAttempt[a.quiz_id].attempted_at) {
      lastAttempt[a.quiz_id] = a;
    }
  });

  return (
    <Layout title="Quizzes">
      <p className="text-sm text-gray-500 -mt-4 mb-6">
        Test your knowledge. Scores are calculated on the backend.
      </p>

      <div className="space-y-6 mb-8">
        {Object.entries(bySubject).map(([subjectName, qs]) => (
          <div key={subjectName}>
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
              {subjectName}
            </h2>
            <div className="space-y-3">
              {qs.map((q) => {
                const last = lastAttempt[q.id];
                return (
                  <div
                    key={q.id}
                    className="bg-white rounded-xl border border-gray-200 p-4 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center">
                        <ClipboardList size={18} className="text-indigo-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">{q.title}</p>
                        <p className="text-xs text-gray-500">{q.question_count} questions</p>
                        {last && (
                          <p className="text-xs text-gray-400 mt-0.5 flex items-center gap-1">
                            <Clock size={10} />
                            Last score:{' '}
                            <span className={`font-medium ${last.accuracy_pct >= 80 ? 'text-green-600' : last.accuracy_pct >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                              {last.accuracy_pct}%
                            </span>
                          </p>
                        )}
                      </div>
                    </div>
                    <Link
                      to={`/quizzes/${q.id}`}
                      className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800"
                    >
                      {last ? 'Retake' : 'Start'} <ChevronRight size={14} />
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Attempt history */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-base font-semibold text-gray-900 mb-4">All Attempts</h2>
        {attempts.length === 0 ? (
          <div className="text-center py-8">
            <ClipboardList size={32} className="text-gray-300 mx-auto mb-2" />
            <p className="text-sm text-gray-400">No attempts yet. Pick a quiz above and start!</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left text-xs font-semibold text-gray-500 pb-2">Quiz</th>
                  <th className="text-left text-xs font-semibold text-gray-500 pb-2">Subject</th>
                  <th className="text-center text-xs font-semibold text-gray-500 pb-2">Score</th>
                  <th className="text-center text-xs font-semibold text-gray-500 pb-2">Accuracy</th>
                  <th className="text-right text-xs font-semibold text-gray-500 pb-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map((a) => (
                  <tr key={a.id} className="border-b border-gray-50">
                    <td className="py-2.5 pr-4 font-medium text-gray-800">{a.quiz_title}</td>
                    <td className="py-2.5 pr-4 text-gray-500">{a.subject_name}</td>
                    <td className="py-2.5 text-center text-gray-800">
                      {a.score}/{a.total_questions}
                    </td>
                    <td className="py-2.5 text-center">
                      <span
                        className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${
                          a.accuracy_pct >= 80
                            ? 'bg-green-100 text-green-700'
                            : a.accuracy_pct >= 50
                            ? 'bg-yellow-100 text-yellow-700'
                            : 'bg-red-100 text-red-700'
                        }`}
                      >
                        {a.accuracy_pct}%
                      </span>
                    </td>
                    <td className="py-2.5 text-right text-gray-400 text-xs">
                      {new Date(a.attempted_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}
