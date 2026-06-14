# US F1 Visa Slot Sniper Radar 🚀🎯
An automated, high-frequency, anti-detection monitoring pipeline designed to track US F1 Visa slot availability data across multiple Visa Application Centers (VACs). By leveraging automated browser orchestration, hardware cursor mapping, and cloud-hosted LPUs via Meta Llama-4 Vision, this system extracts tabular data from live dashboard states, handles anti-ban firewall protection via adaptive PI loop feedback, and triggers multi-channel alarms when target slot thresholds are reached.


## 🛡️ The Claim
### 1. 📉 Mathematical Proof of Convergence (Feedback Latency Loop)
The system operates on the core axiom that the target server’s internal update scheduler follows deterministic, discrete time-series waves ($W$). The closed-loop engine asserts that by calculating the historical progression of table generation gaps ($d_1, d_2$), the exact delta to the subsequent release wave ($T_{next}$) can be bounded and targeted.When an external factor introduces noise—such as regional content delivery network (CDN) caching latency or a local execution delay ($Lag_{capture}$)—the system establishes an error debt metric ($E_{debt}$). By applying this feedback loop directly as a proportional penalty modifier against the target pattern interval, the engine continuously recalibrates itself. 
The engine measures the Data Age ($Age_{data}$) at the exact moment of text extraction. It compares this against a standardized Target Lateness Floor ($\tau = 2.0\text{ minutes}$). The moving average of this error over the last three runs creates our Proportional Error Debt ($E_{debt}$):

This mathematically guarantees that the execution runtime will converge precisely with the server's update horizon:$$T_{run} \to T_{drop} \quad \text{as} \quad E_{debt} \to 0$$

$$E_{debt} = \left( \frac{1}{3} \sum_{i=1}^{3} Age_{data, i} \right) - \tau$$

If $E_{debt} > 0$, the engine calculates a predictive interval ($Interval_{target}$) based on your 3-stamp and 4-stamp gap decoders, subtracts a randomized anti-bot pre-fire buffer ($Lead_{hardware}$), and applies the error debt as a time-shaving penalty:

$$Sleep_{calibrated} = (Interval_{target} - Age_{data} - Lead_{hardware}) - (E_{debt} \times 60)$$

🏎️ The Catch-Up Sprint ($E_{debt} > 0$): The script detects that data is aging. It shaves seconds or minutes off its sleep pool, intentionally launching the next browser window early to catch the next server release wave at the exact moment of injection.

🛑 The Safety Valve Override ($E_{debt} \le 0$): If the script wakes up so fast that it runs before the server updates target_sleep_minutes_temp drops below 2.0 minutes. If the data isn't late, the engine activates its safety valve, expanding the sleep window out by exactly one full server cycle ($+next\_interval\_mins$) to dodge aggressive IP rate-limiting blocks.


### 2. 🧊 The Anti-Entropy Claim (State Space Reset)
The engine claims that state isolation is the only permanent fix for memory entropy. Instead of keeping a single browser instance open and running, the system treats every individual scan as an ephemeral, isolated container. By combining a hard process termination (taskkill /f /im msedge.exe) at the end of every loop with an on-disk JSON patcher (force_clean_session_state), it wipes out structural drift.

[Scan Loop n] ──► Wipes Preferences ──► Launches Process ──► Kills Process ──► [Zero-State Sandbox]
                                                                                      │
[Scan Loop n+1] ◄─────────────────────────────────────────────────────────────────────┘


### 3. ⚡Latency: 
The entire pipeline executes 24x7 in under 20 seconds. It undergoes a rapid LLM Vision check; if the optimization logic confirms a bulk slot drop, it immediately triggers the laptop hardware alarm and simultaneously dispatches a priority notification to the user's personal Telegram.

### 4. 💰 Zero Fee: 
Leverages an ultra-low-cost (virtually $0) infrastructure utilizing Groq's high-speed API endpoints to process thousands of community interactions daily without premium SaaS subscription fees.

### 5. 🕞 24x7: 
Engineered specifically to tackle sudden, high-stakes bulk drops that notoriously occur in the dead of night (2 AM, 3 AM, or later), this system acts as your tireless digital sentinel.



## ✨ Features

# ⚡ LPU-Accelerated Table OCR: 
Drop-in vision engine using meta-llama/llama-4-scout-17b-16e-instruct over Groq Cloud to extract text structures natively to JSON arrays without regex string degradation.

