import cv2
import cvzone
import time
import random
from cvzone.HandTrackingModule import HandDetector
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # suppress TensorFlow Lite INFO/WARN messages

cap = cv2.VideoCapture(0)
cap.set(3, 276)  # width
cap.set(4, 278)  # height

detector = HandDetector(maxHands=2)

timer = 0
stateResult = False
startGame = False
gameOver = False
score = [0, 0]  # [AI, Player]

# load AI move image
def load_ai_move(num):
    path = ''
    if num == 1:
        path = 'resources/rock.png'
    elif num == 2:
        path = 'resources/paper.png'
    else:
        path = 'resources/scissors.png'

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"⚠️ Could not load image: {path}")
    else:
        print(f"✅ AI chose: {path}")
    return img

# load result overlays
imgWin = cv2.imread('resources/win.png', cv2.IMREAD_UNCHANGED)
imgLose = cv2.imread('resources/lose.png', cv2.IMREAD_UNCHANGED)

while True:
    imgBG = cv2.imread("resources/rpsbg.png")
    success, img = cap.read()
    if not success:
        continue

    # crop and scale
    h, w, _ = img.shape
    if h > w:
        diff = (h - w) // 2
        imgCropped = img[diff:h - diff, :]
    else:
        diff = (w - h) // 2
        imgCropped = img[:, diff:w - diff]

    imgScaled = cv2.resize(imgCropped, (278, 278))

    y_offset = 262
    x_offset = 856

    hands, img = detector.findHands(imgScaled)

    if startGame and not gameOver:
        if stateResult is False:
            timer = time.time() - initialTime

            countdown = 3 - int(timer)

            # Box coordinates
            x_center = int((493 + 778) / 2)
            y_center = int((218 + 500) / 2)

            # Offset slightly down/right
            x_shift, y_shift = 10, 20

            if countdown > 0:
                cv2.putText(imgBG, str(countdown), (x_center - 55 + x_shift, y_center + 35 + y_shift),
                            cv2.FONT_HERSHEY_DUPLEX, 5, (80, 0, 170), 18, cv2.LINE_AA)
                cv2.putText(imgBG, str(countdown), (x_center - 55 + x_shift, y_center + 35 + y_shift),
                            cv2.FONT_HERSHEY_DUPLEX, 5, (190, 0, 255), 8, cv2.LINE_AA)
            else:
                cv2.putText(imgBG, "GO!", (x_center - 110 + x_shift, y_center + 30 + y_shift),
                            cv2.FONT_HERSHEY_DUPLEX, 3.8, (80, 0, 170), 14, cv2.LINE_AA)
                cv2.putText(imgBG, "GO!", (x_center - 110 + x_shift, y_center + 30 + y_shift),
                            cv2.FONT_HERSHEY_DUPLEX, 3.8, (220, 0, 255), 6, cv2.LINE_AA)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = 0
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1   # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2   # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3   # Scissors

                    # random AI move
                    randomNumber = random.randint(1, 3)
                    imgAI = load_ai_move(randomNumber)

                    if imgAI is not None:
                        imgAI = cv2.resize(imgAI, (274, 275))
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (131, 262))

                    # no ties allowed, regenerate AI move if tie occurs
                    while playerMove == randomNumber:
                        randomNumber = random.randint(1, 3)

                    # winner logic
                    if (playerMove == 1 and randomNumber == 3) or \
                       (playerMove == 2 and randomNumber == 1) or \
                       (playerMove == 3 and randomNumber == 2):
                        score[1] += 1
                        result = "win"
                    else:
                        score[0] += 1
                        result = "lose"

                    print("Player Move:", playerMove)
                    print("AI Move:", randomNumber)
                    print("Score:", score)

                    # game over after 5 points
                    if score[0] == 5 or score[1] == 5:
                        gameOver = True
                        winner = "Player" if score[1] == 5 else "AI"

    # overlay camera
    imgBG[y_offset:y_offset + 278, x_offset:x_offset + 278] = imgScaled

    # keep AI visible
    if stateResult and 'imgAI' in locals() and imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (131, 262))

    # Score boxes (new sizes and coords)
    ai_box = (210, 122)
    player_box = (935, 122)

    # Bigger, centered scores in 116x116 boxes
    cv2.putText(imgBG, str(score[0]), (ai_box[0] + 30, ai_box[1] + 80),
                cv2.FONT_HERSHEY_DUPLEX, 2, (120, 0, 200), 6, cv2.LINE_AA)
    cv2.putText(imgBG, str(score[1]), (player_box[0] + 30, player_box[1] + 80),
                cv2.FONT_HERSHEY_DUPLEX, 2, (0, 200, 255), 6, cv2.LINE_AA)
    if gameOver:
    # Resize images to fit score boxes
        if imgWin is not None:
            imgWin = cv2.resize(imgWin, (116, 116))
        if imgLose is not None:
            imgLose = cv2.resize(imgLose, (116, 116))

        # Overlay both sides (win/lose on both boxes)
        if winner == "Player":
            if imgWin is not None:
                imgBG = cvzone.overlayPNG(imgBG, imgWin, player_box)
            if imgLose is not None:
                imgBG = cvzone.overlayPNG(imgBG, imgLose, ai_box)
        elif winner == "AI":
            if imgLose is not None:
                imgBG = cvzone.overlayPNG(imgBG, imgLose, player_box)
            if imgWin is not None:
                imgBG = cvzone.overlayPNG(imgBG, imgWin, ai_box)

        # Slightly higher placement for game over text
        cv2.putText(imgBG, "GAME OVER", (440, 620),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (200, 0, 255), 6, cv2.LINE_AA)
        cv2.putText(imgBG, "Press 'R' to Restart", (470, 660),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 200), 2, cv2.LINE_AA)

    cv2.imshow("BG", imgBG)
    key = cv2.waitKey(1)

    if key == ord('s') and not gameOver:
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == ord('r'):
        # reset everything
        score = [0, 0]
        gameOver = False
        startGame = False
        stateResult = False
        print("🔄 Game reset")
