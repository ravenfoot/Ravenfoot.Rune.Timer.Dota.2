#!/usr/bin/env python3
"""
DOTA 2 P100 — Teletext Timer (Professional Edition v1.3)

Goal:
- Provide an always-on-top Teletext-styled timer for Dota 2.
- Handles precise offsets for runes/Roshan.
- Supports different start times (Normal/Bots/Turbo).

Design notes:
- Cross-platform: Windows focus via Win32 APIs; Linux focus via PID -> xdotool.
- Packaging-friendly: resource_path supports both dev and PyInstaller.
- Fail-soft: Optional sound/overlay support.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import font
from pathlib import Path

# ------------------------------------------------------------
# Optional dependency: pygame for sound alerts
# ------------------------------------------------------------
try:
    import pygame  # type: ignore
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False
    print("Warning: 'pygame' not found. Sounds disabled.")


# ============================================================
# 1) CONFIGURATION & PALETTE
# ============================================================

COL_BG     = "#000000"
COL_FG     = "#FFFFFF"
COL_CYAN   = "#00FFFF"
COL_YELLOW = "#FFFF00"
COL_RED    = "#FF0000"
COL_GREEN  = "#00FF00"
COL_BLUE   = "#0000FF"
COL_GREY   = "#444444"

class GameConfig:
    """
    CENTRAL CONFIGURATION FOR TIMINGS AND OFFSETS
    Adjust these values as patches change.
    """
    
    # --- START TIMES (Negative seconds before 00:00) ---
    START_NORMAL = -90
    START_BOTS   = -75
    START_TURBO  = -60

    # --- OFFSETS (How many seconds BEFORE event to warn) ---
    OFFSET_WISDOM = 5   # Warn 5s early
    OFFSET_BOUNTY = 8   # Warn 8s early
    OFFSET_POWER  = 11  # Warn 11s early
    OFFSET_WATER  = 14  # Warn 14s early
    OFFSET_ROSHAN = 17  # Warn 17s early
    OFFSET_DAYNIGHT = 15 # Warn 15s early (except 00:00)

    # --- INTERVALS (Seconds) ---
    INT_WISDOM = 420    # 7 minutes
    INT_BOUNTY = 240    # 4 minutes (per user request)
    INT_POWER  = 120    # 2 minutes
    INT_ROSHAN = 600    # 10 minutes
    INT_DAYNIGHT = 300  # 5 minutes

    # --- FIRST SPAWN TIMES (Seconds) ---
    # When does the FIRST cycle begin?
    START_WISDOM = 420  # 07:00
    START_BOUNTY = 240  # 04:00 (per user request)
    START_POWER  = 360  # 06:00
    START_ROSHAN = 600  # 10:00


def resource_path(*parts: str) -> str:
    """Resolve resource files reliably for Dev and PyInstaller."""
    base = getattr(sys, "_MEIPASS", Path(__file__).parent.absolute())
    return str(Path(base, *parts))


# ============================================================
# 2) WINDOW FOCUS ENGINE
# ============================================================

def focus_dota_window() -> None:
    """
    Robust Cross-Platform Focus Switcher
    """
    # --- WINDOWS (Unchanged) ---
    if os.name == "nt":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = user32.FindWindowW(None, "Dota 2")
            if hwnd:
                if user32.IsIconic(hwnd):
                    user32.ShowWindow(hwnd, 9) # Restore if minimized
                user32.SetForegroundWindow(hwnd)
        except Exception:
            pass
        return

    # --- LINUX (Optimized for Mint/Cinamon/Gnome) ---
    try:
        # STRATEGY 1: Direct Window Name Search (Fastest)
        # We look for a window named exactly "Dota 2".
        # 'timeout=1' prevents indefinite hanging.
        res = subprocess.run(
            ["xdotool", "search", "--name", "^Dota 2$"], 
            capture_output=True, text=True, timeout=1
        )
        
        # If we got a window ID back, activate it immediately.
        if res.stdout.strip():
            win_id = res.stdout.strip().split()[-1] # Take the last one found
            subprocess.run(["xdotool", "windowactivate", win_id], timeout=1)
            return

        # STRATEGY 2: PID Hunter (The "Heavy" Fallback)
        # Only runs if Strategy 1 fails. 
        # We limit the PIDs to the binary name 'dota2' to avoid grabbing 
        # generic 'steam' or 'sh' wrappers which cause hangs.
        pid_res = subprocess.run(
            ["pgrep", "-x", "dota2"], # -x matches exact binary name, not full command line
            capture_output=True, text=True, timeout=1
        )
        
        pids = pid_res.stdout.strip().split()
        for pid in pids:
            # Check if this PID owns a window
            win_res = subprocess.run(
                ["xdotool", "search", "--pid", pid],
                capture_output=True, text=True, timeout=0.5 # Strict 0.5s timeout per PID
            )
            if win_res.stdout.strip():
                win_id = win_res.stdout.strip().split()[-1]
                subprocess.run(["xdotool", "windowactivate", win_id], timeout=1)
                return

    except subprocess.TimeoutExpired:
        print("[Linux] Window switch timed out.")
    except Exception as e:
        print(f"[Linux] Switch failed: {e}")


# ============================================================
# 3) SOUND ENGINE
# ============================================================

class SoundEngine:
    def __init__(self) -> None:
        self.sounds = {}
        if not HAS_SOUND: return
        try:
            pygame.mixer.init()
            # Define file mapping
            files = {
                "bounty": "bounty_rune.wav", "power": "power_rune.wav",
                "water": "water_rune.wav",   "wisdom": "wisdom_rune.wav",
                "roshan": "roshan_rune.wav", "day": "day.wav", "night": "night.wav"
            }
            for name, f in files.items():
                p = resource_path("sounds", f)
                if os.path.exists(p): self.sounds[name] = pygame.mixer.Sound(p)
        except Exception as e:
            print(f"[Sound] Init failed: {e}")

    def play(self, name: str) -> None:
        if HAS_SOUND and name in self.sounds:
            try:
                self.sounds[name].play()
            except: pass


# ============================================================
# 4) OVERLAY WINDOW (Linux Shadow Fix / Windows Chroma)
# ============================================================

class Overlay(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        # --- STRATEGY: CHROMA KEY (Windows) vs HUD CARD (Linux) ---
        self.chroma_key = "#ff00ff"  # Magenta
        
        if os.name == "nt":
            # WINDOWS: Transparent cutout
            self.config(bg=self.chroma_key)
            try: self.attributes("-transparentcolor", self.chroma_key)
            except: pass
            
            self.container = self
            bg_color = self.chroma_key

        else:
            # LINUX: Teletext HUD Style (Cyan Border)
            self.config(bg=COL_CYAN) # Border color
            
            # Use 'splash' type hint to avoid Cinnamon shadows
            try: self.attributes("-type", "splash")
            except: pass
            
            # Use 1.0 alpha to avoid compositor "ghost box" effects
            try: self.attributes("-alpha", 1.0)
            except: pass

            # Inner black frame (creates border effect)
            self.container = tk.Frame(self, bg="#000000")
            self.container.pack(fill="both", expand=True, padx=2, pady=2)
            bg_color = "#000000"

        self.withdraw()

        self.label = tk.Label(
            self.container, 
            bg=bg_color, 
            bd=0, 
            highlightthickness=0
        )
        self.label.pack()
        self._img_ref = None

    def show_alert(self, image_name: str) -> None:
        path = resource_path("assets", "warnings", image_name)
        if not os.path.exists(path): return

        try:
            img = tk.PhotoImage(file=path)
            
            # REMOVED: img.subsample(2, 2)
            # Displaying native resolution now.
            
            self._img_ref = img
            self.label.config(image=img)

            w = img.width()
            h = img.height()
            
            # Add padding for the Linux border calculation
            if os.name != "nt":
                w += 4
                h += 4
            
            screen_w = self.winfo_screenwidth()
            x_pos = (screen_w // 2) - (w // 2)
            
            self.geometry(f"{w}x{h}+{int(x_pos)}+50")
            
            self.deiconify()
            self.after(5000, self.withdraw)
        except Exception as e:
            print(f"[Overlay] Error: {e}")

            
# ============================================================
# 5) MAIN APP (Grid Layout + Precise Events)
# ============================================================

class TeletextTimer(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("DOTA 2 Timer P100")
        self.config(bg=COL_BG)
        # Slightly taller to accommodate mode buttons
        self.geometry("400x420") 
        
        # Load Icon
        try:
            if os.name == "nt":
                ico = resource_path("assets", "icons", "ravenfoot_logo.ico")
                if os.path.exists(ico): self.iconbitmap(ico)
            else:
                png = resource_path("assets", "icons", "ravenfoot_logo.png")
                if os.path.exists(png): self.iconphoto(True, tk.PhotoImage(file=png))
        except: pass

        self.sound_engine = SoundEngine()
        self.overlay = Overlay(self)
        
        # Defaults
        self.game_time = GameConfig.START_NORMAL
        self.selected_start_time = GameConfig.START_NORMAL
        self.running = False
        
        self.setup_gui()

    def setup_gui(self) -> None:
        # Fonts
        f_header = font.Font(family="Courier New", size=20, weight="bold")
        f_timer  = font.Font(family="Courier New", size=48, weight="bold")
        f_mid    = font.Font(family="Courier New", size=14, weight="bold")
        f_btn    = font.Font(family="Courier New", size=10, weight="bold")

        # --- Header ---
        header = tk.Frame(self, bg=COL_BLUE, height=40)
        header.pack(fill="x")
        tk.Label(header, text="P100 DOTA", fg=COL_YELLOW, bg=COL_BLUE, font=f_header).pack(pady=5)

        # --- Timer Display ---
        self.lbl_time = tk.Label(self, text=self.format_time(self.game_time), font=f_timer, fg=COL_GREEN, bg=COL_BG)
        self.lbl_time.pack(pady=10)

        # --- Status Line ---
        self.lbl_status = tk.Label(self, text="SELECT MODE", font=f_mid, fg=COL_CYAN, bg=COL_BG)
        self.lbl_status.pack(pady=5)

        # --- Mode Selection (Grid) ---
        mode_frame = tk.Frame(self, bg=COL_BG)
        mode_frame.pack(pady=10)
        
        # Helper to highlight selected mode
        self.btn_modes = {}

        def set_mode(val, name):
            self.selected_start_time = val
            self.game_time = val
            self.lbl_time.config(text=self.format_time(self.game_time))
            self.lbl_status.config(text=f"MODE: {name}")
            # Visual feedback on buttons
            for k, btn in self.btn_modes.items():
                if k == name: btn.config(bg=COL_GREEN, fg=COL_BG)
                else:         btn.config(bg=COL_GREY, fg=COL_FG)

        modes = [("NORMAL", GameConfig.START_NORMAL), ("BOTS", GameConfig.START_BOTS), ("TURBO", GameConfig.START_TURBO)]
        
        for i, (name, val) in enumerate(modes):
            b = tk.Button(mode_frame, text=name, font=f_btn, width=8,
                          bg=COL_GREY, fg=COL_FG,
                          command=lambda v=val, n=name: set_mode(v, n))
            b.grid(row=0, column=i, padx=5)
            self.btn_modes[name] = b

        # Set default Normal
        set_mode(GameConfig.START_NORMAL, "NORMAL")

        # --- Action Buttons ---
        action_frame = tk.Frame(self, bg=COL_BG)
        action_frame.pack(side="bottom", fill="x", pady=20, padx=10)

        def make_action(txt, col, cmd):
            f = tk.Frame(action_frame, bg=col, padx=2, pady=2)
            f.pack(side="left", expand=True, fill="x", padx=2)
            tk.Button(f, text=txt, bg=COL_BG, fg=col, command=cmd, 
                      relief="flat", font=f_btn).pack(fill="both")

        make_action("START", COL_GREEN, self.start_timer)
        make_action("GAME",  COL_FG,    focus_dota_window)
        make_action("RESET", COL_RED,   self.reset_timer)
        make_action("QUIT",  COL_CYAN,  self.quit)

    def format_time(self, seconds: int) -> str:
        sign = "-" if seconds < 0 else ""
        m, s = divmod(abs(seconds), 60)
        return f"{sign}{m:02d}:{s:02d}"

    def start_timer(self) -> None:
        if not self.running:
            self.running = True
            self.lbl_status.config(text="RUNNING", fg=COL_GREEN)
            focus_dota_window() # Auto-switch
            self.tick()

    def reset_timer(self) -> None:
        self.running = False
        self.game_time = self.selected_start_time
        self.lbl_time.config(text=self.format_time(self.game_time))
        self.lbl_status.config(text="RESET", fg=COL_RED)

    def tick(self) -> None:
        if self.running:
            self.game_time += 1
            self.lbl_time.config(text=self.format_time(self.game_time))
            self.check_events(self.game_time)
            # Use 1000ms. Drift is negligible for this purpose.
            self.after(1000, self.tick)

    # ------------------------------------------------------------
    # EVENT LOGIC (Modular Arithmetic with Offsets)
    # ------------------------------------------------------------
    def check_events(self, t: int) -> None:
        cfg = GameConfig
        
        # 1. SPECIAL CASE: 00:00 (Start of Day)
        if t == 0:
            self.sound_engine.play("day")
            self.lbl_status.config(text="DAY / MATCH START", fg=COL_YELLOW)
            return

        # 2. DAY/NIGHT CYCLE (Every 5 mins)
        # Warning at (Interval - Offset), e.g., 4:45, 9:45
        # We use modulo math to find if we are 'Offset' seconds away from the next 5min mark.
        if t > 0:
            time_until_flip = cfg.INT_DAYNIGHT - (t % cfg.INT_DAYNIGHT)
            if time_until_flip == cfg.OFFSET_DAYNIGHT:
                # Calculate what comes next. 
                # If current cycle is 0-5 (Day), next is Night.
                cycle_count = (t // cfg.INT_DAYNIGHT)
                is_currently_day = (cycle_count % 2 == 0)
                
                # If currently Day, Night is soon.
                next_is_day = not is_currently_day
                
                cue = "day" if next_is_day else "night"
                txt = "DAY SOON" if next_is_day else "NIGHT SOON"
                col = COL_YELLOW if next_is_day else COL_BLUE
                
                self.sound_engine.play(cue)
                self.lbl_status.config(text=txt, fg=col)

        # 3. WISDOM RUNES (Every 7m, Start 7:00)
        # Logic: Must be past start time OR approaching start time
        # Formula: (Time + Offset) % Interval == 0? 
        # But we must ensure t >= (Start - Offset)
        if t >= (cfg.START_WISDOM - cfg.OFFSET_WISDOM):
            # Check if we are exactly at the warning moment
            if (t + cfg.OFFSET_WISDOM) % cfg.INT_WISDOM == 0:
                self.trigger_alert("wisdom", "wisdom_soon.png")

        # 4. BOUNTY RUNES (Start 4:00, Every 4m)
        if t >= (cfg.START_BOUNTY - cfg.OFFSET_BOUNTY):
            if (t + cfg.OFFSET_BOUNTY) % cfg.INT_BOUNTY == 0:
                self.trigger_alert("bounty", "bounty_soon.png")

        # 5. POWER RUNES (Start 6:00, Every 2m)
        if t >= (cfg.START_POWER - cfg.OFFSET_POWER):
            if (t + cfg.OFFSET_POWER) % cfg.INT_POWER == 0:
                self.trigger_alert("power", "power_soon.png")

        # 6. WATER RUNES (Fixed: 2:00 and 4:00 only)
        # Hardcoded because they don't loop forever.
        # Warnings at 1:46 (106s) and 3:46 (226s) given 14s offset.
        water_times = [120, 240] 
        for wt in water_times:
            if t == (wt - cfg.OFFSET_WATER):
                self.trigger_alert("water", "water_soon.png")

        # 7. ROSHAN (Start 10:00, Every 10m)
        if t >= (cfg.START_ROSHAN - cfg.OFFSET_ROSHAN):
            if (t + cfg.OFFSET_ROSHAN) % cfg.INT_ROSHAN == 0:
                self.trigger_alert("roshan", None) # No image for Rosh

    def trigger_alert(self, sound: str, img_name: str | None) -> None:
        self.sound_engine.play(sound)
        if img_name:
            self.overlay.show_alert(img_name)
        # Update status text temporarily
        self.lbl_status.config(text=f"{sound.upper()} SOON", fg=COL_RED)

if __name__ == "__main__":
    app = TeletextTimer()
    app.mainloop()