# 🕵️‍♂️ Anti-Detection & Humanized Behavior: 
Patched profile preference overrides that kill restoration bubbles and automate headless runtime instances cleanly. Implements runtime flags like --disable-blink-features=AutomationControlled to hide automation signatures.🖱️ Cubic Bézier Cursor Engine: Mouse paths are generated using non-linear math steps with natural hover micro-wiggles and varied click-hold durations to mirror organic human motor control.

# ✂️ Hardware-Bounded Crop Matrix: 
Dynamically calculates a safe pixel crop bounding window ($Left: 10\%$, $Top: 25\%$, $Right: 90\%$, $Bottom: 95\%$) protecting downstream parsers from dimensional failure or edge corruption.📉 PID-Inspired Proportional Sleep Loops: Feeds parsed webpage lateness statistics directly back into a dynamic feedback tracker to predict server generation updates and optimize sleep cycles.

# 🚨 Simultaneous Background Alarm Routing: 
Multi-threaded execution pipelines that concurrently fire localized motherboard winsound frequencies, instantiate target user authentication page wrappers, and push formatted HTML updates via the Telegram Bot API.


## 🗺️ System Architecture Overview
The system is split into three modular logical layers to protect consumer hardware memory constraints while maximizing processing throughput:

[Live Portal UI] -------> [Stealth Browser Orchestration] -----------> [Raw VRAM Crop Matrix] 
                                                                                │
                                                                                ▼
[High-Intensity Simultaneous Alarm] <- [Dynamic Sleep Optimization] <- [Groq LPU Vision Engine]


### Ingestion Layer (app.py / humanize_browsing.py): 
Drives Microsoft Edge and Google Chrome using native hardware cursor mimicking wrappers (Cubic Bézier trajectory interpolation) to bypass Cloudflare and perimeter anti-bot firewalls.

### Processing Layer (models.py / screenshot.py): 
Crops standard 1080p display bounds directly down to the targeted DOM coordinate element matrix to safeguard local VRAM allocations before converting to localized Base64 payload URIs.

### Analysis & Alerting Layer (alarm.py / dynamic_sleep.py): 
Passes vectorized frames to high-speed cloud infrastructures, converts extracted tables to structured operational DataFrames, evaluates numeric threshold configurations, and simultaneously executes visual, structural, audio, and network-packet push alerts.


## 🚀 Installation & Setup

1. Environment Configurations
Clone this repository directly into your local machine environment directory, then initialize and activate your virtual isolation workspace:

```
python -m venv f1_env
f1_env\Scripts\activate
```
```
pip install -r requirements.txt
```

2. Environment Variables (.env)
Create a standard .env configuration file inside the root execution hierarchy directory path:
```
GROQ_API_KEY=gsk_your_live_production_groq_api_key_here
ALERT_BOT_TOKEN=1234567890:ABC-Your Telegram Alert Bot Token Here
MY_PERSONAL_CHAT_ID=YOUR_TELEGRAM_TARGET_CHAT_ID_HERE
```


## 🛠️ Deep Module Breakdown

### 🤖 1. Humanized Browsing Core (humanize_browsing.py)
Bypasses advanced fingerprinting via raw hardware emulation:

Mathematical Pathing: Uses randomized sub-interval control paths based on the following parameterized matrix to draw smooth mouse coordinates:

$$x(t) = (1-t)^3 x_0 + 3(1-t)^2 t x_1 + 3(1-t) t^2 x_2 + t^3 x_3$$

[fromula.png]

Session Integrity Control: Manipulates local JSON state preferences directly on disk before boot. This forcefully sets exit_type to "Normal" and exited_cleanly to True, permanently supressing Chromium's "Restore Pages" crash notice bubble which offsets target click coordinates.

Thread-Safe Input Locks: Wraps hardware-level cursor calls inside an atomic mouse_lock = Lock() to prevent asynchronous UI workflows from clashing during simultaneous script runs.


### ✂️ 2. Memory Optimization Engine (screenshot.py)
Isolates tabular regions before processing:

VRAM Defense Matrix: Shrinks the footprint of standard high-resolution screenshot images down to exact analytical boundaries.

Defensive Fallbacks: Includes built-in evaluation layers that catch zero-byte corruptions or calculation collapses, defaulting back to safely managed container limits rather than throwing unhandled exceptions.


