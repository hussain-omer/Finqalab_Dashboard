import React, { useState } from 'react';

export default function TradeHistory({ trades, onAddTrade, onClear }) {
  const [sec, setSec] = useState('');
  const [type, setType] = useState('BUY');
  const [qty, setQty] = useState('');
  const [rate, setRate] = useState('');
  const [date, setDate] = useState(new Date().toISOString().slice(0,10));

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!sec || !qty || !rate) return;
    onAddTrade(sec, type, parseFloat(qty), parseFloat(rate), date);
    setSec(''); setQty(''); setRate('');
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <div className="flex justify-between items-center mb-3">
        <h3 className="font-semibold text-gray-800">Trade History</h3>
        <button onClick={onClear} className="text-red-600 text-sm">Clear all trades</button>
      </div>
      <div className="overflow-x-auto max-h-64 mb-4">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th>Date</th><th>Security</th><th>Type</th><th>Qty</th><th>Rate</th><th>Total</th></tr></thead>
          <tbody>
            {trades.slice().reverse().map((t, idx) => (
              <tr key={idx} className="border-t border-gray-100"><td className="px-2 py-1">{t['Trade Date']}</td><td>{t.Security}</td><td>{t.Type}</td><td className="text-right">{t.Quantity}</td><td className="text-right">₨ {t.Rate}</td><td className="text-right">₨ {t.Total.toLocaleString()}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <form onSubmit={handleSubmit} className="grid grid-cols-3 gap-2">
        <input placeholder="Security" value={sec} onChange={(e) => setSec(e.target.value)} className="border rounded p-1 text-sm" />
        <select value={type} onChange={(e) => setType(e.target.value)} className="border rounded p-1 text-sm"><option>BUY</option><option>SELL</option></select>
        <input type="number" step="1" placeholder="Qty" value={qty} onChange={(e) => setQty(e.target.value)} className="border rounded p-1 text-sm" />
        <input type="number" step="0.01" placeholder="Rate" value={rate} onChange={(e) => setRate(e.target.value)} className="border rounded p-1 text-sm" />
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="border rounded p-1 text-sm" />
        <button type="submit" className="bg-primary text-white px-3 py-1 rounded-lg text-sm">Add Trade</button>
      </form>
    </div>
  );
}