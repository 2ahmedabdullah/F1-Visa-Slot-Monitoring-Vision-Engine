#humanize_browsing.py

import random
import pyautogui
import time
import numpy as np
import os
from threading import Lock
import subprocess
import json



mouse_lock = Lock()

# ==========================================
# UI HARDWARE CURSOR ENGINE (CUBIC BÉZIER)
# ==========================================
def calculate_bezier_points(start_x, start_y, end_x, end_y):
    p1_x = start_x + (end_x - start_x) * random.uniform(0.25, 0.5) + random.randint(-20, 20)
    p1_y = start_y + (end_y - start_y) * random.uniform(0.25, 0.5) + random.randint(-20, 20)
    p2_x = start_x + (end_x - start_x) * random.uniform(0.5, 0.75) + random.randint(-20, 20)
    p2_y = start_y + (end_y - start_y) * random.uniform(0.5, 0.75) + random.randint(-20, 20)
    num_steps = random.randint(18, 32)
    points = []
    for t in np.linspace(0, 1, num_steps):
        x = (1-t)**3 * start_x + 3*(1-t)**2 * t * p1_x + 3*(1-t) * t**2 * p2_x + t**3 * end_x
        y = (1-t)**3 * start_y + 3*(1-t)**2 * t * p1_y + 3*(1-t) * t**2 * p2_y + t**3 * end_y
        points.append((int(x), int(y)))
    return points

def human_mouse_move(target_x, target_y):
    start_x, start_y = pyautogui.position()
    if abs(start_x - target_x) < 2 and abs(start_y - target_y) < 2:
        return
    path_points = calculate_bezier_points(start_x, start_y, target_x, target_y)
    for pt_x, pt_y in path_points:
        pyautogui.moveTo(pt_x, pt_y)
        time.sleep(random.uniform(0.008, 0.015)) 

def human_click(target_x, target_y):
    initial_x = target_x + random.randint(-4, 4)
    initial_y = target_y + random.randint(-4, 4)
    human_mouse_move(initial_x, initial_y)
    time.sleep(random.uniform(0.1, 0.2))  
    hover_steps = random.randint(2, 3)
    current_x, current_y = initial_x, initial_y
    for _ in range(hover_steps):
        wiggle_x = current_x + random.choice([-2, -1, 1, 2])
        wiggle_y = current_y + random.choice([-2, -1, 1, 2])
        if abs(wiggle_x - target_x) <= 6 and abs(wiggle_y - target_y) <= 6:
            pyautogui.moveTo(wiggle_x, wiggle_y, duration=random.uniform(0.05, 0.12))
            current_x, current_y = wiggle_x, wiggle_y
    time.sleep(random.uniform(0.05, 0.15))  
    pyautogui.mouseDown(button='left')
    time.sleep(random.uniform(0.07, 0.14))  
    pyautogui.mouseUp(button='left')

def force_clean_session_state(profile_dir):
    pref_path = os.path.join(profile_dir, "Default", "Preferences")
    if os.path.exists(pref_path):
        try:
            with open(pref_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "profile" not in data:
                data["profile"] = {}
            data["profile"]["exit_type"] = "Normal"
            data["profile"]["exited_cleanly"] = True
            with open(pref_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print("🛡️ [Fix] Patched Edge preferences to suppress restore bubble.")
        except Exception as e:
            print(f"⚠️ [Fix] Failed to patch preferences: {e}")

# ==========================================
# 4. PARALLEL CLICKER THREAD ENGINE
# ==========================================
def run_chrome_pipeline(browser_name, exe_path, flag):
    url = "https://www.usvisascheduling.com"
    if not os.path.exists(exe_path): return
    TARGET_X = 426  
    TARGET_Y = 520  

    print(f"🚀 [Thread-{browser_name}] Launching {browser_name}...")
    try:
        subprocess.Popen([exe_path, flag, url], shell=False)
    except Exception as e:
        print(f"❌ [Thread-{browser_name}] Process Spawn Failure: {e}")
        return

    time.sleep(random.uniform(6.5, 9.5))

    with mouse_lock:
        print(f"🎯 [{browser_name}] Acquired UI hardware control cursor...")
        try:
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(1.8, 3.4))
            
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(4.1, 6.7))
            
            human_click(TARGET_X, TARGET_Y)
            time.sleep(random.uniform(11.2, 16.4))

            human_click(TARGET_X, TARGET_Y)
            print(f"✅ [{browser_name}] Humanized macro sequence successfully delivered.")
        except Exception as err:
            print(f"⚠️ [Thread-{browser_name}] Humanized mouse control error: {err}")


def run_browser_pipeline(browser_name, exe_path):

    url = "https://checkvisaslots.com/latest-us-visa-availability/f-1-regular/"
    output_filename = f"visa_slots.png"

    if not os.path.exists(exe_path): 
        print(f"❌ [Thread-{browser_name}] Binary path invalid.")
        return
    
    profile_dir = os.path.join(os.getcwd(), f"real_user_footprint_{browser_name}")
    os.makedirs(profile_dir, exist_ok=True) 
    force_clean_session_state(profile_dir)
    flags = [
        f"--user-data-dir={profile_dir}", "--start-maximized",
        "--disable-blink-features=AutomationControlled", "--no-first-run",
        "--no-default-browser-check", "--disable-infobars", "--hide-crash-restore-bubble", 
        f"--remote-debugging-port={random.randint(9200, 9399)}",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    ]
    print(f"🚀 [Thread-{browser_name}] Launching anti-detection wrapper for Edge...")
    try:
        subprocess.Popen([exe_path] + flags + [url], shell=False)
    except Exception as e:
        print(f"❌ [Thread-{browser_name}] Process Spawn Failure: {e}")
        return
    time.sleep(random.uniform(2.0, 4.0))
    with mouse_lock:
        print(f"🎯 [{browser_name}] Acquired UI hardware control cursor...")
        try:
            LOGO_X = 1740 + random.randint(-3, 2)
            LOGO_Y = 220 + random.randint(-2, 2)
            human_click(LOGO_X, LOGO_Y)
            time.sleep(random.uniform(2.0, 3.0))
            pyautogui.scroll(-500 + random.randint(-10, 10)) 
            screenshot_path = os.path.join(os.getcwd(), output_filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            print(f"📸 Success! Saved clean screenshot.")
            time.sleep(1.0)
            os.system("taskkill /f /im msedge.exe")
        except Exception as err:
            print(f"⚠️ [Thread-{browser_name}] Curved mouse sequence broken: {err}")