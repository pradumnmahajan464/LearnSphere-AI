import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts';
import {
  BookOpen, ClipboardList, TrendingUp, Award, Lightbulb, ArrowRight,
} from 'lucide-react';
import Layout from '../components/Layout';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { dashboardService } from '../services';
import type { DashboardData } from '../types';

function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  color,
}: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  sub?: string;
  color: string;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 flex items-start gap-4">
      <div className={`w-11 h-11 ${color} rounded-lg flex items-center justify-center shrink-0`}>
        <Icon size={20} className="text-white" />
      </div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
      </div>
    </div>
  );
}

const BAR_COLORS = ['#6366f1', '#3b82f6', '#8b5cf6', '#06b6d4'];

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardService
      .get()
      .then((res) => setData(res.data))
      .catch(() => setError('Failed to load dashboard. Please refresh.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout><LoadingSpinner message="Loading dashboard..." /></Layout>;
  if (error) return <Layout><ErrorMessage message={error} /></Layout>;
  if (!data) return null;

  const chartData = data.subject_progress.map((s) => ({
    name: s.name.split(' ')[0],
    progress: s.progress_pct,
  }));

  return (
    <Layout>
      {/* Welcome */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {data.student_name}! 👋
        </h1>
        <p className="text-gray-500 mt-1 text-sm">Here's your learning overview for today.</p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          icon={BookOpen}
          label="Enrolled Subjects"
          value={data.enrolled_subjects}
          color="bg-indigo-500"
        />
        <StatCard
          icon={TrendingUp}
          label="Quiz Average"
          value={`${data.quiz_average_pct}%`}
          sub="across all subjects"
          color="bg-blue-500"
        />
        <StatCard
          icon={Award}
          label="Completed Lessons"
          value={data.completed_lessons}
          sub={`of ${data.total_lessons} total`}
          color="bg-purple-500"
        />
        <StatCard
          icon={ClipboardList}
          label="Quiz Attempts"
          value={data.recent_attempts.length > 0 ? 'Active' : 'None yet'}
          sub="take a quiz to start"
          color="bg-cyan-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Subject progress chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Subject Progress</h2>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                <Tooltip formatter={(v: number) => [`${v}%`, 'Progress']} />
                <Bar dataKey="progress" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, i) => (
                    <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-gray-400 py-8 text-center">No data yet</p>
          )}
        </div>

        {/* Recommendation card */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb size={18} className="text-yellow-500" />
            <h2 className="text-base font-semibold text-gray-900">Next Recommended Topic</h2>
          </div>
          {data.recommended_topic ? (
            <div className="bg-indigo-50 rounded-lg p-4">
              <p className="text-sm font-medium text-indigo-900">{data.recommended_topic}</p>
              <p className="text-xs text-indigo-600 mt-1">Based on your quiz performance</p>
              <Link
                to="/recommendations"
                className="inline-flex items-center gap-1 mt-3 text-xs font-medium text-indigo-600 hover:text-indigo-800"
              >
                View all recommendations <ArrowRight size={12} />
              </Link>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-sm text-gray-400">Take a quiz to get personalised recommendations.</p>
              <Link to="/quizzes" className="text-sm text-indigo-600 font-medium mt-2 inline-block hover:underline">
                Start a quiz →
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Subject progress list */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
        <h2 className="text-base font-semibold text-gray-900 mb-4">Subject-wise Progress</h2>
        <div className="space-y-4">
          {data.subject_progress.map((s) => (
            <div key={s.id}>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-sm font-medium text-gray-800">
                  {s.icon} {s.name}
                </span>
                <span className="text-xs text-gray-500">
                  {s.completed_count}/{s.topic_count} topics
                </span>
              </div>
              <ProgressBar value={s.progress_pct} />
            </div>
          ))}
        </div>
      </div>

      {/* Recent quiz attempts */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-base font-semibold text-gray-900 mb-4">Recent Quiz Results</h2>
        {data.recent_attempts.length === 0 ? (
          <div className="text-center py-8">
            <ClipboardList size={32} className="text-gray-300 mx-auto mb-2" />
            <p className="text-sm text-gray-400">No quiz attempts yet. Take your first quiz!</p>
            <Link to="/quizzes" className="text-sm text-indigo-600 font-medium mt-2 inline-block hover:underline">
              Browse quizzes →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {data.recent_attempts.map((a) => (
              <div key={a.id} className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-800">{a.quiz_title}</p>
                  <p className="text-xs text-gray-500">{a.subject_name}</p>
                </div>
                <div className="text-right">
                  <span className={`text-sm font-bold ${a.accuracy_pct >= 80 ? 'text-green-600' : a.accuracy_pct >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                    {a.accuracy_pct}%
                  </span>
                  <p className="text-xs text-gray-400">{a.score}/{a.total_questions}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