### 🧠 3. Closed-Loop Timing Calibration Engine (dynamic_sleep.py)

Protects against anti-bot triggers using a predictive time-series model:

Chronological Anomaly Layer: Monitors structural data inconsistencies (such as data-age drops or chronological inversions due to server-side rollbacks). It dynamically catches these issues and maps them onto a standardized, virtual baseline progression.

Multi-Tiered Pattern Recognition: The engine looks back into historical generation timestamps using a 3-stamp and 4-stamp sliding window to map current activity states into specific tracking series:

Series 1: Routine Baseline (10-10-10-8-8) / Reset Trigger Loop (8-8-8-8)
Series 2: Long-Run Cruise Control (6-8-6-8)
Series 3: High-Volume Processing Loop (6-6-6-6)
Series 4: Peak Active Polling (6-4-6-4)
Series 5: Sustained High-Velocity Polling Loop (4-4-4-4)

Moving-Average Feedback Loop: If the systemic average lateness calculation drops below target constraints, the scheduler computes a laggard error penalty to advance the system execution cycle:

$$Sleep_{Calibrated} = (Interval_{Target} - Age_{Data} - Lead_{Hardware}) - Penalty_{Lateness}$$

[formula2.png]

## 📊 Run-Time Diagnostics Matrix
When fully functional, your terminal interface logs diagnostic analytics tracking lookups precisely like this:

```
🚀 Radar Pipeline Active. Monitoring slots in-memory every 10 minutes. Press Ctrl+C to stop.

🎬 Starting scan sequence at: 2026-06-14 16:34:58
🛡️ [Fix] Patched Edge preferences to suppress restore bubble.
🚀 [Thread-Stealth-Edge] Launching anti-detection wrapper for Edge...
🎯 [Stealth-Edge] Acquired UI hardware control cursor...
📸 Success! Saved clean screenshot.
✂️ Cropping the new visa_slots.png to protect 6GB VRAM...
📊 Original Image Metadata -> Width: 1920px, Height: 1080px
✂️ Safe Crop Execution Matrix -> Left: 192, Top: 270, Right: 1728, Bottom: 1026
⚡ Launching high-speed cloud LPU extraction matrix via meta-llama/llama-4-scout-17b-16e-instruct-preview...

   Visa Location      Visa Type Earliest Date Slots on Earliest Date Total Dates Available            Last Seen At      Relative Time
0    HYDERABAD VAC  F-1 (Regular)    29 Jul, 26                    N/A                     3  14 Jun 2026, 03:01 PM   1 hr 33 mins ago
1      KOLKATA VAC  F-1 (Regular)    14 Jul, 26                    N/A                     9  14 Jun 2026, 03:26 PM    1 hr 8 mins ago

ℹ️ No target VAC drops found. Sending test status ping to Telegram...

⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
🎯 ENGINE STATUS           : Series 1: Routine Baseline (10-10-10 Ongoing)
   • Rolling Hourly Scans    : 6 hits in last 60m
   • Last Table Gen Time     : 04:32 PM
   • Current Data Age        : 6.63 minutes old
   • Next Predicted Drop      : +10 minutes
   • Active Feedback Shift   : Shaved 0.00 seconds
   • PURE SLEEP CALIBRATION  : 112.20 seconds
⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡

⏳ Sleeping for 2.00 minutes until next engine check...
```

## 📝 Generated Log Outputs
The pipeline populates telemetry metrics natively into two target log architectures:

check_us_visa_history.log: Standard operational time trace matrix recording framework milestones:

```
[2026-06-14 16:34:58] ▶️ Start
[2026-06-14 16:35:04] 📸 Screenshot Success -> Runtime -> 0.10 mins
[2026-06-14 16:35:12] 🔮 Model Ran -> Runtime -> 0.13 mins | Gen Time: 14 Jun 2026 16:32:00 | Total Current Lateness: 3.20 mins old
[2026-06-14 16:35:12] ⏳ Loop Synchronized -> Predicted Server Step: +10m | Pure Capture Lag: 0.23m | Scheduled Sleep: 2.00 mins
[2026-06-14 16:35:12] ⏹️ Ends
```

## ⚖️ License & Disclaimers

This software is compiled solely for educational exploration, performance profiling, and research tracking optimizations. Ensure any live monitoring execution frequencies fully comply with target platform Terms of Service (ToS) and host rate-limiting infrastructure standards.