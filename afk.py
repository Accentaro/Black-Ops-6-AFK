import atexit
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController, Listener
import random
import time
from pyfiglet import Figlet
import os
import cv2 as cv
import pyautogui
import numpy as np
import ctypes

mouse = MouseController()
keyboard = KeyController()
format = Figlet(font='Big')
user32 = ctypes.windll.user32

# Mouse Movements with Ctypes
MOUSEEVENTF_MOVE = 0x0001

# Get screen resolution
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Set Paused at Start
paused = True
force_paused = False


GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
RESET = "\033[0m"

creator = "Created By - Caden Warren"

mouse_command_list = ["180", "360", "720", "90Left", "90Right", "45Left", "45Right", "RandomTurnSmall"]
key_command_list = ["Sprint", "SlideR", "SlideL", "Crouch", "LayDown", "Back", "Inspect", "Jump", "Slide", "SlideBack"]
mouse_click_list = ["Shoot", "Aim", "Both"]

# not yet implemented
winner_quotes = ["Winner!", "You Won!", "Victory!"]
loser_quotes = ["Defeated", "You Lost.. But if it makes you feel better your team probably hates you", "L"]

# Mouse Movement in Game
def move_mouse_relative(dx, dy):
    """Move the mouse relative to its current position."""
    user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)

def do_mouse_command(command):
    """Execute mouse movement commands."""
    if command == "180":
        print("Performing 180-degree turn")
        move_mouse_relative(500, 0)  # Adjust values for a 180-degree turn
    elif command == "360":
        print("Performing 360-degree turn")
        move_mouse_relative(1000, 0)  # Adjust values for a 360-degree turn
    elif command == "90Left":
        print("Performing 90-degree left turn")
        move_mouse_relative(-250, 0)  # Adjust values for a 90-degree left turn
    elif command == "90Right":
        print("Performing 90-degree right turn")
        move_mouse_relative(250, 0)  # Adjust values for a 90-degree right turn
    else:
        print("Unknown mouse command")


# In Game Screen Detection
compass = cv.imread('cv references/in game/compass.png')
killcam = cv.imread('cv references/in game/killcam.png')
killfeed = cv.imread('cv references/in game/killfeed.png')
match_start= cv.imread('cv references/in game/match start.png')
match_in_progress_logo = cv.imread('cv references/in game/match in progress.png')
mini_map = cv.imread('cv references/in game/mini map.png')
packet_burst = cv.imread('cv references/in game/packet burst.png')
packet_burst_2 = cv.imread('cv references/in game/packet burst 2.png')
score = cv.imread('cv references/in game/score.png')
scorestreaks = cv.imread('cv references/in game/scorestreaks.png')
ui = cv.imread('cv references/in game/UI.png')
compass_player = cv.imread('cv references/in game/compass player.png')
AR_ammo = cv.imread('cv references/in game/AR ammo.png')

# not yet implemented
defeat = cv.imread('cv references/game results/Defeat.png')
victory = cv.imread('cv references/game results/Victory.png')

images_to_detect = [
    compass, 
    killcam,  
    killfeed,
    match_start, 
    match_in_progress_logo, 
    mini_map, 
    packet_burst,
    packet_burst_2, 
    score,
    scorestreaks, 
    ui,
    compass_player,
    AR_ammo
    ]


# Kicked Image Detection
kicked_img = cv.imread('cv references/search/kicked.png')
images_to_detect.append(kicked_img)
kicked_clicks = [(610, 620), (240, 920), (235, 222)] # click exit, find match, quickplay

def check_kicked(frame):
    kicked_region = (500, 376, 921, 309)  # region for kicked image

    screenshot = pyautogui.screenshot(region=kicked_region)
    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    result = cv.matchTemplate(frame, kicked_img, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)
    threshold = 0.75  # Adjust the threshold as needed
    return max_val > threshold

def perform_kicked_actions():
    print(f"{RED}Kicked from the game! Will search for a new match now...{RESET}")

    # Click on the specified positions
    time.sleep(1.5)
    for (x, y) in kicked_clicks:
        mouse.position = (x, y)
        time.sleep(1.5)
        print(f"{GREEN}Mouse Click at location:{RESET} {mouse.position}")
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(.3)


def on_press(key):
    global force_paused
    try:
        if key == Key.f7:
            force_paused = True
            print("Waiting for action to end to pause..")
        elif key == Key.f8:
            force_paused = False
            print("Resuming...")
    except Exception as e:
        print(f"Error: {e}")

