# =============================================================================
# |                                                                           |
# |                             DISCLAIMER                                    |
# |                                                                           |
# =============================================================================
# |                                                                           |
# | This script is for educational and informational purposes only. It is     |
# | NOT financial advice. Stock market investing involves significant risk,   |
# | including the potential loss of principal.                                |
# |                                                                           |
# | This script scrapes data from Screener.in. Website structures change,     |
# | which may break the script. Always verify data from multiple sources.     |
# | Past performance is not indicative of future results.                     |
# =============================================================================

import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
from io import StringIO
import time
import warnings
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import os

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def get_nifty500_stocks():
    """
    Fetches the list of Nifty 500 stock symbols from the official NSE archives.
    If it fails, it uses a reliable, recently updated hardcoded list as a fallback.
    """
    try:
        url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        nifty500_df = pd.read_csv(csv_data)
        # DEFINITIVE FIX: Ensure all symbols are read and treated as strings from the source.
        symbols = nifty500_df['Symbol'].astype(str).tolist()
        nifty_500_stocks = [symbol + ".NS" for symbol in symbols]
        print("Successfully fetched the latest Nifty 500 stock list from NSE Archives.")
        return nifty_500_stocks
    except Exception as e:
        print(f"Error fetching Nifty 100 list from official source: {e}")
        print("Falling back to a hardcoded list.")
        # Fallback to a comprehensive, hardcoded list
        nifty_500_stocks = [
            '360ONE.NS', '3MINDIA.NS', 'ABB.NS', 'ACC.NS', 'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ABBOTINDIA.NS',
            'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 'ADANITRANS.NS', 'ABCAPITAL.NS', 'ABFRL.NS',
            'AEGISCHEM.NS', 'AFFLE.NS', 'AJANTPHARM.NS', 'APLLTD.NS', 'ALKEM.NS', 'ALKYLAMINE.NS', 'AMARAJABAT.NS', 'AMBER.NS', 'AMBUJACEM.NS',
            'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUROPHARMA.NS',
            'AVANTIFEED.NS', 'DMART.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BALKRISIND.NS',
            'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 'BATAINDIA.NS', 'BAYERCROP.NS', 'BERGEPAINT.NS',
            'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BIOCON.NS', 'BIRLACORPN.NS', 'BSOFT.NS', 'BLUEDART.NS',
            'BOSCHLTD.NS', 'BRITANNIA.NS', 'CESC.NS', 'CADILAHC.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CASTROLIND.NS', 'CEATLTD.NS',
            'CENTURYPLY.NS', 'CENTURYTEX.NS', 'CERA.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOLAFIN.NS', 'CIPLA.NS',
            'CUB.NS', 'COALINDIA.NS', 'COCHINSHIP.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CREDITACC.NS', 'CRISIL.NS',
            'CROMPTON.NS', 'CUMMINSIND.NS', 'CYIENT.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DEVYANI.NS',
            'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'ECLERX.NS', 'EDELWEISS.NS', 'EICHERMOT.NS', 'EIDPARRY.NS', 'EIHOTEL.NS',
            'ENDURANCE.NS', 'ENGINERSIN.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FDC.NS', 'FEDERALBNK.NS', 'FACT.NS', 'FINCABLES.NS', 'FINPIPE.NS',
            'FORTIS.NS', 'GAIL.NS', 'GMRINFRA.NS', 'GALAXYSURF.NS', 'GARFIBRES.NS', 'GODFRYPHLP.NS', 'GODREJAGRO.NS', 'GODREJCP.NS',
            'GODREJIND.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GESHIP.NS', 'GSFC.NS', 'GSPL.NS', 'GUJALKALI.NS',
            'GUJGASLTD.NS', 'GNFC.NS', 'GPPL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEG.NS',
            'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HONAUT.NS',
            'HUDCO.NS', 'IBULHSGFIN.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDBI.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IFBIND.NS',
            'INDIAGLYCO.NS', 'INDIAMART.NS', 'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS',
            'NAUKRI.NS', 'INFY.NS', 'IOB.NS', 'IPCALAB.NS', 'IRB.NS', 'IRCON.NS', 'ITC.NS', 'JSL.NS', 'JKCEMENT.NS', 'JKLAKSHMI.NS',
            'JKPAPER.NS', 'JMFINANCIL.NS', 'JSWENERGY.NS', 'JSWSTEEL.NS', 'JUBILANT.NS', 'JUBLFOOD.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS',
            'KPRMILL.NS', 'KEI.NS', 'KNRCON.NS', 'KRBL.NS', 'KAJARIACER.NS', 'KALPATPOWR.NS', 'KALYANKJIL.NS', 'KEC.NS', 'KOTAKBANK.NS',
            'L&TFH.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LAURUSLABS.NS', 'LAXMIMACH.NS', 'LICHSGFIN.NS', 'LICI.NS', 'LUPIN.NS', 'MRF.NS',
            'MGL.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MARICO.NS', 'MARUTI.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS',
            'MEDANTA.NS', 'METROBRAND.NS', 'METROPOLIS.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NATCOPHARM.NS',
            'NBCC.NS', 'NCC.NS', 'NESCO.NS', 'NESTLEIND.NS', 'NAM-INDIA.NS', 'NHPC.NS', 'NLCINDIA.NS', 'NMDC.NS', 'NOCIL.NS', 'NTPC.NS',
            'OBEROIRLTY.NS', 'ONGC.NS', 'OFSS.NS', 'ORIENTELEC.NS', 'PAGEIND.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFIZER.NS',
            'PHOENIXLTD.NS', 'PIDILITIND.NS', 'PEL.NS', 'POLYMED.NS', 'POONAWALLA.NS', 'PFC.NS', 'POWERGRID.NS', 'PRAJIND.NS',
            'PRESTIGE.NS', 'PRINCEPIPE.NS', 'PRSMJOHNSN.NS', 'PNB.NS', 'QUESS.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RITES.NS', 'RADICO.NS',
            'RAJESHEXPO.NS', 'RALLIS.NS', 'RCF.NS', 'RATNAMANI.NS', 'REDINGTON.NS', 'RELAXO.NS', 'RELIANCE.NS', 'RVNL.NS', 'SAIL.NS',
            'SANOFI.NS', 'SCHAEFFLER.NS', 'SFL.NS', 'SHREECEM.NS', 'SRF.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SOBHA.NS', 'SOLARINDS.NS',
            'SONACOMS.NS', 'SONATSOFTW.NS', 'SBIN.NS', 'SBICARD.NS', 'SBILIFE.NS', 'STARHEALTH.NS', 'SJVN.NS', 'SKFINDIA.NS',
            'SUNDARMFIN.NS', 'SUNDRMFAST.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SUPREMEIND.NS', 'SUZLON.NS', 'SYMPHONY.NS', 'SYNGENE.NS',
            'TTKPRESTIG.NS', 'TV18BRDCST.NS', 'TVSMOTOR.NS', 'TANLA.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TCS.NS', 'TATACONSUM.NS',
            'TATAELXSI.NS', 'TATAINVEST.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'RAMCOCEM.NS', 'THERMAX.NS',
            'TIMKEN.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TRENT.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TIINDIA.NS', 'UCOBANK.NS',
            'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UBL.NS', 'UPL.NS', 'UTIAMC.NS', 'VGUARD.NS', 'VMART.NS', 'VARROC.NS', 'VTL.NS', 'VEDL.NS',
            'VENKEYS.NS', 'VIJAYA.NS', 'VOLTAS.NS', 'WELCORP.NS', 'WELSPUNIND.NS', 'WHIRLPOOL.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZEEL.NS',
            'ZENSARTECH.NS', 'ZOMATO.NS', 'ZYDUSLIFE.NS'
        ]
        return nifty_500_stocks

