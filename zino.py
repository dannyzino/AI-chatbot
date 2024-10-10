import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import face_recognition
import cv2

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Configure the generative AI model
genai.configure(api_key="AIzaSyCxDbka9e8Kmha3lLCrFSSukRgWfTp8A_w")
model = genai.GenerativeModel('gemini-1.5-flash')
known_face_encodings = []
known_face_names = ["WIN_20241010_21_34_22_Pro"]

# Add known faces
def load_known_faces():
    # Load an example image and learn how to recognize it
    image_of_person = face_recognition.load_image_file("WIN_20241010_21_34_22_Pro") 
    face_encoding = face_recognition.face_encodings(image_of_person)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append("Zino") 

# Function to recognize faces from the webcam feed
def recognize_face():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
         # Convert the frame to RGB (opencv uses BGR by default)
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations and face encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Check each detected face
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, retrieve the known person's name
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Display the result
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            if name != "Unknown":
                print(f"Recognized: {name}")
                speak(f"Hello, {name}. How can I help you today?")
                video_capture.release()
                cv2.destroyAllWindows()
                return True

        # Display the video with rectangles around faces
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return False
# Function to convert text to speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to capture voice input
def capture_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    return audio

# Function to convert voice input to text
def convert_voice_to_text(audio):
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""

# Function to process voice command and generate response
def process_voice_command(text):
    if text.lower() == "bye":
        speak("Goodbye! Have a nice day!")
        return True

    response = model.generate_content(text)
    response_text = response.text if response and hasattr(response, 'text') else "Sorry, I couldn't generate a response."
    print(f"Chatbot: {response_text}")
    speak(response_text)
    return False

# Main function to run the chatbot
def main():
    speak("Hello! How can I help you today?")
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        if text:
            end_program = process_voice_command(text)

if __name__ == "__main__":
    main()
