import os
import time
from datetime import datetime, timedelta
from alarm import log_alarm_event, trigger_drop_alarm
from humanize_browsing import run_browser_pipeline
from screenshot import optimize_screenshot_for_vram
from models import fast_extract_table, fast_extract_table_groq
import pandas as pd
from dynamic_sleep import dynamic_adaptive_sleep
import requests
import json

def is_within_sweet_spot(relative_time_str, max_hours=24):
    time_str = str(relative_time_str).lower().strip()
    if "min" in time_str:
        try:
            return int(time_str.split("min")[0].strip()) <= 20
        except:
            return False
    if "hr" in time_str: return False
    return False

def check_active_hardware():
    """Queries the local Ollama daemon to see what hardware is processing the model."""
    try:
        response = requests.get("http://localhost:11434/api/ps")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if not models:
                print("ℹ️ No models actively loaded in memory right now.")
                return
            for model in models:
                name = model.get("name")
                processor = model.get("processor", "Unknown")
                vram = model.get("size_vram", 0) / (1024**3) # Convert bytes to GB
                print(f"📊 Active Hardware Status -> Model: {name} | Backend Engine: {processor} | VRAM Used: {vram:.2f} GB")
        else:
            print("⚠️ Could not reach Ollama status endpoint.")
    except Exception as e:
        print(f"⚠️ Hardware check skipped: {e}")

# ==========================================
# LIVE MONITORING RADAR SEQUENCE
# ==========================================

