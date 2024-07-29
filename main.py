import cv2
import numpy as np
from hand_tracking import HandTracker
from buttons import draw_buttons, check_button_clicks, initialize_buttons

# Initialize video capture for the live camera feed 
cap = cv2.VideoCapture(0)

# Set the window width and height
winwidth = 1280
winheight = 720

# Initialize buttons and variables
buttons, color_buttons = initialize_buttons()
drawing_mode = False
current_color = (255, 165, 0)  # Default color: Blue
canvas = np.zeros((winheight, winwidth, 3), dtype="uint8") #original stance of canvas
prev_coords = None
selected_color_button = None

# Initialize hand tracking
hand_tracker = HandTracker()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # mirror camera view
    frame = cv2.flip(frame, 1)

    # Process the frame for hand tracking
    frame, hand_landmarks = hand_tracker.process_frame(frame)

    # Check for button clicks and update states
    drawing_mode, current_color, selected_color_button, canvas, prev_coords = check_button_clicks(
        frame, hand_landmarks, buttons, color_buttons, drawing_mode, current_color, selected_color_button, canvas, prev_coords, winheight, winwidth
    )

    # Resize the canvas to match the frame dimensions if they are different
    if canvas.shape[:2] != frame.shape[:2]:
        canvas = cv2.resize(canvas, (frame.shape[1], frame.shape[0]))

    # Draw the buttons with updated colors
    draw_buttons(frame, buttons, color_buttons, selected_color_button)

    # Combine the canvas with the frame
    combined_frame = cv2.addWeighted(frame, 1, canvas, 1, 0)

    # Display the combined frame
    cv2.imshow('Hand Tracking', combined_frame)

    # Exit loop by pressing 'esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
