# Rock Paper Scissors Hand Detection Game 🤖✋🪨📄✂️

A computer vision-based Rock-Paper-Scissors game using Python, OpenCV, and CVZone.  
The game detects hand gestures through your webcam and pits the player against a simple AI. It keeps score and displays the winner with visual overlays.

---

## 🛠️ Features

- Real-time hand detection using **CVZone** and **Mediapipe**.
- AI randomly chooses rock, paper, or scissors.
- No tie rounds; a winner is always decided.
- Score tracking with a **5-point game system**.
- Visual feedback for **win/lose** after each round.
- Countdown timer with retro, tech-style animation.
- Restart functionality after the game ends (`Press 'R'`).

---

## 📁 Project Structure
rock-paper-scissors/
│
├─ main.py # Main game code

├─ requirements.txt # Python dependencies

├─ resources/ # Game assets

│ ├─ rpsbg.png # Background image

│ ├─ rock.png # AI move images

│ ├─ paper.png

│ ├─ scissors.png

│ ├─ win.png # Win overlay

│ ├─ lose.png # Lose overlay

│ └─ PressStart2P-Regular.ttf # Font used for text


---

## 💻 Installation

#1. Clone the repository:

git clone https://github.com/H31S3NB3R4/Computer_vision_Projects.git
cd Computer_vision_Projects/rock-paper-scissors

2.Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

3.Install dependencies:

pip install -r requirements.txt

🚀 How to Run
python main.py

•Press S to start the game.

•Use hand gestures in front of your webcam:

•Rock: Fist

•Paper: Open hand

•Scissors: Two fingers

•Press R to restart the game after it ends.