# Formula x1, y1, width=x2-x1, height=y2-y1
image_regions = {
    'compass': ((505, 22, 888, 38), compass),
    'killcam': ((851, 38, 219, 56), killcam),
    'killfeed': ((154, 588, 155, 131), killfeed),
    'match_start': ((1587, 193, 315, 39), match_start),
    'match_in_progress_logo': ((1587, 193, 315, 39), match_in_progress_logo),
    'mini_map': ((60, 63, 247, 248), mini_map),
    'packet_burst': ((35, 474, 53, 41), packet_burst),
    'score': ((116, 355, 139, 23), score),
    'scorestreaks': ((1774, 706, 80, 198), scorestreaks),
    'ui': ((1659, 951, 204, 92), ui),
    'compass_player': ((167, 167, 28, 37), compass_player),
    'AR_ammo': ((1527, 1015, 42, 30), AR_ammo)
}


def check_image_in_region(image, region, threshold=0.5):
    """Check if a given image exists in the specified region."""
    # Capture the region desired
    screenshot = pyautogui.screenshot(region=region)
    frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    # Perform template matching
    result = cv.matchTemplate(frame, image, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)

    return max_val > threshold


def ingame():
    """Check if any specified images are in their respective regions, with customized thresholds where needed."""
    for name, (region, img) in image_regions.items():
        if name == 'compass':
            custom_threshold = .8  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region!{RESET}")
                return True
        elif name == 'compass_player':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region!{RESET}")
                return True
        elif name == 'score':
            custom_threshold = .9  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region!{RESET}")
                return True
        elif name == 'killfeed':
            custom_threshold = .7  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region!{RESET}")
                return True
        elif name == 'match_in_progress_logo' or name == 'match_start':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region! (Selecting Loadout){RESET}")
                time.sleep(2)
                # select loadout
                mouse.position = (192, 123)
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(2)
                return True
        elif name == 'killcam':
            custom_threshold = .6  # Custom Threshold
            if check_image_in_region(img, region, threshold=custom_threshold):
                print(f"{GREEN}{name} detected in its region! (skipping Killcam){RESET}")
                # skip killcam
                keyboard.press("e")
                keyboard.release("e")
                return True
        else:
            if check_image_in_region(img, region):
                print(f"{GREEN}{name} detected in its region!{RESET}")
                return True
    return False

def main():
    global paused
    header()
    time.sleep(3)
    input("\n\nPress Enter to continue...")
    clear_console()
    mouse_enabled = enable_mouse()


    mouse.position = (960, 540)
    time.sleep(3)
    print("Waiting to get in a game...")
    while True: # Program Functionality Main Loop
        if not force_paused:
            last_detected_time = time.time()  # Track the last time an image was detected
            while True:
                if force_paused:
                    break
                screenshot = pyautogui.screenshot()
                frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
                
                if not force_paused:
                    if ingame():
                        last_detected_time = time.time()  # Reset Timer
                        if paused:
                            print(f"{GREEN}Image detected! Resuming...{RESET}")
                            paused = False
                    elif check_kicked(frame):  
                        paused = True  # Pause the bot
                        perform_kicked_actions()  # Searches for Match
                        print(f"{GREEN}Kicked actions complete. Resuming search...{RESET}")
                        last_detected_time = time.time()
                    else:
                        # Check if it's been n seconds since the last detection
                        if time.time() - last_detected_time > 20: # adjust time as fit
                            if not paused:
                                print(f"{RED}No image detected for 20 seconds. Pausing...{RESET}")
                                paused = True

                if paused or force_paused:
                    time.sleep(0.1)
                    continue
                
                if mouse_enabled:
                    random_turn = random.randint(-100, 100)
                    move_mouse_relative(random_turn, 0)
                    random_turn = random.randint(-100, 100)
                    move_mouse_relative(random_turn, 0)

                # Keyboard Actions
                skd = get_key_commands(key_command_list)
                do_key_command(skd)

                # Mouse Actions
                if mouse_enabled:
                    smc = get_mouse_commands(mouse_command_list)
                    do_mouse_command(smc)


                shoot(mouse_click_list)
                print("---------------------------------\n")
                time.sleep(1.5)
                keyboard.press("e")
                keyboard.release("e")
                continue

        
        
        clear_console()
        print(format.renderText("PAUSED"))
        while force_paused:
            if not force_paused:
                clear_console()
                print(format.renderText("RESUMED"))
                print("Waiting to get in a game...")
                break



def header():
    print(format.renderText("  AFK   Bot"))
    print(creator.center(43))

def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def enable_mouse():
    while True:
        ask_mouse_enabled = input("Would you like to enable in game mouse movements? [Y/n]: ").lower().strip()
        if ask_mouse_enabled[0] == "y":
            print(f"{GREEN}Mouse Enabled{RESET}")
            return True
        elif ask_mouse_enabled[0] == "n":
            print(f"{RED}Mouse Disabled{RESET}")
            return False
        else:
            continue