def get_screener_data(stock_symbol):
    """
    Scrapes key financial data and ratios for a stock from Screener.in.
    Returns a dictionary of the scraped data.
    """
    try:
        # DEFINITIVE FIX: Ensure symbol is a string before manipulation to prevent errors.
        screener_symbol = str(stock_symbol).replace(".NS", "")
        url = f"https://www.screener.in/company/{screener_symbol}/"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {}

        # --- Extract key ratios from the top ratio list ---
        for li in soup.select("#top-ratios > li"):
            name = li.select_one(".name").text.strip()
            value_span = li.select_one(".value > span")
            if value_span:
                value_text = value_span.text.strip().replace(",", "")
                # Use regex to find the first valid number (handles 'Cr.' etc.)
                numeric_part = re.search(r"[-+]?\d*\.\d+|\d+", value_text)
                if numeric_part:
                    data[name] = float(numeric_part.group())

        # --- Extract data from the quarterly results table ---
        quarterly_table = soup.select_one("#quarters")
        if quarterly_table:
            # Sales Growth
            sales_row = quarterly_table.select_one("tbody > tr:nth-of-type(1)")
            if sales_row and len(sales_row.select("td")) > 3:
                latest_sales = float(sales_row.select("td")[-2].text.strip().replace(",", "") or 0)
                yoy_sales = float(sales_row.select("td")[-3].text.strip().replace(",", "") or 0)
                data['YOY Quarterly Sales Growth'] = ((latest_sales - yoy_sales) / abs(yoy_sales)) * 100 if yoy_sales != 0 else 0

            # Net Profit Growth - ROBUST FIX
            profit_row_header = quarterly_table.find("td", text=re.compile(r"^\s*Net Profit\s*$"))
            if profit_row_header:
                profit_row = profit_row_header.parent
                if profit_row and len(profit_row.select("td")) > 3:
                    latest_profit = float(profit_row.select("td")[-2].text.strip().replace(",", "") or 0)
                    yoy_profit = float(profit_row.select("td")[-3].text.strip().replace(",", "") or 0)

                    if yoy_profit > 0:
                        data['YOY Quarterly Profit Growth'] = ((latest_profit - yoy_profit) / yoy_profit) * 100
                    elif latest_profit > 0 and yoy_profit <= 0:
                        data['YOY Quarterly Profit Growth'] = 100.0
                    else:
                        data['YOY Quarterly Profit Growth'] = -100.0

        # --- Extract Piotroski Score (often in its own section) ---
        piotroski_tag = soup.find("span", text=re.compile(r"Piotroski score"))
        if piotroski_tag:
            data['Piotroski score'] = int(piotroski_tag.find_next_sibling("span").text.strip())

        return data

    except Exception as e:
        print(f"     - Could not scrape data for {stock_symbol}: {e}")
        return None

