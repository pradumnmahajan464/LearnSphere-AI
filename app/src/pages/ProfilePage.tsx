import React, { useEffect, useState } from 'react';
import { User, Mail, Calendar, BookOpen } from 'lucide-react';
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { authService } from '../services';
import type { User as UserType } from '../types';

export default function ProfilePage() {
  const [user, setUser] = useState<UserType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    authService
      .me()
      .then((res) => setUser(res.data))
      .catch(() => setError('Failed to load profile.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Layout title="Profile"><LoadingSpinner /></Layout>;
  if (error) return <Layout title="Profile"><ErrorMessage message={error} /></Layout>;
  if (!user) return null;

  return (
    <Layout title="Profile">
      <div className="max-w-lg">
        {/* Avatar card */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-5">
          <div className="flex items-center gap-5">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-indigo-600">
                {user.name.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">{user.name}</h2>
              <p className="text-sm text-gray-500">{user.email}</p>
            </div>
          </div>
        </div>

        {/* Info card */}
        <div className="bg-white rounded-xl border border-gray-200 divide-y divide-gray-100">
          <div className="flex items-center gap-3 px-5 py-4">
            <User size={16} className="text-gray-400 shrink-0" />
            <div>
              <p className="text-xs text-gray-500">Full Name</p>
              <p className="text-sm font-medium text-gray-900">{user.name}</p>
            </div>
          </div>
          <div className="flex items-center gap-3 px-5 py-4">
            <Mail size={16} className="text-gray-400 shrink-0" />
            <div>
              <p className="text-xs text-gray-500">Email Address</p>
              <p className="text-sm font-medium text-gray-900">{user.email}</p>
            </div>
          </div>
          <div className="flex items-center gap-3 px-5 py-4">
            <Calendar size={16} className="text-gray-400 shrink-0" />
            <div>
              <p className="text-xs text-gray-500">Member Since</p>
              <p className="text-sm font-medium text-gray-900">
                {new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric', month: 'long', day: 'numeric',
                })}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 px-5 py-4">
            <BookOpen size={16} className="text-gray-400 shrink-0" />
            <div>
              <p className="text-xs text-gray-500">Account ID</p>
              <p className="text-sm font-medium text-gray-900">#{user.id}</p>
            </div>
          </div>
        </div>

        <div className="mt-5 bg-indigo-50 border border-indigo-200 rounded-xl p-4 text-xs text-indigo-700">
          <strong>LearnSphere AI</strong> supports UN SDG 4 — Quality Education.
          Your learning data is stored securely and is only accessible to you.
        </div>
      </div>
    </Layout>
  );
}
