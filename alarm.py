#alarm.py

import sys
from threading import Thread
import winsound
import os
import requests
from datetime import datetime
from humanize_browsing import run_chrome_pipeline

ALERT_BOT_TOKEN = os.getenv("ALERT_BOT_TOKEN", "YOUR_PERSONAL_BOT_TOKEN")       
MY_PERSONAL_CHAT_ID = os.getenv("MY_PERSONAL_CHAT_ID", "YOUR_PERSONAL_CHAT_ID")    


# ==========================================
# WINDOWS HIGH-INTENSITY ALARM MODULE (SIMULTANEOUS MODE)
# ==========================================
def trigger_drop_alarm(row=None):
    chrome_exe = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    
    # 1. IMMEDIATE BACKGROUND AUDIO THREAD
    def play_beeps():
        try:
            if sys.platform == "win32":
                for _ in range(100): winsound.Beep(2500, 500)
        except Exception as e: print(f"Could not trigger audio: {e}")
    
    print("🚨 [Simultaneous Trigger] Launching Audio Engine...")
    Thread(target=play_beeps, daemon=True).start()

    # 2. IMMEDIATE BACKGROUND BROWSER THREAD
    print("🚀 [Simultaneous Trigger] Launching Chrome Automation...")
    try:
        chrome_thread = Thread(target=run_chrome_pipeline, args=("Chrome", chrome_exe, "--incognito"), daemon=True)
        chrome_thread.start()
    except Exception as browser_err:
        print(f"⚠️ Failed to launch browser thread: {browser_err}")

    # 3. IMMEDIATE FOREGROUND TELEGRAM PING
    try:
        if row is not None:
            msg = (
                f"🔥 <b>US F1 VISA RADAR ALERT</b> 🔥\n\n"
                f"📍 <b>Location:</b> {row['Visa Location']}\n"
                f"📅 <b>Earliest Date:</b> {row['Earliest Date']}\n"
                f"🔢 <b>Slots on Date:</b> {row['Slots on Earliest Date']}\n"
                f"📊 <b>Total Active Dates:</b> {row['Total Dates Available']}\n"
                f"🕒 <b>Last Seen:</b> {row['Relative Time']}\n\n"
                f"🚀 Log into your portal immediately!"
            )
        else:
            msg = "🔥 No VAC drop has been detected!"

        payload = {
            "chat_id": MY_PERSONAL_CHAT_ID, 
            "text": msg, 
            "parse_mode": "HTML"
        }

        print("📱 [Simultaneous Trigger] Routing Telegram Network Packets...")
        response = requests.post(
            f"https://api.telegram.org/bot{ALERT_BOT_TOKEN}/sendMessage", 
            json=payload,
            timeout=4.0
        )
        response.raise_for_status()
        print("📱 Mobile push alert routed to phone successfully.")
    except Exception as e:
        print(f"Could not send mobile alert: {e}")

    print("🔄 [System Engine] Browser automation context cleared. Portal re-auth paths unlocked.")


# 👇 Upgraded with comprehensive breakdown parameters: pure_capture_latency, predicted_step
def log_alarm_event(location=None, slots=None, earliest_date=None, relative_time=None, 
                    cycle_number=None, event_type="alarm", runtime_mins=0.0, 
                    lateness_mins=None, pure_capture_latency=None, predicted_step=None):
    log_file = "check_us_visa_history.log" 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if event_type == "start":
        log_line = f"-------------------------------------------------------------\n[{timestamp}] ▶️ Start\n"
    elif event_type == "screenshot":
        log_line = f"[{timestamp}] 📸 Screenshot Success -> Runtime -> {runtime_mins:.2f} mins\n"
    elif event_type == "model":
        # Appends the total target lateness metric seamlessly if provided
        latency_str = f" | Total Current Lateness: {lateness_mins:.2f} mins old" if lateness_mins is not None else ""
        log_line = f"[{timestamp}] 🔮 Model Ran -> Runtime -> {runtime_mins:.2f} mins | Gen Time: {location if location else 'N/A'}{latency_str}\n"
    
    elif event_type == "sleep":
        # 📝 NEW EVENT TYPE: Breakdown of the feedback loop calibration
        cap_lag = f"{pure_capture_latency:.2f}m" if pure_capture_latency is not None else "N/A"
        pred_s = f"+{predicted_step}m" if predicted_step is not None else "N/A"
        log_line = f"[{timestamp}] ⏳ Loop Synchronized -> Predicted Server Step: {pred_s} | Pure Capture Lag: {cap_lag} | Scheduled Sleep: {runtime_mins:.2f} mins\n"
        
    elif event_type == "rate_limit":
        log_line = f"[{timestamp}] 🛑 RATE LIMIT / FORBIDDEN DETECTED -> Entering 1-Hour Deep Sleep | Runtime -> {runtime_mins:.2f} mins\n"
    elif event_type == "end":
        log_line = f"[{timestamp}] ⏹️ Ends\n-------------------------------------------------------------\n"
    else:
        log_line = f"[{timestamp}] 🚨 ALARM TRIGGERED -> City: {location} | Slots: {slots} | Earliest: {earliest_date} | Age: {relative_time} | Cycle: #{cycle_number} | Runtime -> {runtime_mins:.2f} minutes | Gen Time: {earliest_date}\n"
        
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)
        if event_type in ["alarm", "rate_limit", "sleep"]:
            print(f"📝 Event successfully logged to {log_file}")
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")


def log_firewall_metric(metric_type, total_hits_in_hour, cooldown_mins=0):
    """
    Saves firewall behavior events to a local log file to identify
    the precise threshold boundaries.
    """
    log_file = "firewall_metrics.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    
    # Check if we need to write headers for a brand new log file
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("=== VISA BOT FIREWALL TELEMETRY LOG ===\n")
            
    with open(log_file, "a") as f:
        if metric_type == "BLOCK":
            f.write(f"[{timestamp}] 🚨 BLOCK TRIGGERED! Total hits achieved in last 60 mins before crash: {total_hits_in_hour}\n")
        elif metric_type == "RECOVERY":
            f.write(f"[{timestamp}] ✅ RECOVERY SUCCESSFUL! System unblocked after a {cooldown_mins} min sleep window.\n")