def get_mouse_commands(mouse_command_list):
    random_mouse_movement = random.choice(mouse_command_list)
    return random_mouse_movement

def get_key_commands(key_command_list):
    random_key_movement = random.choice(key_command_list)
    return random_key_movement

def do_mouse_command(smc):
    if smc == "180":
        print("Performing 180-degree turn")
        move_mouse_relative(550, 0)
    elif smc == "360":
        print("Performing 360-degree turn")
        move_mouse_relative(1000, 0)
    elif smc == "720":
        print("Performing 720-degree turn")
        move_mouse_relative(2000, 0)
    elif smc == "90Left":
        print("Performing 90-degree left turn")
        move_mouse_relative(-250, 0)
    elif smc == "90Right":
        print("Performing 90-degree right turn")
        move_mouse_relative(250, 0)
    elif smc == "45Left":
        print("Performing 45-degree left turn")
        move_mouse_relative(-125, 0)
    elif smc == "45Right":
        print("Performing 45-degree right turn")
        move_mouse_relative(125, 0)
    elif smc == "RandomTurnSmall":
        random_turn = random.randint(-100, 100)
        print(f"Performing a random turn of {abs(random_turn)} Degrees")
        move_mouse_relative(random_turn, 0)
    else:
        print("Unknown mouse command")

def move_mouse_relative(dx, dy, duration=0.25, steps=50, sensitivity=100):
    """
    Smoothly moves the mouse cursor relative to its current position with scaling.

    Args:
        dx (int): Relative x movement.
        dy (int): Relative y movement.
        duration (float): Total time for the movement in seconds.
        steps (int): Number of intermediate steps.
        sensitivity (float): Scaling factor to amplify the movement.
    """
    # Scale the movement based on sensitivity
    dx = int(dx * sensitivity)
    dy = int(dy * sensitivity)

    # Calculate the increment per step
    step_dx = dx / steps
    step_dy = dy / steps

    # Time delay per step
    step_delay = duration / steps

    for i in range(steps):
        # Move by the calculated step amount
        user32.mouse_event(MOUSEEVENTF_MOVE, int(step_dx), int(step_dy), 0, 0)
        time.sleep(step_delay)



def do_key_command(skd):
    if skd == "Sprint":
        print("Sprint")
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(3)
            keyboard.release("w")
    elif skd == "SlideR":
        print("Slide Right")
        with keyboard.pressed(Key.shift):
            keyboard.press("d")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("d")
            keyboard.release("q")
    elif skd == "Slide":
        print("Sprint and Slide")
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("w")
            keyboard.release("q")
    elif skd == "SlideL":
        print("Slide Left")
        with keyboard.pressed(Key.shift):
            keyboard.press("a")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("a")
            keyboard.release("q")
    elif skd == "SlideBack":
        print("Slide Back")
        with keyboard.pressed(Key.shift):
            keyboard.press("s")
            time.sleep(1)
            keyboard.press("q")
            time.sleep(.5)
            keyboard.release("s")
            keyboard.release("q")
    elif skd == "Crouch":
        print("Crouch")
        keyboard.press("q")
        keyboard.release("q")
    elif skd == "LayDown":
        print("Lay Down")
        keyboard.press(Key.ctrl)
        time.sleep(.5)
        keyboard.release(Key.ctrl)
    elif skd == "Back":
        print("Sprint Backwards")
        with keyboard.pressed(Key.shift):
            keyboard.press("s")
            time.sleep(1)
            keyboard.release("s")
    elif skd == "Inspect":
        print("Inspect")
        keyboard.press("f")
        keyboard.release("f")
        time.sleep(5)
    elif skd == ("Jump"):
        print("Run and Jump")
        with keyboard.pressed(Key.shift):
            keyboard.press("w")
            time.sleep(1)
            keyboard.press(Key.space)
            time.sleep(.5)
            keyboard.release("w")
            keyboard.release(Key.space)
    else:
        pass


def shoot(mouse_click_list):
    YesNo = random.choices([True, False], weights=[.7, .3])[0]
    if YesNo:
        shoot = random.choice(mouse_click_list)
        if shoot == "Shoot":
            print("Shoot")
            mouse.press(Button.left)
            time.sleep(2)
            mouse.release(Button.left)
        elif shoot == "Aim":
            print("Aim")
            mouse.press(Button.right)
            time.sleep(2)
            mouse.release(Button.right)
        elif shoot == "Both":
            print("Aim and Shoot")
            mouse.press(Button.right)
            time.sleep(1)
            mouse.press(Button.left)
            time.sleep(2)
            mouse.release(Button.left)
            mouse.release(Button.right)
    else:
        print("Dont Aim or Shoot")
        



if __name__ == "__main__":
    listener = Listener(on_press=on_press)
    listener.start()
    atexit.register(listener.stop)
    
    main()