def calculate_quantamental_score(screener_data, stock_data):
    """
    Calculates a score based on multiple criteria. Instead of a strict pass/fail,
    this function returns a score based on how many criteria are met.
    """
    score = 0
    passed_criteria = []

    # --- Criterion 1: Market Cap ---
    if screener_data.get('Market Cap', 0) > 500:
        score += 1
        passed_criteria.append(f"Market Cap: {screener_data.get('Market Cap', 0):.2f} Cr")

    # --- Criterion 2: Sales Growth ---
    if screener_data.get('YOY Quarterly Sales Growth', 0) >= 12:
        score += 1
        passed_criteria.append(f"Qtr Sales Growth: {screener_data.get('YOY Quarterly Sales Growth', 0):.2f}%")

    # --- Criterion 3: Profit Growth ---
    if screener_data.get('YOY Quarterly Profit Growth', 0) >= 12:
        score += 1
        passed_criteria.append(f"Qtr Profit Growth: {screener_data.get('YOY Quarterly Profit Growth', 0):.2f}%")

    # --- Criterion 4: Piotroski Score ---
    if screener_data.get('Piotroski score', 0) > 5:
        score += 1
        passed_criteria.append(f"Piotroski Score: {screener_data.get('Piotroski score', 0)}")

    # --- Criterion 5: Debt to Equity ---
    if screener_data.get('Debt to equity', float('inf')) < 2.0:
        score += 1
        passed_criteria.append(f"D/E Ratio: {screener_data.get('Debt to equity', 0)}")

    # --- Criterion 6: ROCE ---
    if screener_data.get('ROCE', 0) > 10:
        score += 1
        passed_criteria.append(f"ROCE: {screener_data.get('ROCE', 0)}%")

    # --- Criterion 7: P/E Ratio ---
    if 0 < screener_data.get('Stock P/E', float('inf')) < 70:
        score += 1
        passed_criteria.append(f"P/E Ratio: {screener_data.get('Stock P/E', 0)}")

    # --- Criterion 8: Momentum (Price near 52W High) ---
    try:
        # Use the correct key 'High / Low' which is scraped from the site
        high_52w = screener_data.get('High / Low')
        current_price = screener_data.get('Current Price')
        if high_52w and current_price:
            percent_from_high = ((high_52w - current_price) / high_52w) * 100
            if percent_from_high <= 35:
                score += 1
                passed_criteria.append(f"Price near 52W High ({percent_from_high:.2f}% off)")
    except (KeyError, TypeError):
        pass

    # --- Criterion 9: Momentum (RSI) ---
    try:
        stock_data.ta.rsi(append=True)
        rsi = stock_data['RSI_14'].iloc[-1]
        if not pd.isna(rsi) and rsi > 45:
            score += 1
            passed_criteria.append(f"RSI: {rsi:.2f}")
    except (KeyError, TypeError, IndexError):
        pass

    return score, passed_criteria


