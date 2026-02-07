<h5><code>#!/usr/bin/env markdown</code><br>
<code>#==============================================================================</code><br>
<code># 🎮 RAVENFOOT RUNE TIMER — DOTA 2 (P100 Teletext Edition)</code><br>
<code>#==============================================================================</code><br>
<code># Purpose: Rune / Roshan / Day-Night alerts with a retro Teletext UI.</code><br>
<code># Audience: Players • Reviewers • Hiring managers (portfolio-ready)</code><br>
<code># Stack: Python · Tkinter · pygame (optional) · (Linux optional) xdotool</code><br>
<code># Version: v2.1.0 (Legacy)</code><br>
<code># License: Apache-2.0</code><br>
<code># Status: Stable / Archived / Learning Project</code><br>
<code># Author: Ravenfoot</code><br>
<code>#==============================================================================</code></h5>

---

## 0. 🧬 Ravenfoot projects

* **a)** [Ravenfoot Calculator (Legacy)](https://github.com/ravenfoot/Ravenfoot.Calculator.Legacy.Edition)
* **b)** [Ravenfoot Passwords — P100 (Teletext Edition)](https://github.com/ravenfoot/Ravenfoot.Passwords.P100.Teletext-Edition)
* **c)** [Ravenfoot Rune Timer (Dota 2)] <--- You are here
* **d)** [Ravenfoot NAS Automation (Bash Edition)](https://github.com/ravenfoot/Ravenfoot.NAS.Automation.Bash.Edition)
* **e)** [Ravenfoot Webpage](https://github.com/ravenfoot/Ravenfoot.Webpage)
* **f)** [Ravenfoot Scryer — AoW Overlay (Stage 1)](https://github.com/ravenfoot/Ravenfoot.Scryer.AoW.Overlay.1)


---

## 1. Contents:


* **🕵️ The Mission**
* **⚡ Capabilities**
* **🧱 Project Layout**
* **🔄 Refactor Notes**
* **📦 Packaging (Build It or Download)**
* **🧰 Troubleshooting**
* **🙏 Credits & Assets**

---

## 2. 🕵️ The Mission

**Ravenfoot Rune Timer — P100** is a lightweight companion app for **Dota 2** that gives you **pre-warnings** for:
* **Bounty runes**
* **Water runes**
* **Power runes**
* **Wisdom runes**
* **Roshan reminder**
* **Day / Night cycle changes**

* It’s intentionally **minimal**, **high-contrast**, and designed so you can: keep it on a second monitor, **or**
* run it “background-y” while playing (sound cues + overlay cards).

---

## 3. ⚡ Capabilities

**Controls:**

* **START** → starts the timer and (optionally) tries to focus Dota 2
* **GAME** → manual “switch to Dota 2” button (focus engine)
* **RESET** → back to **-01:15**
* **QUIT** → exits cleanly

**Game Mode Options:**

* **NORMAL** → 90S Countdown
* **BOTS** → 75s Countdowm
* **TURBO** → 60s Countdown

- **3.1 ⏱️ Timing model (human-friendly)**
* Starts at **GAME MODE CHOICE** to match **day-horn** flow.
* Uses Tkinter’s `after(1000, ...)` loop (simple + thread-free).
* Uses modular arithmetic for recurring events (readable + scalable).

- **3.2 🔊 Audio alerts (optional)**
* **WAV cues**via `pygame.mixer`
* **Fail-soft:** if `pygame` isn’t installed, the app still runs (silently)

- **3.3 🖼️ Overlay cards (optional but spicy)**
* **Displays:** a top-center warning PNG for key rune events.
* **Windows:** "Invisible Ink" transparency (Chroma Key) for perfect cutouts.
* **Linux:** "HUD Card" style (Cyan border) with optional transparency (avoids "Black Box" artifacts). ⚠️ Note it's a feature, not a bug! - side steps opacity nightnare in Tkinter ⚠️

- **3.4 🎯 “Focus Dota 2” helper (cross-platform)**
* **Windows:** fast WinAPI `FindWindowW("Dota 2")`
* **Linux:** Hybrid Strategy (Fast --name search → Fallback to PID hunter pgrep if needed).
* **Zero Hangs:** Includes strict timeouts to prevent freezing on Linux Mint/Gnome.

---

## 4. 🧱 Project Layout

Directory structure (v1.3):

```text
.
├── assets/
│   ├── icons/
│   │   ├── ravenfoot_logo.ico
│   │   └── ravenfoot_logo.png
│   └── warnings/
│       ├── bounty_soon.png
│       ├── power_soon.png
│       ├── water_soon.png
│       └── wisdom_soon.png
├── sounds/
│   ├── bounty_rune.wav
│   ├── power_rune.wav
│   ├── water_rune.wav
│   ├── wisdom_rune.wav
│   ├── roshan_rune.wav
│   ├── day.wav
│   └── night.wav
├── dota2_timer.py
└── requierments.txt
```
Design choice: **single-file app** with clearly separated “sections” inside the file:

 1) CONFIGURATION & PALETTE
 2) WINDOW FOCUS ENGINE
 3) SOUND ENGINE
 4) OVERLAY WINDOW (Linux Shadow Fix / Windows Chroma)
 5) MAIN APP (Grid Layout + Precise Events)

That’s deliberate: easy to audit, easy to package, easy to clone + run.

---

## 5. 🔄 Evolution: v1.0 → v2.1.0 (Refactor Notes)

