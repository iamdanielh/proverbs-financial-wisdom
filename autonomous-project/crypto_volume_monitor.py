#!/usr/bin/env python3
"""
Crypto Volume Alert Monitor
Detects unusual volume spikes and price movements in cryptocurrency markets.
Uses CoinGecko API (free tier, no API key required).

Built for Dan: analytical, efficiency-focused, hands-on.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error


class CryptoVolumeMonitor:
    COINGECKO_API = "https://api.coingecko.com/api/v3"
    
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.data_dir = Path(self.config.get("data_dir", "./data"))
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.history = self.load_history()
        
    def load_config(self, path):
        defaults = {
            "coins": ["bitcoin", "ethereum", "solana", "cardano"],
            "volume_spike_threshold": 2.0,
            "price_change_threshold": 0.05,
            "data_dir": "./data"
        }
        try:
            with open(path) as f:
                cfg = json.load(f)
                defaults.update(cfg)
                return defaults
        except FileNotFoundError:
            with open(path, 'w') as f:
                json.dump(defaults, f, indent=2)
            print(f"Created config: {path}")
            return defaults
        except:
            return defaults
    
    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def fetch(self, endpoint):
        url = f"{self.COINGECKO_API}/{endpoint}"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "CryptoMonitor/1.0",
                "Accept": "application/json"
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("Error: API rate limit hit. Wait 60 seconds.")
            else:
                print(f"API error: {e.code}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_data(self):
        coins = ",".join(self.config["coins"])
        return self.fetch(
            f"simple/price?ids={coins}&vs_currencies=usd"
            f"&include_24hr_vol=true&include_24hr_change=true"
            f"&include_market_cap=true"
        ) or {}
    
    def check_anomalies(self, coin_id, vol, change):
        hist = self.history.get(coin_id, {}).get("volumes", [])
        vol_spike = False
        vol_ratio = 0
        
        if len(hist) >= 3:
            avg = sum(hist[-3:]) / 3
            if avg > 0:
                vol_ratio = vol / avg
                vol_spike = vol_ratio >= self.config["volume_spike_threshold"]
        
        price_anomaly = abs(change) >= self.config["price_change_threshold"] * 100
        direction = "PUMP" if change > 0 else "DUMP" if price_anomaly else ""
        
        return vol_spike, vol_ratio, price_anomaly, direction
    
    def fmt(self, n):
        if n >= 1e12: return f"{n/1e12:.2f}T"
        if n >= 1e9: return f"{n/1e9:.2f}B"
        if n >= 1e6: return f"{n/1e6:.2f}M"
        return f"{n:,.0f}"
    
    def analyze(self):
        print(f"\n{'='*65}")
        print(f"CRYPTO VOLUME ALERT | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*65}\n")
        print(f"{'COIN':12} {'PRICE':>14} {'24H CHG':>10} {'VOLUME':>12} {'MCAP':>12}")
        print(f"{'-'*65}")
        
        data = self.get_data()
        alerts = []
        
        for coin in self.config["coins"]:
            if coin not in data:
                print(f"{coin:12} <no data>")
                continue
            
            d = data[coin]
            price = d.get("usd", 0)
            vol = d.get("usd_24h_vol", 0)
            chg = d.get("usd_24h_change", 0)
            mcap = d.get("usd_market_cap", 0)
            
            # Update history
            if coin not in self.history:
                self.history[coin] = {"volumes": []}
            self.history[coin]["volumes"].append(vol)
            self.history[coin]["volumes"] = self.history[coin]["volumes"][-30:]
            
            # Check anomalies
            vol_spike, vol_ratio, price_anom, direction = self.check_anomalies(coin, vol, chg)
            
            # Format output
            ps = f"${price:,.2f}" if price > 1 else f"${price:.6f}"
            vs = self.fmt(vol)
            ms = self.fmt(mcap)
            cs = f"{chg:+.1f}%"
            
            # Show alerts inline
            markers = []
            if vol_spike:
                markers.append(f"VOL-{vol_ratio:.1f}x")
            if price_anom:
                markers.append(direction)
            
            marker = f" [{' | '.join(markers)}]" if markers else ""
            print(f"{coin.upper():12} {ps:>14} {cs:>10} {vs:>12} {ms:>12}{marker}")
            
            if vol_spike or price_anom:
                alerts.append({
                    "coin": coin,
                    "time": datetime.now().isoformat(),
                    "price": price,
                    "change_24h": chg,
                    "volume_24h": vol,
                    "volume_spike": vol_spike,
                    "vol_ratio": vol_ratio,
                    "price_anomaly": price_anom,
                    "direction": direction
                })
        
        self.save_history()
        
        print(f"\n{'-'*65}")
        self.save_alerts(alerts)
        return alerts
    
    def save_alerts(self, alerts):
        if not alerts:
            print("No anomalies detected.")
            return
        
        print(f"ALERTS: {len(alerts)} anomalies detected")
        
        alerts_file = self.data_dir / "alerts.json"
        all_alerts = []
        if alerts_file.exists():
            try:
                with open(alerts_file) as f:
                    all_alerts = json.load(f)
            except:
                pass
        
        all_alerts.extend(alerts)
        # Keep last 100 alerts
        all_alerts = all_alerts[-100:]
        
        with open(alerts_file, 'w') as f:
            json.dump(all_alerts, f, indent=2)
        
        print(f"Saved to: {alerts_file}")


def main():
    monitor = CryptoVolumeMonitor()
    try:
        monitor.analyze()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