if __name__ == "__main__":
    # Start time at 0 mins
    print("Start Time: 0 mins")
    startime = datetime.now()
    # Record the exact beginning
    start_perf = time.perf_counter()

    image_file_path = "visa_slots.png" 

    EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    last_triggered_snapshot = "" 
    alert_counter = 0  
    history_log = []
    hourly_hit_log = [] 
    lateness_tracker = []
    error_streak = 0
    
    print("🚀 Radar Pipeline Active. Monitoring slots in-memory every 10 minutes. Press Ctrl+C to stop.")
    
    while True:
        if os.path.exists(image_file_path):
            os.remove(image_file_path)

        sequence_start_time = time.time()
        start = datetime.now()

        log_alarm_event(event_type="start")
        # 1. Load Configurations globally at startup

        CONFIG_FILE = "config.json"
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
            print("⚙️ Successfully loaded keyword configurations from JSON layout.")

        params = config_data.get("PARAMS", {})
        json_schema = config_data.get("JSON_SCHEMA", {})

        # 2. Define Execution Target
        TEST_IMAGE_PATH = r"cropped_visa_table.png"

        print(f"\n🎬 Starting scan sequence at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        run_browser_pipeline("Stealth-Edge", EDGE_EXE)


        # --- LOG SCREENSHOT STAGE ---
        log_alarm_event(event_type="screenshot", runtime_mins=(time.time() - sequence_start_time) / 60)

        try:
            print("✂️ Cropping the new visa_slots.png to protect 6GB VRAM...")
            optimized_image_path = optimize_screenshot_for_vram("visa_slots.png", output_path="cropped_visa_table.png")
        except Exception as e:
            print(f"❌ Failed to crop fresh image: {e}")
            optimized_image_path = "visa_slots.png"

        # 3. Process Execution Matrix (This blocks and waits until finished)
        df, footer_text = fast_extract_table(TEST_IMAGE_PATH, params, json_schema)

        ps = requests.get("http://localhost:11434/api/ps").json()
        # print("Active models:", ps.get("models", []))


        # 4. Check hardware status immediately AFTER processing the image
        print("\n--------------------------------------------------")
        print("Checking active engine state during/after vision processing...")
        check_active_hardware()
        print("--------------------------------------------------")

        elapsed = datetime.now() - start
        print(f"Elapsed time in Generation: {elapsed}")
        print("--------------------------------------------------")

        # --- ANTI-BAN FORBIDDEN/RATE LIMIT DETECTOR ---
        is_forbidden = df is None or df.empty or (len(df) == 1 and "error" in str(df.iloc[0]).lower())
        if is_forbidden:
            error_streak += 1  # Track progressive blocks
            history_log.append("Error Page")  # Route to tracking layer
            
            # ✅ FIX 1: Correct unpack order to match function return signature perfectly
            seconds_to_sleep, target_sleep_minutes, pure_capture_latency, cooldown_minutes = dynamic_adaptive_sleep(
                history_list=history_log, 
                hourly_hit_log=hourly_hit_log, 
                error_streak=error_streak, 
                sequence_start_time=sequence_start_time,
                lateness_history=lateness_tracker # Pass it here too as a safety default
            )
            
            log_alarm_event(event_type="rate_limit", runtime_mins=target_sleep_minutes)
            log_alarm_event(event_type="end")
            
            print(f"🛑 Adaptive Cooldown Active: Sleeping for {target_sleep_minutes:.2f} mins to clear firewall reset-key.")
            time.sleep(seconds_to_sleep)
            continue  # Drop back safely to the top of the next loop pass

        # 2. Define exactly how to fill blanks per column
        clean_rules = {
            "Visa Location": "Unknown Location",
            "Earliest Date": "No Date Available",
            "Slots on Earliest Date": 0,       # Keeps this column as an integer!
            "Total Dates Available": 0,        # Keeps this column as an integer!
            "Relative Time": "N/A"
        }

        # 3. Apply the rules globally
        df.fillna(value=clean_rules, inplace=True)


        if df is not None and not df.empty:
            df = df[df["Visa Location"].str.contains("VAC", case=False, na=False)].copy()
            df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()
            # Map common LLM table header variations to the expected baseline string
            df = df.rename(columns={
                'Total Dates': 'Total Dates Available',
                'Total Dates Available': 'Total Dates Available'
            })

            clean_footer_short = footer_text.replace("Latest update as of ", "").replace("Latest updates as of ", "").strip()

            # Extract and parse the generation time safely by removing commas first
            gen_time_parts = clean_footer_short.split("generated at")
            gen_time_str = gen_time_parts[-1].replace(",", "").strip() if len(gen_time_parts) > 1 else clean_footer_short

            # 👇 Clean extraction targeting exactly the trailing "HH:MM AM/PM" element
            try:
                # Splits by spaces and grabs the last two components (e.g., ['11:02', 'PM'])
                time_parts = gen_time_str.split()
                time_only_str = f"{time_parts[-2]} {time_parts[-1]}".strip()
                
            except Exception:
                time_only_str = gen_time_str  # Emergency fallback

            if not history_log or history_log[-1] != time_only_str:
                error_streak = 0  # <--- ADD THIS LINE (Resets block chain)
                hourly_hit_log.append(datetime.now())  # <--- ADD THIS LINE (Logs success metric)
                history_log.append(time_only_str)

                if len(history_log) > 3:  # Keep list lean and memory bounded
                    history_log.pop(0)

            generation_time = pd.to_datetime(gen_time_str, errors='coerce')

            # Calculate the data age latency relative to right now securely
            try:
                if pd.notna(generation_time):
                    # Force conversion from pandas Timestamp to native Python datetime
                    native_gen_time = generation_time.to_pydatetime()
                    current_lateness = (datetime.now() - native_gen_time).total_seconds() / 60.0
                    lateness_tracker.append(current_lateness)
                else:
                    current_lateness = None
            except Exception as latency_err:
                print(f"⚠️ Could not calculate log latency: {latency_err}")
                current_lateness = None

            # --- LOG MODEL STAGE WITH WEBPAGE GENERATION TIME & LATENCY ---
            log_alarm_event(
                event_type="model", 
                runtime_mins=(time.time() - sequence_start_time) / 60, 
                location=gen_time_str,
                lateness_mins=current_lateness
            )

            significant_drop_found = False
            current_snapshot = ""  
            matched_row_data = None  
            
            df_fresh = df[df["Relative Time"].apply(lambda x: is_within_sweet_spot(x, max_hours=24))].copy()
            
            
            matched_rows = []
            if not df_fresh.empty:
                for _, row in df_fresh.iterrows():
                    try:
                        try:
                            total_dates = int(float(row["Total Dates Available"]))
                        except (ValueError, TypeError):
                            total_dates = 0

                        try:
                            earliest_slots = int(float(row["Slots on Earliest Date"]))
                        except (ValueError, TypeError):
                            earliest_slots = 0

                        time_str = str(row["Relative Time"]).lower().strip()
                        
                        # Check numbers first so the alarm triggers immediately
                        if total_dates >= 7 or earliest_slots >= 7:
                            significant_drop_found = True
                            matched_rows.append(row)
                            print(f"🔥 CONDITIONS MET! High-Volume Drop Found: {row['Visa Location']}")
                            print(f"📈 Match Details: {total_dates} Total Dates | {earliest_slots} Earliest Slots")

                        # Run time delta math separately so formatting crashes cannot block the alarm
                        try:
                            slot_last_seen = pd.to_datetime(row["Last Seen At"], errors='coerce')
                            if pd.notna(generation_time) and pd.notna(slot_last_seen):
                                time_difference_mins = abs((generation_time - slot_last_seen).total_seconds() / 60)
                                print(f"⏱️ Drop Latency: Roughly {round(time_difference_mins)} mins old.")
                        except Exception as time_err:
                            print(f"⚠️ Timestamp cross-check skipped due to formatting: {time_err}")  

                    except Exception as row_err:
                        print(f"❌ Structural data parsing error on this row: {row_err}")

            if significant_drop_found and matched_rows:
                # 1. Generate the fresh real-time string profile
                current_snapshot = "|".join([f"{r['Visa Location']}-{r['Total Dates Available']}-{r['Earliest Date']}" for r in matched_rows])
                
                # 2. Run the mutation check FIRST to intercept state alterations
                if last_triggered_snapshot:
                    try:
                        current_loc = matched_rows[0]['Visa Location']
                        current_count = int(float(matched_rows[0]['Total Dates Available']))
                        
                        prev_parts = last_triggered_snapshot.split("|")[0].split("-")
                        prev_loc = prev_parts[0]
                        prev_count = int(prev_parts[1]) if len(prev_parts) > 1 else 0
                        
                        # If a new city appears or counts scale up, clear the cache to allow an update
                        if current_loc != prev_loc or current_count > prev_count:
                            last_triggered_snapshot = "" 
                            print(f"🔄 Radar detected a critical state evolution! Location shift or capacity surge tracked.")
                    except Exception as snapshot_err:
                        print(f"⚠️ Snapshot state variation parsing exception: {snapshot_err}")

                # 3. Use the updated state variable for the alert conditional logic
                matched_row_data = matched_rows[0]  # Fallback payload data

                if current_snapshot != last_triggered_snapshot:
                    alert_counter = 1  
                    last_triggered_snapshot = current_snapshot
                    
                    for match_row in matched_rows:
                        log_alarm_event(
                            location=match_row['Visa Location'],
                            slots=match_row['Total Dates Available'],
                            earliest_date=gen_time_str,
                            relative_time=match_row['Relative Time'],
                            cycle_number=alert_counter,
                            event_type="alarm",
                            runtime_mins=(time.time() - sequence_start_time) / 60
                        )
                    trigger_drop_alarm(matched_rows[0])
                    
                else:
                    alert_counter += 1  
                    print(f"🤫 Alarm skipped: Already alerted you about this drop state (Cycle #{alert_counter}).")
                    
                    for match_row in matched_rows:
                        log_alarm_event(
                            location=match_row['Visa Location'],
                            slots=match_row['Total Dates Available'],
                            earliest_date=gen_time_str,
                            relative_time=match_row['Relative Time'],
                            cycle_number=alert_counter,
                            event_type="alarm",
                            runtime_mins=(time.time() - sequence_start_time) / 60
                        )
                
            else:
                print("ℹ️ No target VAC drops found. Sending test status ping to Telegram...")
                # trigger_drop_alarm(row=None)
                    

            df_display = df[df["Relative Time"].apply(lambda x: is_within_sweet_spot(x))].copy()

            if not df_display.empty:
                df_display['Total Dates Available Num'] = df_display['Total Dates Available'].astype(float).astype(int)
                df_display = df_display[df_display['Total Dates Available Num'] >= 3].copy()


            if not df_display.empty:
                df_display['parsed_date'] = pd.to_datetime(df_display['Earliest Date'], format="%d %b, %y", errors='coerce')
                reference_date = generation_time if pd.notna(generation_time) else datetime.now()
                df_display['is_valid_future_date'] = df_display['parsed_date'] >= reference_date

                df_display['is_stale_data'] = ~df_display['Relative Time'].str.contains('mins', na=False, case=False)

                df_sorted = df_display.sort_values(by=['is_valid_future_date', 'is_stale_data', 'Total Dates Available Num', 'parsed_date'], 
                    ascending=[False, True, False, True]).copy()

                df_sorted = df_sorted.drop(columns=['parsed_date', 'is_valid_future_date', 'is_stale_data', 'Total Dates Available Num'], errors='ignore')

                print("="*40)
                print(f"📊 High-Priority Dashboard (Total Dates Available ≥ 3)")
                print(f"🌐 Website Status: {clean_footer_short}")
                if significant_drop_found and alert_counter > 0:
                    print(f"🚨 ACTIVE EMERGENCY: Alert has been active for {alert_counter * 10} mins!")
                print("-"*40)
                print(df_sorted.to_string(index=False))
                print("="*40)
            else:
                print("="*40)
                print(f"📊 High-Priority Dashboard")
                print(f"🌐 Website Status: {clean_footer_short}")
                print("-"*40)
                print("No active locations found with 3 or more open dates.")
                print("="*40)


        # Calculate total minutes taken for this loop cycle only
        end_time_now = time.time()
        total_minutes = (end_time_now - sequence_start_time) / 60

        # End time shows how many minutes it took
        print(f"End Time:   {total_minutes:.2f} mins")
        # --- CLOSE OUT SEQUENCE LOG ---
        log_alarm_event(event_type="end")

        # 1. Fetch calibrated parameters from your upgraded adaptive sleep engine
        # (For this to work, make sure your dynamic_adaptive_sleep function returns target_sleep_minutes, seconds_to_sleep, pure_capture_latency, next_interval_mins)
        seconds_to_sleep, target_sleep_minutes, pure_capture_latency, next_interval_mins = dynamic_adaptive_sleep(
                history_list=history_log, 
                hourly_hit_log=hourly_hit_log, 
                error_streak=error_streak, 
                sequence_start_time=sequence_start_time,
                lateness_history=lateness_tracker # 🚨 CRITICAL: Feeds the PI loop
            )


        # 2. Log the raw latency breakdown to your file before going to sleep
        log_alarm_event(
            event_type="sleep",
            runtime_mins=target_sleep_minutes, 
            pure_capture_latency=pure_capture_latency,
            predicted_step=next_interval_mins
        )

        # 🧹 MEMORY CLEANUP: Prune historical lists down to rolling window requirements
        history_log = history_log[-10:]
        lateness_tracker = lateness_tracker[-10:]

        hourly_hit_log = [hit for hit in hourly_hit_log if hit > (datetime.now() - timedelta(hours=1))]

        mins_to_sleep = seconds_to_sleep / 60.0
        
        print(f"\n⏳ Sleeping for {mins_to_sleep:.2f} minutes until next engine check...")
        print("Elapsed Time:", datetime.now()-startime)
        time.sleep(seconds_to_sleep)