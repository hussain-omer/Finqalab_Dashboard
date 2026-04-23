import React, { useState } from 'react';

export default function Adjustments({ adjustments, onAddAdjustment }) {
  const [type, setType] = useState('deposit');
  const [amount, setAmount] = useState('');
  const [date, setDate] = useState(new Date().toISOString().slice(0,10));
  const [desc, setDesc] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;
    onAddAdjustment(type, parseFloat(amount), date, desc);
    setAmount('');
    setDesc('');
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h3 className="font-semibold text-gray-800 mb-3">Fees & Adjustments</h3>
      <div className="overflow-x-auto mb-4">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50">
            <tr><th className="px-2 py-1 text-left">Date</th><th className="px-2 py-1 text-left">Type</th><th className="px-2 py-1 text-right">Amount</th><th className="px-2 py-1 text-left">Description</th></tr>
          </thead>
          <tbody>
            {adjustments.map((a, idx) => (
              <tr key={idx} className="border-t border-gray-100">
                <td className="px-2 py-1">{a.Date}</td>
                <td className="px-2 py-1">{a.Type}</td>
                <td className="px-2 py-1 text-right">₨ {a.Amount.toLocaleString()}</td>
                <td className="px-2 py-1">{a.Description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-2">
        <select value={type} onChange={(e) => setType(e.target.value)} className="border rounded p-1 text-sm">
          <option value="deposit">Deposit</option><option value="withdrawal">Withdrawal</option>
          <option value="broker_fee">Broker fee</option><option value="other_fee">Other fee</option>
        </select>
        <input type="number" step="100" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} className="border rounded p-1 text-sm" />
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="border rounded p-1 text-sm" />
        <input placeholder="Description" value={desc} onChange={(e) => setDesc(e.target.value)} className="border rounded p-1 text-sm" />
        <button type="submit" className="bg-primary text-white px-3 py-1 rounded-lg text-sm col-span-2">Add Adjustment</button>
      </form>
    </div>
  );
}