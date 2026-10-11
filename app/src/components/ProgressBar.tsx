import React from 'react';

interface Props {
  value: number; // 0–100
  color?: 'indigo' | 'green' | 'yellow' | 'red';
  size?: 'sm' | 'md';
  showLabel?: boolean;
}

const colorMap = {
  indigo: 'bg-indigo-500',
  green: 'bg-green-500',
  yellow: 'bg-yellow-400',
  red: 'bg-red-500',
};

export default function ProgressBar({ value, color = 'indigo', size = 'md', showLabel = false }: Props) {
  const h = size === 'sm' ? 'h-1.5' : 'h-2.5';
  const pct = Math.min(100, Math.max(0, value));
  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Progress</span>
          <span>{pct}%</span>
        </div>
      )}
      <div className={`w-full bg-gray-200 rounded-full ${h}`}>
        <div
          className={`${colorMap[color]} ${h} rounded-full transition-all duration-300`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
