# Quantamental Stock Screener 📈

This Python-based tool analyzes Nifty 500 stocks using a hybrid of quantitative (technical indicators) and fundamental (financial ratios) analysis. It scrapes data from Screener.in and Yahoo Finance, assigns a score based on predefined rules, and sends Telegram alerts for top candidates.

## Features
- Scrapes Nifty 500 stocks list from NSE
- Fundamental data from Screener.in (e.g., ROCE, PE, D/E, Piotroski)
- Technical indicator: RSI
- Quantamental score calculation (9-point scale)
- Sends results to Telegram channel
- Auto-adjusted Yahoo Finance historical price retrieval

## Usage
```bash
pip install -r requirements.txt
python main.py
```

Set your Telegram credentials (BOT TOKEN & CHAT ID) in environment variables or directly in the script.

## Disclaimer
This tool is for educational purposes only. It is **NOT** financial advice.
