import cv2 as cv
import numpy as np
import pyautogui

# Images
compass = cv.imread('cv references/in game/compass.png')
killcam = cv.imread('cv references/in game/killcam.png')
killfeed = cv.imread('cv references/in game/killfeed.png')
match_in_progress_logo = cv.imread('cv references/in game/match in progress.png')
mini_map = cv.imread('cv references/in game/mini map.png')
packet_burst = cv.imread('cv references/in game/packet burst.png')
packet_burst_2 = cv.imread('cv references/in game/packet burst 2.png')
score = cv.imread('cv references/in game/score.png')
scorestreaks = cv.imread('cv references/in game/scorestreaks.png')
ui = cv.imread('cv references/in game/UI.png')
compass_player = cv.imread('cv references/in game/compass player.png')
kicked_img = cv.imread('cv references/search/kicked.png')

images_to_detect = [
    compass, 
    killcam,  
    killfeed, 
    match_in_progress_logo, 
    mini_map, 
    packet_burst,
    packet_burst_2, 
    score,
    scorestreaks, 
    ui,
    compass_player
]

# Image Regions (x1, y1, width, height)
image_regions = {
    'compass': ((505, 22, 888, 38), compass),
    'killcam': ((851, 38, 219, 56), killcam),
    'killfeed': ((154, 588, 155, 131), killfeed),
    'match_in_progress_logo': ((1587, 193, 315, 39), match_in_progress_logo),
    'mini_map': ((60, 63, 247, 248), mini_map),
    'packet_burst': ((35, 438, 53, 41), packet_burst),
    'score': ((116, 355, 139, 23), score),
    'scorestreaks': ((1774, 706, 80, 198), scorestreaks),
    'ui': ((1659, 961, 204, 92), ui),
    'compass_player': ((167, 167, 28, 37), compass_player),
}

# Capture screenshot of the entire screen
screenshot = pyautogui.screenshot()

# Convert the screenshot to a NumPy array
frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

# Printed regions to avoid repeating print messages
printed_regions = set()

def resize_region_if_needed():
    """Resize the region if any image exceeds the region's dimensions."""
    for name, (region, img) in image_regions.items():
        region_x, region_y, region_width, region_height = region
        image_width, image_height = img.shape[1], img.shape[0]

        # Debugging: print the size of the region and image
        print(f"Checking region '{name}'")
        print(f"Region size: {region_width}x{region_height}")
        print(f"Image size: {image_width}x{image_height}")

        # Ensure that the image is smaller than or equal to the region size
        if image_width > region_width or image_height > region_height:
            # If the region hasn't been printed before, print its name
            if name not in printed_regions:
                print(f"Template for '{name}' is too large for its region! Resizing the region...")
                printed_regions.add(name)

            # Resize the region to match the image's size
            new_region_width = max(region_width, image_width)
            new_region_height = max(region_height, image_height)

            # Update the region size in the dictionary
            image_regions[name] = ((region_x, region_y, new_region_width, new_region_height), img)
            print(f"Updated region size for '{name}' to {new_region_width}x{new_region_height}.")

def save_updated_regions_to_file():
    """Save the updated regions to a file."""
    with open("new_regions.txt", "a") as file:
        for name, (region, img) in image_regions.items():
            x1, y1, width, height = region
            # Append the region in the exact format for easy copying
            file.write(f"'{name}': (({x1}, {y1}, {width}, {height}), {name}),\n")
            print(f"Saved updated region for '{name}' to new_regions.txt.")

# Resize the regions if needed
resize_region_if_needed()

# Save the updated regions to the file
save_updated_regions_to_file()

# Draw rectangles for each region
for region_name, (region, img) in image_regions.items():
    x1, y1, width, height = region
    x2 = x1 + width
    y2 = y1 + height
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle

    # Optionally, add the label for each region
    cv.putText(frame, region_name, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the image with the regions drawn
cv.imshow('Image Regions', frame)

# Wait indefinitely until a key is pressed
cv.waitKey(0)

# Close all OpenCV windows
cv.destroyAllWindows()
