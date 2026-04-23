import axios from 'axios';

const api = axios.create({ baseURL: '' }); // relative to same origin

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/upload-pdf', formData);
};

export const fetchPortfolioStats = async () => {
  const res = await api.get('/api/portfolio-stats');
  return res.data;
};

export const fetchTrades = async () => {
  const res = await api.get('/api/trades');
  return res.data;
};

export const fetchAdjustments = async () => {
  const res = await api.get('/api/adjustments');
  return res.data;
};

export const addAdjustment = async (type, amount, date, description) => {
  const params = new URLSearchParams();
  params.append('adj_type', type);
  params.append('amount', amount);
  params.append('date', date);
  params.append('description', description);
  return api.post('/api/add-adjustment', params);
};

export const addTrade = async (security, type, quantity, rate, tradeDate) => {
  const params = new URLSearchParams();
  params.append('security', security);
  params.append('trade_type', type);
  params.append('quantity', quantity);
  params.append('rate', rate);
  params.append('trade_date', tradeDate);
  return api.post('/api/add-trade', params);
};

export const clearTrades = async () => {
  return api.post('/api/clear-trades');
};