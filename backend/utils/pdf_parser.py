import pdfplumber
import re
import pandas as pd
from datetime import datetime

def parse_finqalab_pdf(pdf_file):
    trades = []
    fees = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            for line in lines:
                if 'BUY' not in line and 'SELL' not in line:
                    continue
                # Security
                sec_match = re.match(r'^([A-Z]{2,5})', line.strip())
                if not sec_match:
                    words = line.split()
                    for w in words:
                        if w.isalpha() and w not in ['BUY', 'SELL'] and len(w) >= 2:
                            security = w
                            break
                    else:
                        continue
                else:
                    security = sec_match.group(1)
                # Type
                type_match = re.search(r'\b(BUY|SELL)\b', line)
                if not type_match:
                    continue
                trade_type = type_match.group(1)
                # Numbers after type
                pos = type_match.start()
                after_text = line[pos:]
                after_nums = re.findall(r'[\d,]+\.?\d*', after_text)
                after_nums_clean = [float(x.replace(',', '')) for x in after_nums]
                if len(after_nums_clean) >= 3:
                    rate = after_nums_clean[0]
                    qty = after_nums_clean[1]
                    total = after_nums_clean[2]
                else:
                    all_nums = re.findall(r'[\d,]+\.?\d*', line)
                    all_clean = [float(x.replace(',', '')) for x in all_nums]
                    if len(all_clean) >= 3:
                        rate = all_clean[-3]
                        qty = all_clean[-2]
                        total = all_clean[-1]
                    else:
                        continue
                # Broker fee
                broker = 0.0
                broker_match = re.search(r'Broker\s+Total[\s:]*([\d,]+\.?\d*)', line, re.IGNORECASE)
                if not broker_match:
                    broker_match = re.search(r'Broker[\s:]*([\d,]+\.?\d*)', line, re.IGNORECASE)
                if broker_match:
                    try:
                        broker = float(broker_match.group(1).replace(',', ''))
                    except:
                        pass
                # Date
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                trade_date = date_match.group(1) if date_match else None
                trades.append({
                    'Security': security,
                    'Type': trade_type,
                    'Quantity': qty,
                    'Rate': rate,
                    'Total': total,
                    'Trade Date': trade_date,
                    'Upload Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                if broker > 0:
                    fees.append({
                        'Date': trade_date,
                        'Amount': broker,
                        'Description': f'Broker fee for {security} {trade_type}'
                    })
    return pd.DataFrame(trades), pd.DataFrame(fees)