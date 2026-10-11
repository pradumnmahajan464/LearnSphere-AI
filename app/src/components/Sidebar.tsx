import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, BookOpen, ClipboardList,
  Lightbulb, User, LogOut,
} from 'lucide-react';
import { authService } from '../services';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/subjects', label: 'My Subjects', icon: BookOpen },
  { to: '/quizzes', label: 'Quizzes', icon: ClipboardList },
  { to: '/recommendations', label: 'Recommendations', icon: Lightbulb },
  { to: '/profile', label: 'Profile', icon: User },
];

export default function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <aside className="w-64 min-h-screen bg-indigo-700 flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-indigo-600">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-white rounded-lg flex items-center justify-center">
            <span className="text-indigo-700 font-bold text-lg">L</span>
          </div>
          <div>
            <p className="text-white font-bold text-base leading-tight">LearnSphere</p>
            <p className="text-indigo-200 text-xs">AI Learning Assistant</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-white text-indigo-700'
                  : 'text-indigo-100 hover:bg-indigo-600 hover:text-white'
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="px-3 pb-6">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-indigo-100 hover:bg-indigo-600 hover:text-white transition-colors"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </aside>
  );
}
