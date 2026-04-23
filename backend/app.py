from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime

from utils.pdf_parser import parse_finqalab_pdf
from utils.fifo_pnl import compute_fifo_realized_pnl
from utils.price_fetcher import get_live_prices
from utils.storage import (
    load_cumulative_trades, save_cumulative_trades,
    load_adjustments, save_adjustments, compute_net_capital,
    DEFAULT_INITIAL_CAPITAL
)

app = FastAPI()

# Allow CORS only if needed (but static files are same origin, so not strictly required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- API Endpoints ----------
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        new_trades, extracted_fees = parse_finqalab_pdf(file.file)
        if new_trades.empty:
            raise HTTPException(status_code=400, detail="No trades found in PDF")
        cumulative = load_cumulative_trades()
        updated = pd.concat([cumulative, new_trades], ignore_index=True)
        save_cumulative_trades(updated)
        # Add fees as adjustments
        adj_df = load_adjustments()
        for _, fee in extracted_fees.iterrows():
            new_adj = pd.DataFrame([{
                'Type': 'broker_fee',
                'Amount': fee['Amount'],
                'Date': pd.to_datetime(fee['Date']),
                'Description': fee['Description']
            }])
            adj_df = pd.concat([adj_df, new_adj], ignore_index=True)
        save_adjustments(adj_df)
        return {"status": "ok", "trades_added": len(new_trades), "fees_added": len(extracted_fees)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio-stats")
async def portfolio_stats():
    trades_df = load_cumulative_trades()
    if trades_df.empty:
        return {"has_data": False}
    adjustments_df = load_adjustments()
    net_cap, initial, deposits, withdrawals, broker_fees, other_fees = compute_net_capital(adjustments_df)
    # Calculate holdings and P&L
    buys = trades_df[trades_df['Type'] == 'BUY']
    sells = trades_df[trades_df['Type'] == 'SELL']
    holdings_net = buys.groupby('Security')['Quantity'].sum().sub(sells.groupby('Security')['Quantity'].sum(), fill_value=0)
    holdings_net = holdings_net[holdings_net > 0]
    tickers_needed = list(holdings_net.index)
    live_prices = get_live_prices(tickers_needed)
    # FIFO realized
    _, _, total_realized = compute_fifo_realized_pnl(trades_df)
    # Unrealized
    unrealized_total = 0.0
    holdings_list = []
    for sec, qty in holdings_net.items():
        buys_sec = buys[buys['Security'] == sec]
        total_cost = (buys_sec['Quantity'] * buys_sec['Rate']).sum()
        avg_cost = total_cost / qty if qty > 0 else 0
        current_price = live_prices.get(sec, avg_cost)
        market_val = qty * current_price
        cost_val = qty * avg_cost
        unrealized = market_val - cost_val
        unrealized_total += unrealized
        holdings_list.append({
            'Security': sec,
            'Shares': qty,
            'Avg Cost': avg_cost,
            'Current Price': current_price,
            'Market Value': market_val,
            'Cost Basis Value': cost_val,
            'Unrealized P&L': unrealized,
            'Unrealized %': (unrealized / cost_val * 100) if cost_val != 0 else 0
        })
    live_portfolio_value = net_cap + total_realized + unrealized_total
    holdings_market_value = sum(h['Market Value'] for h in holdings_list)
    return {
        "has_data": True,
        "net_capital": net_cap,
        "live_portfolio_value": live_portfolio_value,
        "realized_pnl": total_realized,
        "unrealized_pnl": unrealized_total,
        "holdings_market_value": holdings_market_value,
        "holdings": holdings_list,
        "initial_capital": initial,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "broker_fees": broker_fees,
        "other_fees": other_fees
    }

@app.get("/api/trades")
async def get_trades():
    df = load_cumulative_trades()
    return df.to_dict(orient='records')

@app.get("/api/adjustments")
async def get_adjustments():
    df = load_adjustments()
    df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")
    return df.to_dict(orient='records')

@app.post("/api/add-adjustment")
async def add_adjustment(adj_type: str, amount: float, date: str, description: str = ""):
    df = load_adjustments()
    new_row = pd.DataFrame([{
        'Type': adj_type,
        'Amount': amount,
        'Date': pd.to_datetime(date),
        'Description': description
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_adjustments(df)
    return {"status": "ok"}

@app.post("/api/add-trade")
async def add_trade(security: str, trade_type: str, quantity: float, rate: float, trade_date: str):
    df = load_cumulative_trades()
    new_row = pd.DataFrame([{
        'Security': security.upper(),
        'Type': trade_type,
        'Quantity': quantity,
        'Rate': rate,
        'Total': quantity * rate,
        'Trade Date': trade_date,
        'Upload Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_cumulative_trades(df)
    return {"status": "ok"}

@app.post("/api/clear-trades")
async def clear_trades():
    empty = pd.DataFrame(columns=['Security', 'Type', 'Quantity', 'Rate', 'Total', 'Trade Date', 'Upload Date'])
    save_cumulative_trades(empty)
    return {"status": "ok"}

# ---------- Serve static frontend ----------
static_dir = "/app/static"
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))