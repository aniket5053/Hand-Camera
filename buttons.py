import cv2
import numpy as np
import mediapipe as mp

def initialize_buttons():
    buttons = {
        "erase": {"topleft": (10, 10), "bottomright": (110, 60), "color": (255, 0, 0), "label": "Erase", "original_color": (255, 0, 0)},
        "draw": {"topleft": (130, 10), "bottomright": (230, 60), "color": (0, 255, 0), "label": "Draw", "original_color": (0, 255, 0)},
        "stop": {"topleft": (250, 10), "bottomright": (350, 60), "color": (0, 0, 255), "label": "Stop", "original_color": (0, 0, 255)},
    }

    color_buttons = [
        {"topleft": (10, 70), "bottomright": (60, 120), "color": (255, 165, 0)},  # Blue
        {"topleft": (70, 70), "bottomright": (120, 120), "color": (0, 255, 0)},  # Green
        {"topleft": (130, 70), "bottomright": (180, 120), "color": (0, 0, 255)},  # Red
        {"topleft": (190, 70), "bottomright": (240, 120), "color": (0, 255, 255)},  # Yellow
        {"topleft": (250, 70), "bottomright": (300, 120), "color": (255, 255, 255)},  # White
    ]
    
    return buttons, color_buttons

def draw_buttons(frame, buttons, color_buttons, selected_color_button):
    for key, button in buttons.items():
        cv2.rectangle(frame, button["topleft"], button["bottomright"], button["color"], -1)
        cv2.putText(frame, button["label"], (button["topleft"][0] + 10, button["topleft"][1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    for i, color_button in enumerate(color_buttons):
        cv2.rectangle(frame, color_button["topleft"], color_button["bottomright"], color_button["color"], -1)
        if selected_color_button == i:
            cv2.rectangle(frame, (color_button["topleft"][0] - 2, color_button["topleft"][1] - 2), (color_button["bottomright"][0] + 2, color_button["bottomright"][1] + 2), (0, 0, 0), 2)

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def check_button_clicks(frame, hand_landmarks, buttons, color_buttons, drawing_mode, current_color, selected_color_button, canvas, prev_coords, winheight, winwidth):
    # Reset button colors to original at the start of each frame
    for key in buttons:
        buttons[key]["color"] = buttons[key]["original_color"]
    
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            index_finger_tip = hand_landmark.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmark.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

            h, w, _ = frame.shape
            index_finger_tip_coords = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            thumb_tip_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            distance = calculate_distance(index_finger_tip_coords, thumb_tip_coords)
            distance_threshold = 30

            if (buttons["erase"]["topleft"][0] <= index_finger_tip_coords[0] <= buttons["erase"]["bottomright"][0] and
                buttons["erase"]["topleft"][1] <= index_finger_tip_coords[1] <= buttons["erase"]["bottomright"][1]):
                if distance < distance_threshold:
                    canvas = np.zeros((winheight, winwidth, 3), dtype="uint8")
                    buttons["erase"]["color"] = (0, 255, 255)  # Change to yellow when clicked

            if (buttons["draw"]["topleft"][0] <= index_finger_tip_coords[0] <= buttons["draw"]["bottomright"][0] and
                buttons["draw"]["topleft"][1] <= index_finger_tip_coords[1] <= buttons["draw"]["bottomright"][1]):
                if distance < distance_threshold:
                    drawing_mode = True
                    buttons["draw"]["color"] = (255, 255, 0)  # Change to yellow when clicked

            if (buttons["stop"]["topleft"][0] <= index_finger_tip_coords[0] <= buttons["stop"]["bottomright"][0] and
                buttons["stop"]["topleft"][1] <= index_finger_tip_coords[1] <= buttons["stop"]["bottomright"][1]):
                if distance < distance_threshold:
                    drawing_mode = False
                    buttons["stop"]["color"] = (255, 255, 0)  # Change to yellow when clicked

            for i, color_button in enumerate(color_buttons):
                if (color_button["topleft"][0] <= index_finger_tip_coords[0] <= color_button["bottomright"][0] and
                    color_button["topleft"][1] <= index_finger_tip_coords[1] <= color_button["bottomright"][1]):
                    if distance < distance_threshold:
                        current_color = color_button["color"]
                        selected_color_button = i

            if drawing_mode and distance < distance_threshold:
                if prev_coords is not None:
                    cv2.line(canvas, prev_coords, index_finger_tip_coords, current_color, 5)
                prev_coords = index_finger_tip_coords
            else:
                prev_coords = None
    
    return drawing_mode, current_color, selected_color_button, canvas, prev_coords
