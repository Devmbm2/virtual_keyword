import cv2
import mediapipe as mp
from time import sleep
from pynput.keyboard import Controller

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Initialize the keyboard controller
keyboard = Controller()

# Define the keyboard layout (with space and backspace)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        [" ", "<-"]]  # Space bar and Backspace

finalText = ""

# Button class to store button properties
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create the list of buttons
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == " ":  # Make the space bar wider
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, size=[600, 85]))
        elif key == "<-":  # Backspace key
            buttonList.append(Button([100 * j + 650, 100 * i + 50], key, size=[150, 85]))  # Positioned after space
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Function to draw all buttons on the screen with reduced opacity
def drawAll(img, buttonList):
    imgNew = img.copy()  # Create a copy of the original image
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(imgNew, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    # Blend the keyboard with the original image to reduce opacity
    out = cv2.addWeighted(imgNew, 0.5, img, 0.5, 0)
    return out

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a more natural feel
    img = cv2.flip(img, 1)

    # Convert the image to RGB for Mediapipe processing
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Draw all buttons on the screen with reduced opacity
    img = drawAll(img, buttonList)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draw landmarks on the hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Get the positions of the index finger (tip: landmark 8) and thumb (tip: landmark 4)
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            if lmList:
                # Index finger tip coordinates
                x1, y1 = lmList[8]
                # Thumb tip coordinates
                x2, y2 = lmList[12]

                # Calculate the distance between the index finger and thumb
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                # Check if the index finger is over a button
                for button in buttonList:
                    x, y = button.pos
                    w, h = button.size
                    if x < x1 < x + w and y < y1 < y + h:
                        # Highlight the button when hovered
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        # Simulate a click if the distance is small enough
                        if distance < 50:
                            if button.text == " ":  # Handle space bar
                                keyboard.press(" ")
                                keyboard.release(" ")
                                finalText += " "
                            elif button.text == "<-":  # Handle backspace
                                keyboard.press("\b")  # Simulate backspace
                                keyboard.release("\b")
                                finalText = finalText[:-1]  # Remove the last character
                            else:  # Regular key press
                                keyboard.press(button.text)
                                keyboard.release(button.text)
                                finalText += button.text

                            # Highlight the pressed button
                            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            sleep(0.15)  # Add a small delay to avoid multiple presses

    # Display the final text (moved down to avoid overlapping with the space bar)
    cv2.rectangle(img, (50, 500), (700, 600), (175, 0, 175), cv2.FILLED)  # Moved down
    cv2.putText(img, finalText, (60, 580),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Show the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()