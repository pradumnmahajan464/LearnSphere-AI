import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CheckCircle2, XCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { quizService } from '../services';
import type { QuizDetail, QuizSubmitResponse } from '../types';

type QuizState = 'taking' | 'submitted';

export default function QuizDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState<QuizDetail | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [state, setState] = useState<QuizState>('taking');
  const [result, setResult] = useState<QuizSubmitResponse | null>(null);
  const [currentQ, setCurrentQ] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    quizService
      .get(Number(id))
      .then((res) => setQuiz(res.data))
      .catch(() => setError('Failed to load quiz.'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleSelect = (optionIndex: number) => {
    if (state === 'submitted') return;
    setAnswers((prev) => ({ ...prev, [currentQ]: optionIndex }));
  };

  const handleSubmit = async () => {
    if (!quiz) return;
    const answersArray = quiz.questions.map((_, i) => answers[i] ?? 0);
    setSubmitting(true);
    try {
      const res = await quizService.submit(quiz.id, answersArray);
      setResult(res.data);
      setState('submitted');
      setCurrentQ(0);
    } catch {
      setError('Failed to submit quiz. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Layout><LoadingSpinner /></Layout>;
  if (error) return <Layout><ErrorMessage message={error} /></Layout>;
  if (!quiz) return null;

  const totalQ = quiz.questions.length;
  const answeredCount = Object.keys(answers).length;

  // ─── Results view ──────────────────────────────────────────────────────────
  if (state === 'submitted' && result) {
    const current = result.results[currentQ];
    return (
      <Layout>
        <button
          onClick={() => navigate('/quizzes')}
          className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-4"
        >
          <ChevronLeft size={16} /> Back to Quizzes
        </button>

        {/* Score summary */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-5 text-center">
          <p className="text-sm text-gray-500 mb-1">{quiz.title}</p>
          <p
            className={`text-5xl font-bold mb-1 ${
              result.accuracy_pct >= 80
                ? 'text-green-600'
                : result.accuracy_pct >= 50
                ? 'text-yellow-600'
                : 'text-red-600'
            }`}
          >
            {result.accuracy_pct}%
          </p>
          <p className="text-gray-500 text-sm">
            {result.score} / {result.total_questions} correct
          </p>
          <p className="mt-2 text-sm font-medium text-gray-700">
            {result.accuracy_pct >= 80
              ? '🎉 Excellent work! Ready to advance.'
              : result.accuracy_pct >= 50
              ? '📚 Good effort! A bit more practice will help.'
              : '🔄 Keep revising — you\'ll get there!'}
          </p>
        </div>

        {/* Question review navigation */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-gray-900">Review Answers</h2>
            <span className="text-xs text-gray-500">{currentQ + 1} / {totalQ}</span>
          </div>

          <p className="text-sm font-medium text-gray-800 mb-4">{current.question_text}</p>

          <div className="space-y-2 mb-4">
            {quiz.questions[currentQ].options.map((opt, i) => {
              const isSelected = i === current.selected;
              const isCorrect = i === current.correct;
              let cls = 'border border-gray-200 bg-gray-50 text-gray-700';
              if (isCorrect) cls = 'border border-green-400 bg-green-50 text-green-800';
              else if (isSelected && !isCorrect) cls = 'border border-red-400 bg-red-50 text-red-800';
              return (
                <div key={i} className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm ${cls}`}>
                  {isCorrect ? (
                    <CheckCircle2 size={15} className="text-green-500 shrink-0" />
                  ) : isSelected ? (
                    <XCircle size={15} className="text-red-500 shrink-0" />
                  ) : (
                    <span className="w-4" />
                  )}
                  {opt}
                </div>
              );
            })}
          </div>

          {current.explanation && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 text-xs text-blue-800">
              <span className="font-semibold">Explanation: </span>{current.explanation}
            </div>
          )}

          <div className="flex items-center justify-between mt-4">
            <button
              onClick={() => setCurrentQ((p) => p - 1)}
              disabled={currentQ === 0}
              className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 disabled:opacity-40"
            >
              <ChevronLeft size={16} /> Previous
            </button>
            <div className="flex gap-1.5">
              {result.results.map((r, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentQ(i)}
                  className={`w-6 h-6 rounded-full text-xs font-medium transition-colors ${
                    i === currentQ
                      ? 'bg-indigo-600 text-white'
                      : r.is_correct
                      ? 'bg-green-200 text-green-700'
                      : 'bg-red-200 text-red-700'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
            </div>
            <button
              onClick={() => setCurrentQ((p) => p + 1)}
              disabled={currentQ === totalQ - 1}
              className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 disabled:opacity-40"
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  // ─── Quiz-taking view ──────────────────────────────────────────────────────
  const question = quiz.questions[currentQ];

  return (
    <Layout>
      <button
        onClick={() => navigate('/quizzes')}
        className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-4"
      >
        <ChevronLeft size={16} /> Back to Quizzes
      </button>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-semibold text-gray-900">{quiz.title}</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Question {currentQ + 1} of {totalQ}
            </p>
          </div>
          <span className="text-xs text-gray-500">{answeredCount}/{totalQ} answered</span>
        </div>

        {/* Progress dots */}
        <div className="flex gap-1.5 mb-6">
          {quiz.questions.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 flex-1 rounded-full transition-colors ${
                i === currentQ
                  ? 'bg-indigo-500'
                  : answers[i] !== undefined
                  ? 'bg-indigo-200'
                  : 'bg-gray-200'
              }`}
            />
          ))}
        </div>

        <p className="text-sm font-medium text-gray-800 mb-4">{question.question_text}</p>

        <div className="space-y-2 mb-6">
          {question.options.map((opt, i) => (
            <button
              key={i}
              onClick={() => handleSelect(i)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm text-left transition-all border ${
                answers[currentQ] === i
                  ? 'border-indigo-500 bg-indigo-50 text-indigo-800'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50 text-gray-700'
              }`}
            >
              <span
                className={`w-6 h-6 rounded-full border text-xs flex items-center justify-center shrink-0 ${
                  answers[currentQ] === i
                    ? 'border-indigo-500 bg-indigo-500 text-white'
                    : 'border-gray-300 text-gray-400'
                }`}
              >
                {String.fromCharCode(65 + i)}
              </span>
              {opt}
            </button>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <button
            onClick={() => setCurrentQ((p) => p - 1)}
            disabled={currentQ === 0}
            className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 disabled:opacity-40"
          >
            <ChevronLeft size={16} /> Previous
          </button>

          {currentQ < totalQ - 1 ? (
            <button
              onClick={() => setCurrentQ((p) => p + 1)}
              className="flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-800"
            >
              Next <ChevronRight size={16} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting || answeredCount === 0}
              className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
            >
              {submitting ? 'Submitting...' : `Submit Quiz (${answeredCount}/${totalQ} answered)`}
            </button>
          )}
        </div>
      </div>
    </Layout>
  );
}
