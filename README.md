# Hand Tracking and Drawing Application

Using MediaPipe, this project implements a tool that tracks your hand to paint on the screen. The application allows users to draw, erase, and select colors by interacting with on-screen buttons and gestures.

## Project Overview

This real-time application leverages hand tracking to create a virtual drawing tool. The core features include:

- **Hand Tracking:** Real-time detection and tracking of hand landmarks using MediaPipe.
- **Drawing Interface:** A virtual canvas where users can draw with selected colors.
- **Button Interaction:** On-screen buttons for drawing, erasing, and changing colors.
- **Color Selection:** Users can select colors by hovering over color buttons and confirming the selection with a gesture.

## How It Works

1. **Starting the Application:**
   - Upon starting, the user should move their hand towards the "Draw" button.
   - Tap the Index Finger and Thumb together to activate the drawing mode. Visual feedback will confirm the button click.

2. **Drawing:**
   - The default drawing color is blue. To change the color, hover over a color button and tap your Index Finger and Thumb together. A black box will appear around the selected color to indicate the choice.

3. **Erasing:**
   - To clear the canvas, move your hand to the "Erase" button and tap your Index Finger and Thumb together. This will reset the canvas to a blank state.

4. **Stopping Drawing:**
   - To stop drawing, move your hand to the "Stop" button and tap your Index Finger and Thumb together. This will deactivate the drawing mode.

## Files Description

- **`hand_tracking.py`**
  - **Purpose:** Defines the `HandTracker` class for detecting and tracking hand landmarks using MediaPipe.
  - **Functions:**
    - `__init__()`: Initializes the MediaPipe Hands model.
    - `process_frame(frame)`: Processes a video frame to detect hand landmarks and draw them on the frame.

- **`buttons.py`**
  - **Purpose:** Contains functions to initialize and manage on-screen buttons for interaction.
  - **Functions:**
    - `initialize_buttons()`: Creates and returns the configuration for drawing, erasing, and color buttons.
    - `draw_buttons(frame, buttons, color_buttons, selected_color_button)`: Draws the buttons on the video frame.
    - `calculate_distance(point1, point2)`: Computes the Euclidean distance between two points.
    - `check_button_clicks(frame, hand_landmarks, buttons, color_buttons, drawing_mode, current_color, selected_color_button, canvas, prev_coords, winheight, winwidth)`: Checks if any button is clicked and updates the drawing state and color accordingly.

- **`main.py`**
  - **Purpose:** The main script that integrates hand tracking with button interactions to enable drawing on a virtual canvas.
  - **Key Components:**
    - Captures video from the webcam.
    - Uses `HandTracker` to process each frame for hand landmarks.
    - Handles button interactions for drawing, erasing, and color selection.
    - Combines the canvas with the video frame and displays the result.
    - Exits when the `Esc` key is pressed.

## Usage

1. **Run the Application:**
   - Execute `python main.py` to start the application.

2. **Interact with the Application:**
   - **Draw:** Move your hand to the "Draw" button and tap your Index Finger and Thumb together.
   - **Change Color:** Hover over a color button and tap your Index Finger and Thumb together to select the color.
   - **Erase:** Move your hand to the "Erase" button and tap your Index Finger and Thumb together.
   - **Stop Drawing:** Move your hand to the "Stop" button and tap your Index Finger and Thumb together.

3. **Exit the Application:**
   - Press the `Esc` key to close the application.

