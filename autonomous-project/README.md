# Crypto Volume Alert Monitor

A lightweight, no-API-key-required cryptocurrency monitoring tool that detects unusual volume spikes and significant price movements.

## What It Does

This tool monitors configured cryptocurrencies and alerts you when:

- **Volume Spike**: 24h trading volume exceeds the 3-day moving average by your threshold (default: 2x)
- **Price Anomaly**: 24h price change exceeds your threshold (default: 5%)

Uses the free CoinGecko API - no signup or API key required.

## Why This Exists

Built specifically for Dan - someone who:
- Values efficiency and practical automation
- Wants hands-on tools to understand how things work
- Needs reliable data without vendor lock-in
- Cares about identifying market anomalies before the crowd

## Quick Start

```bash
# Run it
python3 crypto_volume_monitor.py

# First run creates config.json - edit to customize
```

## Configuration

Edit `config.json` to customize:

```json
{
  "coins": ["bitcoin", "ethereum", "solana", "cardano"],
  "volume_spike_threshold": 2.0,
  "price_change_threshold": 0.05,
  "data_dir": "./data"
}
```

- `coins`: Coin IDs from CoinGecko (check their /coins/list endpoint)
- `volume_spike_threshold`: Multiplier for volume alert (2.0 = 2x average)
- `price_change_threshold`: Percentage for price alert (0.05 = 5%)

## Output

Console output:
```
COIN            PRICE     24H CHG     VOLUME       MCAP
-----------------------------------------------------------------
BITCOIN    $87,423.50     +2.3%    $45.2B    $1.73T [VOL-2.1x | PUMP]
ETHEREUM    $2,123.45     -1.1%    $12.8B    $255B
SOLANA        $145.22     +7.8%    $3.1B      $68B [VOL-3.2x | PUMP]
```

Alerts are also saved to `data/alerts.json` for integration with other tools.

## Data Persistence

- `data/history.json`: Rolling volume data (last 30 readings per coin)
- `data/alerts.json`: Alert history (last 100 alerts)

## Automation

Run periodically via cron:

```bash
# Every hour
crontab -e
0 * * * * cd /path/to/crypto_volume_monitor && python3 crypto_volume_monitor.py >> /dev/null 2>&1
```

Or use a simple loop for continuous monitoring:

```bash
while true; do
  python3 crypto_volume_monitor.py
  sleep 300  # 5 minutes
done
```

## Extending

Since this is pure Python with standard library only, you can easily extend it:

- Add webhook notifications (Slack/Discord)
- Export to CSV for spreadsheet analysis
- Add technical indicators (RSI, MACD)
- Integrate with trading APIs

## Technical Notes

- CoinGecko free tier: ~50 calls/minute rate limit
- No external dependencies - runs on any Python 3.6+
- Uses stdlib only (`urllib`, `json`, `pathlib`)

## Troubleshooting

**Rate Limited**: You're making too many requests. Wait 60 seconds or reduce coins.

**No Data**: Check coin IDs at https://api.coingecko.com/api/v3/coins/list

**History reset**: If you delete `data/history.json`, baselines will rebuild over time.

## Files

- `crypto_volume_monitor.py` - Main script
- `config.json` - Configuration
- `data/` - Runtime data directory
- `README.md` - This file
