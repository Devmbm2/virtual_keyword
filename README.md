# Virtual Keyboard with Hand Gestures

🚀 **Built a Virtual Keyboard with Hand Gestures Using Python!** 🖥️  
This project allows users to type on a virtual keyboard by simply moving their hands in front of the webcam. It uses **OpenCV**, **MediaPipe**, and **pynput** to recognize hand gestures and simulate keyboard inputs.

## Key Features
- 🖐️ **Hand Gesture Recognition:** Detects finger movements to simulate key presses.
- ␣ **Space Bar & Backspace:** Fully functional space and backspace keys for seamless typing.
- 💡 **Improved UI:** Reduced button opacity for better visibility and a repositioned text display area.

## Tech Stack
- **OpenCV:** Video capture and real-time processing.
- **MediaPipe:** Hand landmark detection.
- **pynput:** Simulating keyboard inputs.
- **Python:** Core implementation.

## Installation
Follow the steps below to install and run the project:

### 1. Clone the Repository
```bash
git clone <repository-link>
cd virtual-keyboard-hand-gestures
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\\Scripts\\activate
```

### 3. Install Dependencies
Install the required packages using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `opencv-python==4.10.0.84`
- `mediapipe==0.10.20`
- `pynput==1.7.7`

### 4. Run the Application
```bash
python virtual_keyboard.py
```

## How to Use
1. Make sure your webcam is connected.
2. Move your hand in front of the webcam.
3. Use your index finger to hover over the virtual keyboard.
4. Pinch your thumb and index finger together to simulate a key press.
5. Use the space bar key for space and the "<-" key for backspace.
6. Press **`q`** on your keyboard to quit the application.

## File Structure
```plaintext
📂 virtual-keyboard-hand-gestures
├── virtual_keyboard.py    # Main application file
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

## Contribution
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

---

