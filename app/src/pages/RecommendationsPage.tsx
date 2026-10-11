import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Lightbulb, TrendingUp, BookOpen, ArrowRight } from 'lucide-react';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { recommendationService } from '../services';
import type { Recommendation } from '../types';

function AccuracyBadge({ pct }: { pct: number | null }) {
  if (pct === null) {
    return (
      <span className="inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
        No attempts
      </span>
    );
  }
  const color =
    pct >= 80
      ? 'bg-green-100 text-green-700'
      : pct >= 50
      ? 'bg-yellow-100 text-yellow-700'
      : 'bg-red-100 text-red-700';
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {pct}% accuracy
    </span>
  );
}

function ActionIcon({ pct }: { pct: number | null }) {
  if (pct === null) return <BookOpen size={18} className="text-gray-400" />;
  if (pct >= 80) return <TrendingUp size={18} className="text-green-500" />;
  if (pct >= 50) return <BookOpen size={18} className="text-yellow-500" />;
  return <ArrowRight size={18} className="text-red-400" />;
}

export default function RecommendationsPage() {
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    recommendationService
      .list()
      .then((res) => setRecs(res.data))
      .catch(() => setError('Failed to load recommendations.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout title="Recommendations"><LoadingSpinner /></Layout>;
  if (error) return <Layout title="Recommendations"><ErrorMessage message={error} /></Layout>;

  return (
    <Layout title="Recommendations">
      <div className="mb-6">
        <p className="text-sm text-gray-500 -mt-4">
          Personalised study recommendations based on your quiz performance and topic completion.
        </p>
      </div>

      {/* How it works */}
      <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-4 mb-6 text-sm text-indigo-800">
        <div className="flex items-start gap-2">
          <Lightbulb size={16} className="mt-0.5 shrink-0 text-indigo-500" />
          <div>
            <strong>How recommendations work:</strong> Below 50% accuracy → revision recommended.
            50–79% → additional practice. 80%+ → advance to the next topic.
            No quiz attempts → start with the first topic.
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {recs.map((r, i) => (
          <div key={i} className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-3 flex-1">
                <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
                  <ActionIcon pct={r.accuracy_pct} />
                </div>
                <div>
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <h3 className="text-sm font-semibold text-gray-900">{r.subject_name}</h3>
                    <AccuracyBadge pct={r.accuracy_pct} />
                  </div>
                  <p className="text-base font-medium text-indigo-700 mb-1">{r.topic_title}</p>
                  <p className="text-xs text-gray-600 mb-2">{r.reason}</p>
                  <div className="bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-700">
                    <span className="font-medium">Suggested action: </span>{r.action}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 text-center">
        <p className="text-xs text-gray-400">
          Complete more quizzes to get updated recommendations.{' '}
          <Link to="/quizzes" className="text-indigo-600 hover:underline">Take a quiz →</Link>
        </p>
      </div>
    </Layout>
  );
}