def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat using the bot API.
    """
    if not bot_token or not chat_id or "YOUR_BOT_TOKEN" in bot_token:
        print("⚠️ Telegram BOT_TOKEN or CHAT_ID not set. Skipping message.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    max_length = 4096
    chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]

    for chunk in chunks:
        payload = {'chat_id': chat_id, 'text': chunk, 'parse_mode': 'Markdown'}
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("Telegram message chunk sent successfully!")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")

def main():
    """
    Main function to run the stock analysis and send recommendations.
    """
    # Load credentials securely from environment variables
    BOT_TOKEN = "<YOUR BOT TOEN>"
    CHAT_ID = "<YOUR CHAT ID>"

    # Set the minimum score to be considered a candidate
    SCORE_THRESHOLD = 6 # Out of a possible 9 points
    MAX_STOCKS_TO_REPORT = 15 # Limit the number of stocks in the final report

    candidate_stocks = []
    nifty_500_stocks = get_nifty500_stocks()
    total_stocks = len(nifty_500_stocks)

    print(f"\nStarting Quant-amental Scoring for {total_stocks} stocks...")
    print(f"A stock needs a score of at least {SCORE_THRESHOLD}/9 to be considered.")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    for i, stock_symbol in enumerate(nifty_500_stocks):
        print(f"\n({i+1}/{total_stocks}) Analyzing {stock_symbol}...")
        try:
            # Step 1: Scrape fundamental data
            screener_data = get_screener_data(stock_symbol)
            if screener_data is None:
                continue

            # Step 2: Download historical data for technicals
            # DEFINITIVE FIX: Use yf.Ticker().history() for stability and to avoid MultiIndex errors.
            ticker = yf.Ticker(stock_symbol)
            stock_data = ticker.history(start=start_date, end=end_date, auto_adjust=True)

            if stock_data.empty or len(stock_data) < 240:
                print(f"     - Skipping {stock_symbol}: Insufficient historical price data.")
                continue

            # Step 3: Calculate the score using the new scoring function
            score, reasons = calculate_quantamental_score(screener_data, stock_data)
            print(f"     - Score for {stock_symbol}: {score}/9")

            if score >= SCORE_THRESHOLD:
                last_price = screener_data.get('Current Price', 0)
                # Calculate target price based on 1:2 Risk-Reward Ratio
                stop_loss_price = last_price * 0.92 # 8% stop loss
                target_price = last_price * 1.16   # 16% target (2 * 8%)

                print(f"     ✅ ADDED: {stock_symbol} is a potential candidate with score {score}.")
                candidate_stocks.append({
                    "symbol": stock_symbol,
                    "price": f"{last_price:.2f}",
                    "stop_loss": f"{stop_loss_price:.2f}",
                    "target": f"{target_price:.2f}",
                    "time_horizon": "90-180 days",
                    "criteria": reasons,
                    "score": score
                })

            time.sleep(1.5) # Be respectful to the API

        except Exception as e:
            print(f"     - MAJOR ERROR processing {stock_symbol}: {e}")

    # --- Sort by Score and Prepare Telegram Message ---
    candidate_stocks.sort(key=lambda x: x['score'], reverse=True)

    # Limit the number of stocks in the report
    top_candidate_stocks = candidate_stocks[:MAX_STOCKS_TO_REPORT]

    if top_candidate_stocks:
        message = f"🚀 *Top {len(top_candidate_stocks)} Quant-amental Stock Candidates* 🚀\n\n"
        message += f"Found {len(candidate_stocks)} stocks with a score of *{SCORE_THRESHOLD}/9* or higher in nifty 500. Showing the top {len(top_candidate_stocks)}.\n\n"
        for stock in top_candidate_stocks:
            message += f"*{stock['symbol']}* (Score: {stock['score']}/9)\n"
            message += f"  - *Price:* ₹{stock['price']}\n"
            message += f"  - *Target:* ₹{stock['target']} (Time: {stock['time_horizon']})\n"
            message += f"  - *Stop Loss (8%):* ₹{stock['stop_loss']}\n"
            message += f"  - *Passed Criteria:* {'; '.join(stock['criteria'])}\n\n"
    else:
        message = f"No stocks met the minimum score of {SCORE_THRESHOLD}/9 today."

    disclaimer = (
        "\n\n*Disclaimer: This is an automated analysis for educational purposes and is NOT financial advice. "
        "Stock market investments are subject to market risks. No strategy guarantees returns. "
        "Data may be inaccurate. Always do your own research.*"
    )
    message += disclaimer

    print("\n--- FINAL REPORT ---")
    print(message)
    send_telegram_message(BOT_TOKEN, CHAT_ID, message)

if __name__ == "__main__":
    main()
