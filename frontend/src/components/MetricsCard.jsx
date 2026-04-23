import React from 'react';

export default function MetricsCard({ title, value, delta }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition">
      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</h3>
      <p className="text-2xl font-mono font-semibold text-gray-900 mt-1">₨ {value?.toLocaleString()}</p>
      {delta !== undefined && (
        <p className={`text-sm mt-1 ${parseFloat(delta) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {delta}% vs net capital
        </p>
      )}
    </div>
  );
}