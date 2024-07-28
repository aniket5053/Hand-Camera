import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.mpdrawing = mp.solutions.drawing_utils
        self.hands = self.mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        process_frames = self.hands.process(rgb_frame)
        hand_landmarks_list = []

        if process_frames.multi_hand_landmarks:
            for hand_landmarks in process_frames.multi_hand_landmarks:
                self.mpdrawing.draw_landmarks(frame, hand_landmarks, self.mphands.HAND_CONNECTIONS)
                hand_landmarks_list.append(hand_landmarks)
        
        return frame, hand_landmarks_list
