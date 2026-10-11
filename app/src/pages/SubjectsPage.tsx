import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, ChevronRight } from 'lucide-react';
import Layout from '../components/Layout';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { subjectService } from '../services';
import type { SubjectListItem } from '../types';

const difficultyColors: Record<string, string> = {
  Beginner: 'bg-green-100 text-green-700',
  Intermediate: 'bg-yellow-100 text-yellow-700',
  Advanced: 'bg-red-100 text-red-700',
};

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState<SubjectListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    subjectService
      .list()
      .then((res) => setSubjects(res.data))
      .catch(() => setError('Failed to load subjects.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout title="My Subjects"><LoadingSpinner /></Layout>;
  if (error) return <Layout title="My Subjects"><ErrorMessage message={error} /></Layout>;

  return (
    <Layout title="My Subjects">
      <p className="text-sm text-gray-500 -mt-4 mb-6">
        Explore learning materials and track your topic completion.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {subjects.map((s) => (
          <Link
            key={s.id}
            to={`/subjects/${s.id}`}
            className="bg-white rounded-xl border border-gray-200 p-5 hover:border-indigo-300 hover:shadow-sm transition-all block"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{s.icon}</span>
                <div>
                  <h3 className="text-base font-semibold text-gray-900">{s.name}</h3>
                  <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{s.description}</p>
                </div>
              </div>
              <ChevronRight size={16} className="text-gray-400 mt-1 shrink-0" />
            </div>
            <div className="mt-4">
              <div className="flex justify-between text-xs text-gray-500 mb-1.5">
                <span>{s.completed_count}/{s.topic_count} topics completed</span>
                <span>{s.progress_pct}%</span>
              </div>
              <ProgressBar value={s.progress_pct} />
            </div>
          </Link>
        ))}
      </div>
    </Layout>
  );
}

// Unused but exported to satisfy import consistency
export { difficultyColors };
