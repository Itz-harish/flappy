import cv2
import mediapipe as mp
import numpy as np
import random
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Window size
width, height = 640, 480
frame = np.zeros((height, width, 3), dtype=np.uint8)

# Game constants
gravity = 1
flap_power = -15
bird_radius = 20
pipe_gap = 150
pipe_speed = 5

# File helpers
def take_screenshot(frame):
    filename = f"screenshot_{int(time.time())}.png"
    cv2.imwrite(filename, frame)
    print(f"[✅] Screenshot saved: {filename}")

def start_video_writer():
    filename = f"recording_{int(time.time())}.avi"
    return cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height)), filename

# Pipe generation
def new_pipe():
    top = random.randint(50, height - 200)
    return [width, top]

# Finger state checker
def is_hand_open(landmarks):
    finger_tips = [8, 12, 16, 20]
    return all(landmarks[tip].y < landmarks[tip - 2].y for tip in finger_tips)

# Game state reset
def reset_game():
    return {
        'bird_y': height // 2,
        'bird_velocity': 0,
        'score': 0,
        'pipes': [new_pipe()],
        'game_over': False,
    }

# Initialize game
state = reset_game()
cap = cv2.VideoCapture(0)

recording = False
video_writer = None
record_filename = ""

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    frame[:] = (135, 206, 235)

    # Hand detection
    hand_open = False
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_open = is_hand_open(hand_landmarks.landmark)

    # Bird physics
    if not state['game_over']:
        state['bird_velocity'] += gravity
        if hand_open:
            state['bird_velocity'] = flap_power
        state['bird_y'] += state['bird_velocity']

        # Move pipes
        for i in range(len(state['pipes'])):
            state['pipes'][i][0] -= pipe_speed
        if state['pipes'][-1][0] < width - 200:
            state['pipes'].append(new_pipe())
        if state['pipes'][0][0] < -60:
            state['pipes'].pop(0)

        # Pipes drawing and collision
        for pipe in state['pipes']:
            x, top = pipe[0], pipe[1]
            bottom = top + pipe_gap

            cv2.rectangle(frame, (x, 0), (x + 60, top), (34, 139, 34), -1)
            cv2.rectangle(frame, (x, bottom), (x + 60, height), (34, 139, 34), -1)

            if 100 + bird_radius > x and 100 - bird_radius < x + 60:
                if state['bird_y'] - bird_radius < top or state['bird_y'] + bird_radius > bottom:
                    state['game_over'] = True

            if not state['game_over'] and x + 60 < 100 and 'scored' not in pipe:
                state['score'] += 1
                pipe.append('scored')

    # Bird position limit
    if state['bird_y'] > height or state['bird_y'] < 0:
        state['game_over'] = True

    # Draw bird
    cv2.circle(frame, (100, int(state['bird_y'])), bird_radius, (255, 255, 0), -1)

    # Score display
    cv2.putText(frame, f"Score: {state['score']}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    if state['game_over']:
        cv2.putText(frame, "GAME OVER", (180, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, "Press R to Restart", (170, height // 2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Instructions
    cv2.putText(frame, "S = Screenshot  |  V = Record  |  R = Restart  |  Q = Quit", (10, height - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2)

    # Mini camera preview
    img_small = cv2.resize(img, (160, 120))
    frame[0:120, width-160:width] = img_small

    # Show game window
    cv2.imshow("Flappy Hand Game", frame)

    # Record video if active
    if recording and video_writer:
        video_writer.write(frame)

    # Key input
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    elif key == ord('r') and state['game_over']:
        state = reset_game()
    elif key == ord('s'):
        take_screenshot(frame)
    elif key == ord('v'):
        if not recording:
            video_writer, record_filename = start_video_writer()
            recording = True
            print(f"[🎥] Started recording: {record_filename}")
        else:
            recording = False
            if video_writer:
                video_writer.release()
                print(f"[💾] Saved recording: {record_filename}")
                video_writer = None

# Cleanup
if video_writer:
    video_writer.release()
cap.release()
cv2.destroyAllWindows()
