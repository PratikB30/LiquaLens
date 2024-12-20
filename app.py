import numpy as np
import cv2
import os, sys
import time
import operator
from string import ascii_uppercase
import tkinter as tk
from PIL import Image, ImageTk
from spellchecker import SpellChecker  # Import SpellChecker from pyspellchecker
import tensorflow
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import model_from_json

# Initialize SpellChecker with English dictionary
spell = SpellChecker(language='en')  # Using the 'en' dictionary (English)

# Application class
class Application:

    def __init__(self):
        try:
            print("SpellChecker initialized with English dictionary")
        except Exception as e:
            print(f"Error initializing SpellChecker: {e}")
            
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open(r"Models\model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(r"Models\model_new.h5")

        self.json_file_dru = open(r"Models\model-bw_dru.json", "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()

        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights(r"Models\model-bw_dru.h5")

        self.json_file_tkdi = open(r"Models\model-bw_tkdi.json", "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()

        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights(r"Models\model-bw_tkdi.h5")

        self.json_file_smn = open(r"Models\model-bw_smn.json", "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()

        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights(r"Models\model-bw_smn.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
            self.ct[i] = 0

        print("Loaded model from disk")

        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x900")

        self.panel = tk.Label(self.root)
        self.panel.place(x=100, y=10, width=580, height=580)

        self.panel2 = tk.Label(self.root)  # initialize image panel
        self.panel2.place(x=400, y=65, width=275, height=275)

        self.T = tk.Label(self.root)
        self.T.place(x=60, y=5)
        self.T.config(text="Sign Language To Text Conversion", font=("Courier", 30, "bold"))

        self.panel3 = tk.Label(self.root)  # Current Symbol
        self.panel3.place(x=500, y=540)

        self.T1 = tk.Label(self.root)
        self.T1.place(x=10, y=540)
        self.T1.config(text="Character :", font=("Courier", 30, "bold"))

        self.panel4 = tk.Label(self.root)  # Word
        self.panel4.place(x=220, y=595)

        self.T2 = tk.Label(self.root)
        self.T2.place(x=10, y=595)
        self.T2.config(text="Word :", font=("Courier", 30, "bold"))

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=350, y=645)

        self.T3 = tk.Label(self.root)
        self.T3.place(x=10, y=645)
        self.T3.config(text="Sentence :", font=("Courier", 30, "bold"))

        self.T4 = tk.Label(self.root)
        self.T4.place(x=250, y=690)
        self.T4.config(text="Suggestions :", fg="red", font=("Courier", 30, "bold"))

        self.bt1 = tk.Button(self.root, command=self.action1, height=0, width=0)
        self.bt1.place(x=26, y=745)

        self.bt2 = tk.Button(self.root, command=self.action2, height=0, width=0)
        self.bt2.place(x=325, y=745)

        self.bt3 = tk.Button(self.root, command=self.action3, height=0, width=0)
        self.bt3.place(x=625, y=745)

        # Delete Button
        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_last, font=("Courier", 20))
        self.delete_button.place(x=700, y=595)  # Position the button where needed

        # Enter Button to add the current word to the sentence
        self.enter_button = tk.Button(self.root, text="Enter", command=self.enter_character, font=("Courier", 20))
        self.enter_button.place(x=750, y=745)  # Position it where you want in the UI

        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()

        if ok:
            cv2image = cv2.flip(frame, 1)

            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)

            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            cv2image = cv2image[y1: y2, x1: x2]

            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 2)

            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)

            imgtk = ImageTk.PhotoImage(image=self.current_image2)

            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)

            self.panel3.config(text=self.current_symbol, font=("Courier", 30))

            self.panel4.config(text=self.word, font=("Courier", 30))

            self.panel5.config(text=self.str, font=("Courier", 30))

            # Get spelling suggestions using pyspellchecker
            predicts = list(spell.candidates(self.word))  # Get a list of candidate words

            # If there are any suggestions, update the buttons
            if len(predicts) > 1:
                self.bt1.config(text=list(predicts)[0], font=("Courier", 20))
            else:
                self.bt1.config(text="")

            if len(predicts) > 2:
                self.bt2.config(text=list(predicts)[1], font=("Courier", 20))
            else:
                self.bt2.config(text="")

            if len(predicts) > 3:
                self.bt3.config(text=list(predicts)[2], font=("Courier", 20))
            else:
                self.bt3.config(text="")

        self.root.after(5, self.video_loop)

    def predict(self, test_image):
        # The image processing and prediction code remains the same
        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        result_dru = self.loaded_model_dru.predict(test_image.reshape(1, 128, 128, 1))
        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1, 128, 128, 1))
        result_smn = self.loaded_model_smn.predict(test_image.reshape(1, 128, 128, 1))

        prediction = {}
        prediction['blank'] = result[0][0]
        inde = 1

        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1

        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)

        self.current_symbol = prediction[0][0]

        # Handle other symbols 'D', 'R', 'U' and others, similar to your existing code...

    def action1(self):
        if len(self.word) > 0:
            self.str = self.str[:-len(self.word)]

        self.word = self.bt1["text"]
        self.str = self.str + self.word + " "
        self.word = " "

    def action2(self):
        if len(self.word) > 0:
            self.str = self.str[:-len(self.word)]

        self.word = self.bt2["text"]
        self.str = self.str + self.word + " "
        self.word = " "

    def action3(self):
        if len(self.word) > 0:
            self.str = self.str[:-len(self.word)]

        self.word = self.bt3["text"]
        self.str = self.str + self.word + " "
        self.word = " "

    def delete_last(self):
        if self.word:
            #Remove the last character of the current word
            self.word = self.word[:-1]
        else:
            if self.str:
                # If word is empty, remove the last word from the sentence
                self.str = self.str.strip().rsplit(' ', 1)[0]
                
                # Update the displayed word and sentence
                 
                self.panel4.config(text=self.word, font=("Courier", 30))
                self.panel5.config(text=self.str, font=("Courier", 30))

    def enter_character(self):
        if self.current_symbol and self.current_symbol != 'blank':
            self.word += self.current_symbol  # Append the predicted character to the word string
            self.panel4.config(text=self.word, font=("Courier", 30))  # Update word display in the GUI
        else:
            print("No valid character to add")  # Optionally handle blank or empty predictions

        
    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

# Starting the Application
print("Starting Application...")
(Application()).root.mainloop()
