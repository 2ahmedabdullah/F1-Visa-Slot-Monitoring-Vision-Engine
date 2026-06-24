#dynamic_sleep.py

import random
import time
from datetime import datetime, timedelta

def dynamic_adaptive_sleep(history_list, hourly_hit_log, error_streak, sequence_start_time, lateness_history=None):
    """
    Visa Sniper Engine - Advanced Feedback & Stall-Protection Edition
    
    CRITICAL FORMULAS IMPLEMENTED:
    1. Base Sleep = (Target Pattern Step - Data Age) - Hardware Lead
    2. Lateness Error = Average(Last 3 Lateness Points) - 2.0 Target Minutes
    3. Final Calibrated Sleep = Base Sleep - Lateness Error
    
    EXECUTION HIERARCHY:
    Priority 1: 4-Stamp Gear Shift Decoder (Intercepts transitions)
    Priority 2: 3-Stamp Pattern Matrix (Maintains steady state waves)
    Priority 3: Fallback Baseline (Handles anomalies safely)
    """
    now = datetime.now()
    default_interval = 8  # Fallback baseline step (minutes)
    pure_capture_latency = time.time() - sequence_start_time

    # ==========================================
    # 1. PROCESS ROLLING HOURLY HIT COUNTER
    # ==========================================
    one_hour_ago = now - timedelta(hours=1)
    active_hourly_hits = [hit for hit in hourly_hit_log if hit > one_hour_ago]
    total_hits_this_hour = len(active_hourly_hits)

    # ==========================================
    # 2. ESCALATING ERROR COOLDOWN ENGINE
    # ==========================================
    if history_list and history_list[-1].strip() == "Error Page":
        cooldown_minutes = 20 if error_streak == 1 else (25 if error_streak == 2 else 40)
        seconds_to_sleep = max(360.0, (cooldown_minutes * 60.0) - pure_capture_latency) #  FIXED
        target_sleep_minutes = seconds_to_sleep / 60.0
        return seconds_to_sleep, target_sleep_minutes, pure_capture_latency, cooldown_minutes

    # ==========================================
    # 3. FILTER AND VALIDATE HISTORY DEPTH
    # ==========================================
    clean_history = [t for t in history_list if t.strip() != "Error Page"]
    total_points = len(clean_history)

    # Absolute minimum requirement for engine pattern synchronization
    if total_points < 3:
        seconds_to_sleep = max(10.0, (default_interval * 60.0) - pure_capture_latency)
        target_sleep_minutes = seconds_to_sleep / 60.0
        print(f"📋 History shallow ({total_points}/3). Defaulting to 8+ baseline sleep.")
        return seconds_to_sleep, target_sleep_minutes, pure_capture_latency, default_interval

    # ==========================================
    # 4. PARSE TIMESTAMPS & FIX DAY BOUNDARIES
    # ==========================================
    fmt = "%I:%M %p"
    try:
        y_gen = datetime.strptime(clean_history[-1].strip(), fmt).replace(year=now.year, month=now.month, day=now.day)
        x_gen = datetime.strptime(clean_history[-2].strip(), fmt).replace(year=now.year, month=now.month, day=now.day)
        w_gen = datetime.strptime(clean_history[-3].strip(), fmt).replace(year=now.year, month=now.month, day=now.day)
        
        # 🚨 THE MIDNIGHT CROSS GUARD FIX 🚨
        if now.hour == 0 or now.hour == 1:
            if y_gen.hour == 23 or y_gen.hour == 22: y_gen -= timedelta(days=1)
            if x_gen.hour == 23 or x_gen.hour == 22: x_gen -= timedelta(days=1)
            if w_gen.hour == 23 or w_gen.hour == 22: w_gen -= timedelta(days=1)

        # Handle chronological day transitions inside the history sequence itself
        if y_gen < x_gen: y_gen += timedelta(days=1)
        if x_gen < w_gen: x_gen += timedelta(days=1)
        
        # Calculate raw gaps between historical updates
        d1 = round((y_gen - x_gen).total_seconds() / 60.0)
        d2 = round((x_gen - w_gen).total_seconds() / 60.0)
        
        # 🚨 STALL & INVERSION PROTECTION CRITICAL EXCEPTION LAYER 🚨
        # Catch duplicate tables (d1 <= 0) OR historical timestamp rollbacks (y_gen is older than current real time or creates an impossible gap)
        data_age_check_mins = (now - y_gen).total_seconds() / 60.0
        
        if d1 <= 0 or data_age_check_mins < 0 or d2 > 60:
            print(f"🛑 [Chronological Anomaly Detected] Stale or inverted timestamps found (d1={d1}m, Age={data_age_check_mins:.1f}m).")
            print("   Forcing safety override to protect engine from massive multi-hour desync sleep loops.")
            
            # Virtualize timestamps to standard baseline progression
            y_gen = now  # Reset the data age calculation to 0 minutes old
            x_gen = y_gen - timedelta(minutes=8)
            w_gen = x_gen - timedelta(minutes=8)
            d1 = 8
            d2 = 8

    except Exception as parse_err:
        print(f"⚠️ Timestamp parsing error: {parse_err}. Defaulting to safe baseline sleep.")
        seconds_to_sleep = 30*60
        return seconds_to_sleep, seconds_to_sleep / 60.0, pure_capture_latency, default_interval

    # Initialize execution targets
    next_interval_mins = None
    pattern_identified = None

    # ========================================================
    # 5. PRIORITY 1: GEAR SHIFT DECODER (4-Log Deep Window Check)
    # ========================================================
    if total_points >= 4:
        try:
            v_gen = datetime.strptime(clean_history[-4].strip(), fmt).replace(year=now.year, month=now.month, day=now.day)
            if now.hour == 0 and v_gen.hour == 23: v_gen -= timedelta(days=1)
            if w_gen < v_gen: w_gen += timedelta(days=1)
            
            d3 = round((w_gen - v_gen).total_seconds() / 60.0)
            
            # Match the specialized transition rules
            if d1 == 6 and d2 == 10: 
                next_interval_mins = 8  
                pattern_identified = f"🏎️ Gear Shift Recovery Sequence [Gaps: {d3}m -> {d2}m -> {d1}m]"
            elif d1 == 4 and d2 == 10: 
                next_interval_mins = 6  
                pattern_identified = f"🏎️ Gear Shift Acceleration Sequence [Gaps: {d3}m -> {d2}m -> {d1}m]"
            elif d1 == 10 and d2 == 6: 
                next_interval_mins = 10 
                pattern_identified = f"🏎️ Gear Shift Cooldown Sequence [Gaps: {d3}m -> {d2}m -> {d1}m]"
        except Exception:
            pass # Pass through seamlessly to standard matrix if 4th-log verification errors out

    # ========================================================
    # 6. PRIORITY 2: STANDARD PATTERN RECOGNITION MATRIX (3-Log)
    # ========================================================
    if next_interval_mins is None:
        # ---- SERIES 3: The 6-6-6-6 Series (High-Volume Processing) ----
        if d1 == 6 and d2 == 6:
            next_interval_mins = 6
            pattern_identified = "Series 3: High-Volume Processing Loop (6-6-6-6)"
        
        # ---- SERIES 4: The 6-4-6-4 Series (Peak Active Polling) ----
        elif d1 == 4 and d2 == 6:
            next_interval_mins = 6
            pattern_identified = "Series 4: Peak Active Polling (6-4-6-4 Tracking)"
        elif d1 == 6 and d2 == 4:
            next_interval_mins = 4
            pattern_identified = "Series 4: Peak Active Polling (6-4-6-4 Tracking)"

        # ---- SERIES 2: The 6-8-6-8 Series (Long-Run Cruise Control) ----
        elif d1 == 8 and d2 == 6:
            next_interval_mins = 6
            pattern_identified = "Series 2: Long-Run Cruise Control (6-8-6-8 Tracking)"
        elif d1 == 6 and d2 == 8:
            next_interval_mins = 8
            pattern_identified = "Series 2: Long-Run Cruise Control (6-8-6-8 Tracking)"

        # ---- SERIES 1: The 10-10-10-8-8 Series (Routine & Reset) ----
        elif d1 == 10 and d2 == 10:
            next_interval_mins = 10
            pattern_identified = "Series 1: Routine Baseline (10-10-10 Ongoing)"
        elif d1 == 8 and d2 == 10:
            next_interval_mins = 8
            pattern_identified = "Series 1: Tapering Phase (10 -> 8 Shift)"
        elif d1 == 8 and d2 == 8:
            next_interval_mins = 10
            pattern_identified = "Series 1: Reset Trigger Imminent (8 -> 8 Complete)"
        
        # ---- SERIES 5: Sustained High-Velocity Polling (4-4-4-4 Continuous) ----
        elif d1 == 4 and d2 == 4:
            next_interval_mins = 4
            pattern_identified = "Series 5: Sustained High-Velocity Polling Loop (4-4-4-4)"
            
    # ========================================================
    # 7. PRIORITY 3: STRUCTURAL FALLBACK CORRECTION
    # ========================================================
    if next_interval_mins is None:
        next_interval_mins = default_interval
        pattern_identified = f"Broken Pattern Window (Gaps: {d2}m -> {d1}m). Resetting to 8+ Baseline."

    # ========================================================
    # 8. TIME CONVERGENCE MATHEMATICS WITH ERROR DEBT CORRECTION
    # ========================================================
    # Calculate exactly how long ago the server generated the last update table
    data_age_seconds = ((now - timedelta(seconds=80)) - y_gen).total_seconds()
    target_interval_seconds = next_interval_mins * 60.0
    # Base anti-bot pre-fire buffer (wake up 5-10s early)
    hardware_lead_time_seconds = random.uniform(5.0, 10.0) 
    # Calculate base raw sleep time target
    seconds_to_sleep = target_interval_seconds - data_age_seconds - hardware_lead_time_seconds

    avg_lateness_mins = 0.0

    # 🚨 MOVING-AVERAGE LATENESS CORRECTION FEEDBACK ENGINE 🚨
    lateness_penalty_seconds = 0.0
    if lateness_history and len(lateness_history) >= 1:
        # Evaluate up to the last 3 runs to dynamically compute laggard debt
        recent_lateness = lateness_history[-3:]
        avg_lateness_mins = sum(recent_lateness) / len(recent_lateness)
        
        if avg_lateness_mins > 2.0:
            lateness_error_mins = avg_lateness_mins - 2.0
            lateness_penalty_seconds = lateness_error_mins * 60.0
            
            # Apply error penalty directly to pull forward the pipeline run
            seconds_to_sleep -= lateness_penalty_seconds
            print(f"🎯 [Feedback Loop Active] Avg Lateness: {avg_lateness_mins:.2f}m. Target: 2.0m.")
            print(f"   Applying correction penalty: Shaving {lateness_penalty_seconds:.2f}s off sleep.")

    # Safety catch 1: If processing delay overshot target pattern entirely, cycle instantly!
    if seconds_to_sleep <= 0:
        print(f"⚠️ [Timing Correction Alert] Processing delay overshot target pattern. Recycling pipeline.")
        seconds_to_sleep = 360.0  # Safe recovery anchor bounce

    # 🛡️ Safety catch 2: THE SAFETY VALVE (Anti-Rate-Limit & Anti-Desync Throttle)
    else:
        target_sleep_minutes_temp = seconds_to_sleep / 60.0
        
        # 🚨 NEW: Only trigger rate-limit protection if we aren't actively trying to catch up from being late!
        if target_sleep_minutes_temp < 2.0 and avg_lateness_mins <= 2.0:
            print("\n🛑 [Safety Valve Triggered] Recovery window too short, risk of rate-limiting is high!")
            
            # Mathematically push the target out exactly one full server cycle ahead
            target_sleep_minutes_temp += next_interval_mins
            seconds_to_sleep = target_sleep_minutes_temp * 60.0
            
            print(f"🔄 Buffered sleep window expanded to: {target_sleep_minutes_temp:.2f} mins to protect IP health.")
            
        elif target_sleep_minutes_temp < 2.0 and avg_lateness_mins > 2.0:
            # We bypass the safety valve because the feedback engine explicitly ordered a fast run to catch up
            print(f"🏎️ [Safety Valve Inactive] Sleep is {target_sleep_minutes_temp:.2f}m, but bypassing rate-limit floor to clear {avg_lateness_mins:.2f}m of server lateness.")

    # ==========================================
    # 9. LIVE TERMINAL INTERCEPT DASHBOARD
    # ==========================================
    print("\n" + "⚡" * 30)
    print(f"🎯 ENGINE STATUS         : {pattern_identified}")
    print(f"   • Rolling Hourly Scans    : {total_hits_this_hour} hits in last 60m")
    print(f"   • Last Table Gen Time     : {clean_history[-1].strip()}")
    print(f"   • Current Data Age        : {(now - y_gen).total_seconds() / 60.0:.2f} minutes old")
    print(f"   • Next Refresh Estimate   : +{next_interval_mins} minutes")
    print(f"   • Active Feedback Shift   : Shaved {lateness_penalty_seconds:.2f} seconds")
    print(f"   • PURE SLEEP CALIBRATION  : {(seconds_to_sleep-60):.2f} seconds")
    print("⚡" * 30 + "\n")

    # Export true calculated targets cleanly
    seconds_to_sleep = seconds_to_sleep-90
    if seconds_to_sleep<=60:
        seconds_to_sleep = 120
    target_sleep_minutes = seconds_to_sleep / 60.0
    
    return seconds_to_sleep, target_sleep_minutes, pure_capture_latency, next_interval_mins