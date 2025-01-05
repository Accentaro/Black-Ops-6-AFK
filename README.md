# AFK Black Ops 6 Bot

![In Game Image](readme-imgs/ingame.png)

## Overview

Advanced automation bot for Black Ops 6. Simulates human-like behavior by performing mouse movements, keyboard actions, and screen detections, allowing you to stay active in the game.

The script is fully configurable and utilizes Python libraries like 'pynput`, `pyfiglet`, `cv2` (OpenCV), and `pyautogui` to handle inputs, screen detection, and automation.

**Use in modes that won't negatively affect other players: FFA, 10v10, Stakeout 24/7**
---

## Features

1. **Mouse Control**
   - Perform relative mouse movements like 180°, 360°, or random turns.
   - Simulate smooth and dynamic cursor movements for more accurate human-like behavior.

2. **Keyboard Actions**
   - Execute common in-game commands such as Sprint, Slide, Crouch, Jump, and Inspect.
   - Randomize actions for unpredictable, human-like behavior.

3. **Screen Detection**
   - Detect in-game UI elements such as mini map, kill feed, or match in progress icon using OpenCV template matching.
   - Automate responses to specific screen events like skipping kill cams or selecting loadouts.
![Killcam](readme-imgs/killcam.png)

4. **Recovery Mechanism**
   - Automatically rejoin matches if kicked or disconnected, with predefined mouse-click actions.
![Kicked](readme-imgs/kicked.png)

5. **Dynamic Status**
   - Automatic Pause in menu and Resume in game
   - Monitors in-game activity and adjusts behavior accordingly.
   ![Menu](readme-imgs/menu.png)

---

## Prerequisites

1. **Python Libraries**  
   Install the required libraries:
   pip install requirements.txt
   or
   pip install pynput pyfiglet opencv-python pyautogui numpy pillow

2. **Image References**
Ensure the cv references folder is installed. It contains the necessary reference images for in-game detection under cv references/in game/ and cv references/game results/

3. **Screen Resolution**
Ensure your screen resolution matches the coordinates used in the script. Modify the regions if needed.

## How to Use
- Clone or download this repository.
- Follow Prerequisites
- Run the script: afk.py
- Follow on-screen instructions to enable or disable mouse movements.

  
## Important Notes
- Customization: Adjust mouse sensitivity, regions, and thresholds for screen detection in the script as needed.
- Safety: Use responsibly and comply with the terms of the game.
- Supported Platforms: Windows is required due to dependencies like ctypes.

## Acknowledgments
Creator: Caden Warren
Libraries Used: pynput, pyfiglet, opencv-python, pyautogui, numpy.
