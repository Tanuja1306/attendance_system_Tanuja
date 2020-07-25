# **Attendance System by Face Recognition**

Hi there! , this is a  project made by Tanuja Kumari (2K18/CO/370) during my summer training , as heading says the aim is to detect ,recognize and mark attendance by face recognition but the project has a lot more objctives:

1. **Detection**
2. **Recognition**
3. **Updating record in Excel**
4. **Managing office employees data and faculty data through excel by the help of GUI**

## - **Detection**

_Detection is done by the help of OpenCV and Haar cascades_

_Face detection using Haar cascades is a machine learning based approach where a cascade function is trained with a set of input data. OpenCV already contains many pre-trained classifiers for face, eyes, smiles, etc.. Today we will be using the face classifier. You can experiment with other classifiers as well._

## - **Recognition**

_Recognition is done by LBPH recogniser_

_Local Binary Pattern (LBP) is a simple yet very efficient texture operator which labels the pixels of an image by thresholding the neighborhood of each pixel and considers the result as a binary number._

_LBPH is one of the easiest face recognition algorithms._
_It can represent local features in the images._
_It is possible to get great results (mainly in a controlled environment)._
_It is robust against monotonic gray scale transformations._
_It is provided by the OpenCV library (Open Source Computer Vision Library)._

## - **Manage record in Excel files by GUI**

_By the help of gui CRUD operations can be performed in excel files_


## - **Python libraries used**

- **OpenCV-python 3.8**
- **tkinter**


Directions to use:
-Download the project using downloading the zip and unzipping it OR clone the project.
-Make a folder named TrainingImageLabel in the unzipped folder.
-Use versions of python3 (I have used python3.8 i.e.the current latest version at the time of making) to run attendance.py file.
-Open terminal at the folder for mac or command prompt at the path of folder in windows/linux.
-Type 'ls' to check the files contained in the folder and check for the 'attendance.py' file.
-Type python3 attendance.py to run the python file.
-The gui would appear on the screen.
-Click 'Image Capture' button to insert your image in the dataset .Wait for a few seconds till it takes all the images to be able to train the cascade classifier.
-In the notification message 'Image has been saved ' would appear.
-Now click on Train Images to train the saved images to the cascade classifier . It will then popup a message window displaying the message'the image has been trained successfully'.
-After image is captured and trained, kindly click on 'Track Image' to mark your attendance.
-The recognizer identifies your image and stores the details in an excel sheet.
-Thank you for passing by !!! Hope you enjoyed the experience.


The project is solely developed by Tanuja Kumari (2nd year DTU student).

