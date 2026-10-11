import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CheckCircle2, Circle, ChevronLeft, BookOpen } from 'lucide-react';
import Layout from '../components/Layout';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { subjectService } from '../services';
import type { SubjectDetail, Topic } from '../types';

const difficultyColors: Record<string, string> = {
  Beginner: 'bg-green-100 text-green-700',
  Intermediate: 'bg-yellow-100 text-yellow-700',
  Advanced: 'bg-red-100 text-red-700',
};

export default function SubjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [subject, setSubject] = useState<SubjectDetail | null>(null);
  const [activeTopic, setActiveTopic] = useState<Topic | null>(null);
  const [completing, setCompleting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    subjectService
      .get(Number(id))
      .then((res) => {
        setSubject(res.data);
        if (res.data.topics.length > 0) setActiveTopic(res.data.topics[0]);
      })
      .catch(() => setError('Failed to load subject.'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleComplete = async () => {
    if (!activeTopic || !subject) return;
    setCompleting(true);
    try {
      await subjectService.completeTopic(activeTopic.id);
      // Refresh subject data
      const res = await subjectService.get(subject.id);
      setSubject(res.data);
      const updated = res.data.topics.find((t) => t.id === activeTopic.id);
      if (updated) setActiveTopic(updated);
    } catch {
      // silently ignore
    } finally {
      setCompleting(false);
    }
  };

  if (loading) return <Layout><LoadingSpinner /></Layout>;
  if (error) return <Layout><ErrorMessage message={error} /></Layout>;
  if (!subject) return null;

  return (
    <Layout>
      {/* Back button */}
      <button
        onClick={() => navigate('/subjects')}
        className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-4"
      >
        <ChevronLeft size={16} /> Back to Subjects
      </button>

      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-5">
        <div className="flex items-start gap-4">
          <span className="text-4xl">{subject.icon}</span>
          <div className="flex-1">
            <h1 className="text-xl font-bold text-gray-900">{subject.name}</h1>
            <p className="text-sm text-gray-500 mt-1">{subject.description}</p>
            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>
                  {subject.topics.filter((t) => t.completed).length}/{subject.topics.length} topics completed
                </span>
                <span>{subject.progress_pct}%</span>
              </div>
              <ProgressBar value={subject.progress_pct} showLabel={false} />
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-5">
        {/* Topic list */}
        <div className="w-56 shrink-0">
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 px-1">Topics</h2>
          <div className="space-y-1">
            {subject.topics.map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveTopic(t)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-left transition-colors ${
                  activeTopic?.id === t.id
                    ? 'bg-indigo-50 text-indigo-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {t.completed ? (
                  <CheckCircle2 size={15} className="text-green-500 shrink-0" />
                ) : (
                  <Circle size={15} className="text-gray-300 shrink-0" />
                )}
                <span className="truncate">{t.title}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Topic content */}
        {activeTopic && (
          <div className="flex-1 bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-lg font-bold text-gray-900">{activeTopic.title}</h2>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${difficultyColors[activeTopic.difficulty] || 'bg-gray-100 text-gray-600'}`}>
                {activeTopic.difficulty}
              </span>
            </div>

            {activeTopic.completed && (
              <div className="flex items-center gap-1.5 text-green-600 text-xs mb-4">
                <CheckCircle2 size={14} /> Completed
              </div>
            )}

            {/* Notes rendered as pre-formatted markdown-like content */}
            <div className="prose prose-sm max-w-none mt-4 text-gray-700 text-sm leading-relaxed whitespace-pre-wrap font-sans">
              {activeTopic.notes}
            </div>

            {!activeTopic.completed && (
              <button
                onClick={handleComplete}
                disabled={completing}
                className="mt-6 inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
              >
                <BookOpen size={15} />
                {completing ? 'Marking complete...' : 'Mark as Completed'}
              </button>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}
