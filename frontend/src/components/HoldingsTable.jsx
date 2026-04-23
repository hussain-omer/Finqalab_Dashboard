import React from 'react';

export default function HoldingsTable({ holdings }) {
  if (!holdings || holdings.length === 0) return <div className="bg-white p-4 rounded-xl">No holdings</div>;
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left">Security</th>
            <th className="px-4 py-2 text-right">Shares</th>
            <th className="px-4 py-2 text-right">Avg Cost</th>
            <th className="px-4 py-2 text-right">Current Price</th>
            <th className="px-4 py-2 text-right">Market Value</th>
            <th className="px-4 py-2 text-right">Unrealized P&L</th>
            <th className="px-4 py-2 text-right">Unrealized %</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map(h => (
            <tr key={h.Security} className="border-t border-gray-100 hover:bg-gray-50">
              <td className="px-4 py-2 font-medium">{h.Security}</td>
              <td className="px-4 py-2 text-right">{h.Shares}</td>
              <td className="px-4 py-2 text-right">₨ {h['Avg Cost'].toFixed(2)}</td>
              <td className="px-4 py-2 text-right">₨ {h['Current Price'].toFixed(2)}</td>
              <td className="px-4 py-2 text-right">₨ {h['Market Value'].toLocaleString()}</td>
              <td className={`px-4 py-2 text-right ${h['Unrealized P&L'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ₨ {h['Unrealized P&L'].toLocaleString()}
              </td>
              <td className="px-4 py-2 text-right">{h['Unrealized %'].toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}