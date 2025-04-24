# **Flappy Hand Game with OpenCV and Mediapipe**

This is a Flappy Bird-like game powered by OpenCV and Mediapipe, where you control the bird by detecting hand gestures. When your hand is open, the bird flaps and flies. When your hand is closed, the bird stays grounded. You can also take screenshots and record the screen with specific keyboard inputs.

## **Features**

🎮 Hand Gesture Control: Open hand for bird to fly, closed hand to stop.

🖼 Screenshot: Save the current screen with the S key.

🎥 Screen Recording: Toggle screen recording with the V key.

🔁 Game Restart: Restart the game with the R key after game over.

🏆 Score Counter: Track and display the score.

❌ Quit Game: Quit the game by pressing the Q key.

## **Requirements**
✅Python 3.x

✅OpenCV

✅Mediapipe

✅NumPy

## **Install dependencies:**
    pip install opencv-python mediapipe numpy
    
## **Setup and Run**

1.Clone the repository to your local machine:

    git clone https://github.com/yourusername/flappy-hand-game.git
    cd flappy-hand-game

2.Run the script:

    python flappy_game.py

3.Controls:

➡️S: Take a screenshot of the current game frame.

➡️V: Start/Stop screen recording.

➡️R: Restart the game if it's over.

➡️Q: Quit the game.

# **Game Overview**
The game is inspired by Flappy Bird, where the player controls the bird's movement using their hand gestures. The game detects the hand using Mediapipe and OpenCV. It features:

➡️A bird that flies when the hand is open (detected by Mediapipe).

➡️Obstacles (pipes) that move towards the bird.

➡️The game ends if the bird hits a pipe or goes out of bounds.

# **Screenshot and Screen Recording**

➡️Screenshots are saved with a timestamp in the same directory where the game script is run. For example: screenshot_1679876543.png.

➡️Screen recordings are saved as .avi files with a timestamp. You can start/stop the recording by pressing the V key.
 


 
