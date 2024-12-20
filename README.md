# Sign Language to Text Conversion

## Overview
Sign language is one of the oldest and most natural forms of communication. However, most people do not know sign language, and interpreters are hard to come by. This project addresses this gap by providing a real-time method for converting American Sign Language (ASL) fingerspelling gestures into text using neural networks.

This solution leverages a Convolutional Neural Network (CNN) to classify hand gestures with an accuracy of 98% for the 26 letters of the alphabet. The system enhances communication accessibility for Deaf and Mute (D&M) individuals by interpreting their nonverbal gestures into text.

---

## Features
1. Real-time gesture recognition and text conversion.
2. High accuracy achieved using a two-layer classifier for similar gesture sets.
3. A user-friendly GUI for converting gestures into complete sentences.

---

## Steps to run
```bash
1.  Download the project code (if not cloned)
   -> unzip Sign-Language-Interpreter-using-CNN.zip

2. Navigate to the project directory -> cd Sign-Language-Interpreter-using-CNN

3. Install required libraries -> pip install -r requirements.txt

4. Run the application -> python app.py
```


---

## Steps to Build the Project

### 1. Data Collection
- **Dataset Creation**: Custom dataset created using webcam frames.

- **Preprocessing**: Applied Gaussian blur to extract relevant image features and reduce noise.

### 2. Model Development
- **Architecture**: Built using a Convolutional Neural Network (CNN).
  - **Convolution Layer**: Extracts visual features from hand gestures.
  
  - **Pooling Layer**: Reduces activation matrix size for fewer learnable parameters.
    - Max Pooling
    - Average Pooling
  - **Fully Connected Layer**: Combines inputs for final classification.
  
  - **Final Output Layer**: Predicts class probabilities using the SoftMax function.

### 3. Training
- **Preprocessing**:
  - Converted input images to grayscale.
    
  - Applied Gaussian blur and adaptive thresholding.
    
  - Resized images to 128 x 128 pixels.
    
- **Optimization**:
  - Cross-entropy loss minimized using Adam Optimizer.
    
  - Labeled data used to iteratively adjust network weights.

### 4. Testing
- Two-layer algorithms used to improve classification for similar gesture sets:
  - {D, R, U}
    
  - {T, K, D, I}
    
  - {S, M, N}
    
- Improved predictions through specialized classifiers for each subset.

### 5. GUI Development
- Developed a graphical interface to:
  - Convert gestures to text.
  
  - Form sentences for enhanced communication.

---

## Results
- Achieved 98% accuracy for ASL alphabet gestures.

- Resolved misclassifications for similar gestures through layered classification.

---

## Usage
1. **Training**:
   - Place training and testing data in their respective folders.
     
   - Run the CNN training script to generate a trained model.
     
2. **Testing**:
   - Input live hand gestures through the webcam.
     
   - Use the GUI to view real-time text predictions.
     
3. **GUI**:
   - Convert recognized gestures into meaningful sentences.

---

## Limitations
- Some gestures with high visual similarity require additional classifiers for accurate predictions.
  
- Requires adequate lighting for optimal performance.

---

## Future Improvements
1. Extend support for non-alphabetic ASL gestures.
  
2. Improve robustness in varying lighting conditions.
   
4. Implement a mobile version for portability.

---

## Technologies Used
- **Programming Language**: Python
  
- **Libraries**: TensorFlow, Keras, OpenCV
  
- **Model**: Convolutional Neural Network (CNN)
  
- **Tools**: Gaussian blur, Adaptive Thresholding, Adam Optimizer

---

## How It Works
1. Captures the Region of Interest (ROI) from a live webcam feed.
   
2. Applies preprocessing techniques like Gaussian blur.
   
3. Uses the CNN model to classify gestures
   
4. Outputs the recognized text in real time through a GUI.

---

## Contribution
Feel free to fork, modify, and contribute to this project. Suggestions and pull requests are welcome!

---
