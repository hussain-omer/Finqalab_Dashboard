import pandas as pd

def compute_fifo_realized_pnl(trades_df):
    trades_df = trades_df.sort_values('Trade Date').copy()
    realized = {}
    remaining_lots = {}
    for _, row in trades_df.iterrows():
        sec = row['Security']
        typ = row['Type']
        qty = row['Quantity']
        rate = row['Rate']
        if typ == 'BUY':
            if sec not in remaining_lots:
                remaining_lots[sec] = []
            remaining_lots[sec].append([qty, rate])
        else:
            if sec not in remaining_lots:
                continue
            sell_qty = qty
            sell_rate = rate
            profit = 0.0
            lots = remaining_lots[sec]
            while sell_qty > 0 and lots:
                lot_qty, lot_rate = lots[0]
                take = min(lot_qty, sell_qty)
                profit += take * (sell_rate - lot_rate)
                sell_qty -= take
                lot_qty -= take
                if lot_qty == 0:
                    lots.pop(0)
                else:
                    lots[0][0] = lot_qty
            realized[sec] = realized.get(sec, 0.0) + profit
    total_realized = sum(realized.values())
    return realized, remaining_lots, total_realized