import pyautogui
import cv2 as cv
import numpy as np

# Define your regions
image_regions = {
    'compass': (505, 22, 888, 38),
    'killcam': (851, 38, 219, 56),
    'killfeed': (154, 588, 155, 131),
    'match_start': (1587, 193, 315, 39),
    'match_in_progress_logo': (1587, 193, 315, 39),
    'mini_map': (60, 63, 247, 248),
    'packet_burst': (35, 474, 53, 41),
    'score': (116, 355, 139, 23),
    'scorestreaks': (1774, 706, 80, 198),
    'ui': (1659, 951, 204, 92),
    'compass_player': (167, 167, 28, 37),
    'AR_ammo': (1527, 1015, 42, 30),
    'kicked_region':(500, 376, 921, 309)
}

# Capture screenshot of the entire screen
screenshot = pyautogui.screenshot()

# Convert the screenshot to a NumPy array
frame = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

# Draw rectangles for each region
for region_name, (x1, y1, width, height) in image_regions.items():
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

# Ask the user if they want to save the image
ask_save = input("Would you like to save this image? [Y/n]: ").strip().lower()
if ask_save == "y":
    while True:
        file_name = input("Give your image a name and extension (e.g., 'image.png' or 'image.jpg'): ").strip()
        try:
            cv.imwrite(file_name, frame)  # Save the image with the specified filename
            print(f"Image saved as {file_name}")
            break
        except Exception:
            print("Failed to save")

