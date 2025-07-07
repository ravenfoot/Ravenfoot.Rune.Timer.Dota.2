CONTENTS:

1. About
2. Features.
3. Code Overview.
4. Installation and Usage details, including optional steps for packaging with PyInstaller and NSIS.
5. Resource Acknowledgements for sounds and images.
6. References to ChatGPT prompts and code changes (relative vs. absolute paths).
7. Disclaimer & License
8. Contact.

1. About:

A simple Python application that alerts players to upcoming rune spawns, Roshan timers, and day/night cycles in Dota 2. 
It displays both audio (WAV) alerts and an optional visual overlay for critical rune spawn times.

2. Features:

Rune Timers: Bounty, Water, Wisdom, and Power runes.
Roshan Timer: Triggers every 10 minutes.
Day/Night Timer: Cycles every 5 minutes, with alerts 15 seconds beforehand.
Audio Alerts: Uses .wav files played via pygame.
Visual Overlay: Displays top-center PNG images for major runes (optional if in borderless/windowed mode).

3. Code Overview:

a. main.py: Entry point that initializes timers and the main GUI window.

b. gui/gui.py: Manages the primary Qt interface, including the timer label and user buttons.

c. timers/:
rune_timer.py: Tracks Bounty, Power, Wisdom, Water runes.
roshan_timer.py: Tracks Roshan spawn intervals.
daynight_timer.py: Day→Night cycle transitions every 5 minutes.

d. utils/:
sound_manager.py: Handles audio playback (pygame).

e. overlay_manager.py: Displays top-center PNG overlays for runes.

f. game_focus.py: Brings Dota 2’s window to the front (if desired).

g. path_utils.py: Provides resource_path() to handle data files in PyInstaller onefile builds.


4. Installation & Usage:

a. Run from Source
    1. Clone or Download this repository into a directory (e.g., Dota_2_Timer).

    2. Install Dependencies:
~ pip install -r requirements.txt ~

    3. Run.
~ python main.py ~

The Qt application window should open.
Press Start to begin the timer.

b. Build a Single .exe with PyInstaller (Optional)
If you want a self-contained Windows .exe:

    1. Install PyInstaller:
~ pip install pyinstaller ~

    2. Compile
pyinstaller --onefile --windowed --icon "assets/icons/timer_icon.ico" --add-data "assets;assets" --add-data "sounds;sounds" --add-data "gui;gui" main.py

    3. Check dist/ Folder:
You should see a Dota2Timer.exe. Double-click to test.

c. Create a Windows Installer with NSIS (Optional)

    1. Install NSIS from nsis.sourceforge.io.
    2. Create Dota2Timer.nsi script in an installer/ folder.
    3. Compile with NSIS → produces Dota2Timer_Installer.exe.
    4. Distribute Dota2Timer_Installer.exe to friends.


5. Resource Acknowledgements

Sound Effects: Obtained from myinstants.com under the Sound Effects category. Each .wav file is included in the sounds/ folder.
Icons and PNG Artwork: Created by Raul L. (S0fty) using Affinity Designer. This includes timer_icon.ico, bounty_soon.png, power_soon.png, etc.

PyInstaller: For bundling Python scripts into an .exe.

NSIS (Nullsoft Scriptable Install System): For building a Windows installer with a standard uninstaller and user-selectable install paths.


6. ChatGPT: Used to help refine code structure, handle relative paths vs. _MEIPASS logic in PyInstaller, and provide modular design suggestions.

e.g. Input Relative vs. Absolute Paths

A key modification supported by ChatGPT was the introduction of a utils/path_utils.py and the function resource_path(...) to ensure that assets and sounds load properly in both:
Normal Python runs (local file structure).
PyInstaller onefile mode (where _MEIPASS is used).


7. Disclaimer & License:

This project is not affiliated with or endorsed by Valve or Dota 2.

For personal/educational use—no warranties are provided regarding game modifications or usage in official tournaments.

License: MIT License

8. Contact:

Developer: S0fty
For questions, you can reach out via GitHub
Any use or modification should appropiately reference S0fty