This repo is intentionally presented as a clean evolution rather than a “magic final drop”.

- **5.1 v1.0 baseline**

* Teletext Tkinter UI ✅
* Basic Rune / Roshan logic ✅
* pygame audio ✅

- **5.2 v2.1.0 refactor (Professional Edition)**

* **Fail-soft dependencies:** pygame is optional; app runs silently if missing.
* **Robust resource loading:** Uses .absolute() to solve VirtualBox/Windows shared drive path errors.
* **Explicit Garbage Collection:** Retains PhotoImage references to prevent blank overlays.

- **5.3 v2.1.0 upgrade (The "Polished" Edition)**

* **Multi-Mode Start:** Added buttons for Normal (-90s), Bots (-75s), and Turbo (-60s).
* **Precision Timings:** Specific offsets for every rune type (e.g., Water Runes at 2:00/4:00 only).
* **Hybrid Focus Engine (Linux):** Now uses a fast --name search first, falling back to a "PID Hunter" only if needed. Includes strict timeouts to prevent hanging on Linux Mint/Gnome.

**Smart Overlays:**

* **Windows:** "Invisible Ink" (Chroma Key) for perfect shaped cutouts.
* **Linux:** "HUD Card" style (Cyan border)

---

## 6. 📦 Packaging (Build It)

- **6.1 Windows: Create Installer (Inno Setup)**

We use PyInstaller to freeze the code and Inno Setup to create a professional setup.exe.

**Windows:**

**a) Create a Fresh Venv**

```PowerShell
python -m venv venv
.\venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

**b) Freeze the binary (Folder Mode):**

```PowerShell
pyinstaller --noconfirm --onedir --windowed --clean --name "Ravenfoot_Timer" --icon "assets/icons/ravenfoot_logo.ico" --add-data "assets;assets" --add-data "sounds;sounds" dota2_timer.py
```

**c) Compile Installer:**

Open build_installer.iss (provided in repo) with Inno Setup Compiler.

Click Build.

Output: Output/Ravenfoot_Timer_Setup_v1.2.exe.



- **6.2 Linux: Create .deb Package**

**a) Create a Fresh Venv**

```Bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

**b) Freeze the binary (Single File):**

```Bash
pyinstaller --noconfirm --onedir --windowed --clean \
  --name "ravenfoot-timer" \
  --add-data "assets:assets" \
  --add-data "sounds:sounds" \
  dota2_timer.py
```
Build .deb:

**c) Structure your deb_package folder**

e.g.

```
mkdir -p deb_package/DEBIAN
mkdir -p deb_package/opt/ravenfoot-timer
mkdir -p deb_package/usr/share/applications
mkdir -p deb_package/usr/share/icons/hicolor/256x256/apps
mkdir -p deb_package/usr/share/icons/hicolor/64x64/apps
```

```copy
cp -a dist/ravenfoot-timer/* deb_package/opt/ravenfoot-timer/
cp assets/icons/ravenfoot_logo.png deb_package/usr/share/icons/hicolor/256x256/apps/ravenfoot-timer.png
cp assets/icons/ravenfoot_logo.png deb_package/usr/share/icons/hicolor/64x64/apps/ravenfoot-timer.png
```

**d) Build .deb***

Run: dpkg-deb --build deb_package ravenfoot-timer_1.4_amd64.deb.


--**OR**--

just download:

**🐧 Linux (.deb)**

* **a)** [Ravenfoot Passwords — P100 (Teletext Edition)](https://github.com/ravenfoot/Ravenfoot.Calculator.Legacy.Edition/releases/download/Linux_Software_Package/ravenfoot-calc.deb)

**🪟 Windows (.exe)**

* **b)** [Ravenfoot Passwords — P100 (Teletext Edition)](https://github.com/ravenfoot/Ravenfoot.Calculator.Legacy.Edition/releases/tag/Windows_Executable_Binary)

**🪟 Windows (portable)**

* **b)** [Ravenfoot Passwords — P100 (Teletext Edition)](https://github.com/ravenfoot/Ravenfoot.Calculator.Legacy.Edition/releases/tag/Windows_Executable_Binary)

## 7. 🧰 Troubleshooting

- **7.1 No sound**
Ensure pygame is installed: pip install pygame

Check system audio mixer (ensure Python/App isn't muted).

- **7.2 Linux: "GAME" button doesn't focus Dota**
Required Tool: Install xdotool.

```Bash
sudo apt install xdotool
Wayland Users: Focus stealing is often blocked by security policies in Wayland. Use an X11 session if this feature is critical.
```

- **7.3 Overlay looks like a black box (Linux)**
This is a known limitation of X11/Tkinter transparency.

Feature, not bug: In v2.1.0, we style this as a "Cyan HUD Card" with 60% transparency ("Ghost Mode") to ensure the map is still visible through the background.

7.4 False Positive "Virus Detected"
Antivirus heuristics often flag un-signed PyInstaller bootloaders.

Fix: Whitelist the folder locally. When distributing, providing a signed installer or hash checksums helps users trust the file.

## 8. 🙏 Credits & Assets

Sound cues: Included under sounds/ (WAV format) from https://www.myinstants.com/en/categories/sound%20effects/.

Icons + warning PNGs: Custom made using Adobe Illustrator.

Dota 2: Trademark of Valve — this project is not affiliated with Val


<code>#==============================================================================</code><br>
<code>#🛑 END</code><br>
<code>#==============================================================================</code></h5>
