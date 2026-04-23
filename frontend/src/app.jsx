import React, { useState, useEffect } from 'react';
import { fetchPortfolioStats, fetchTrades, fetchAdjustments, uploadPDF, addAdjustment, addTrade, clearTrades } from './api';
import MetricsCard from './components/MetricsCard';
import HoldingsTable from './components/HoldingsTable';
import UploadPDF from './components/UploadPDF';
import Adjustments from './components/Adjustments';
import TradeHistory from './components/TradeHistory';

function App() {
  const [stats, setStats] = useState(null);
  const [trades, setTrades] = useState([]);
  const [adjustments, setAdjustments] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsData, tradesData, adjData] = await Promise.all([
        fetchPortfolioStats(),
        fetchTrades(),
        fetchAdjustments()
      ]);
      setStats(statsData);
      setTrades(tradesData);
      setAdjustments(adjData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUpload = async (file) => {
    await uploadPDF(file);
    await loadData();
  };

  const handleAddAdjustment = async (type, amount, date, desc) => {
    await addAdjustment(type, amount, date, desc);
    await loadData();
  };

  const handleAddTrade = async (sec, type, qty, rate, date) => {
    await addTrade(sec, type, qty, rate, date);
    await loadData();
  };

  const handleClearTrades = async () => {
    if (confirm('Delete all trade data? This cannot be undone.')) {
      await clearTrades();
      await loadData();
    }
  };

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Finqalab Portfolio</h1>
      <p className="text-gray-500 mb-6">Live PSX data · FIFO accounting · Broker fees</p>

      {stats?.has_data ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
            <MetricsCard title="Net Capital" value={stats.net_capital} />
            <MetricsCard title="Live Portfolio" value={stats.live_portfolio_value} delta={((stats.live_portfolio_value - stats.net_capital)/stats.net_capital*100).toFixed(1)} />
            <MetricsCard title="Realized P&L" value={stats.realized_pnl} />
            <MetricsCard title="Unrealized P&L" value={stats.unrealized_pnl} />
            <MetricsCard title="Holdings Market Value" value={stats.holdings_market_value} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <HoldingsTable holdings={stats.holdings} />
            <UploadPDF onUpload={handleUpload} />
          </div>

          <div className="mb-6">
            <TradeHistory trades={trades} onAddTrade={handleAddTrade} onClear={handleClearTrades} />
          </div>

          <div className="mb-6">
            <Adjustments adjustments={adjustments} onAddAdjustment={handleAddAdjustment} />
          </div>
        </>
      ) : (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center">
          <p className="text-gray-600 mb-4">No data yet. Upload a Finqalab PDF to start.</p>
          <UploadPDF onUpload={handleUpload} />
        </div>
      )}
    </div>
  );
}

export default App;