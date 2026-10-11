import React from 'react';
import { AlertCircle } from 'lucide-react';

interface Props {
  message: string;
}

export default function ErrorMessage({ message }: Props) {
  return (
    <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
      <AlertCircle size={16} className="mt-0.5 shrink-0" />
      <span>{message}</span>
    </div>
  );
}
