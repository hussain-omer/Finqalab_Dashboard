import os
import pandas as pd
from datetime import datetime

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)
CUMULATIVE_CSV = os.path.join(DATA_DIR, "cumulative_trades.csv")
ADJUSTMENTS_CSV = os.path.join(DATA_DIR, "adjustments.csv")
DEFAULT_INITIAL_CAPITAL = 1_102_000

def load_cumulative_trades():
    if os.path.exists(CUMULATIVE_CSV):
        return pd.read_csv(CUMULATIVE_CSV)
    else:
        return pd.DataFrame(columns=['Security', 'Type', 'Quantity', 'Rate', 'Total', 'Trade Date', 'Upload Date'])

def save_cumulative_trades(df):
    df.to_csv(CUMULATIVE_CSV, index=False)

def load_adjustments():
    if os.path.exists(ADJUSTMENTS_CSV):
        df = pd.read_csv(ADJUSTMENTS_CSV)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        return pd.DataFrame([{
            'Type': 'initial',
            'Amount': DEFAULT_INITIAL_CAPITAL,
            'Date': datetime.now(),
            'Description': 'Initial Capital'
        }])

def save_adjustments(df):
    df_out = df.copy()
    if 'Date' in df_out:
        df_out['Date'] = df_out['Date'].dt.strftime("%Y-%m-%d")
    df_out.to_csv(ADJUSTMENTS_CSV, index=False)

def compute_net_capital(adjustments_df):
    initial = adjustments_df[adjustments_df['Type'] == 'initial']['Amount'].sum()
    deposits = adjustments_df[adjustments_df['Type'] == 'deposit']['Amount'].sum()
    withdrawals = adjustments_df[adjustments_df['Type'] == 'withdrawal']['Amount'].sum()
    broker_fees = adjustments_df[adjustments_df['Type'] == 'broker_fee']['Amount'].sum()
    other_fees = adjustments_df[adjustments_df['Type'] == 'other_fee']['Amount'].sum()
    net_capital = initial + deposits - withdrawals - broker_fees - other_fees
    return net_capital, initial, deposits, withdrawals, broker_fees, other_fees