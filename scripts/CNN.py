# -*- coding: utf-8 -*-
"""compfinalCNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nifp4u2VVNUX8TiEowSWBpF7auxu2a_B

Codebase: https://www.kaggle.com/code/emilieyip/vehicle-license-plate-detection-cnn/notebook

This dataset contains 300 images with bounding box annotations of the car license plates within the image. Our goal here is to train a convolutional neural network capable of locating licenses plate on new images.

## Preparation of the data

Import libraries
"""

#The following two installation steps are needed to generate a PDF version of the notebook
#(These lines are needed within Google Colab, but are not needed within a local version of Jupyter notebook)

from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/Colab Notebooks/ComputerVision_FinalProject/ml/')

!sudo apt install tesseract-ocr
!pip install pytesseract
!pip install easyocr

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import cv2
import os
import glob
import imutils
import pytesseract
import numpy as np
from google.colab.patches import cv2_imshow
import easyocr

"""dataset"""

import os
for dirname, _, filenames in os.walk('input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

"""We create the variable X containing all the images of cars by resizing them to 200 * 200.


"""

IMAGE_SIZE = 200

img_dir = "input/images" # Enter Directory of all images 
data_path = os.path.join(img_dir,'*g')
files = glob.glob(data_path)
files.sort() #We sort the images in alphabetical order to match them to the xml files containing the annotations of the bounding boxes
X=[]
for f1 in files:
    img = cv2.imread(f1)
    img = cv2.resize(img, (IMAGE_SIZE,IMAGE_SIZE))
    X.append(np.array(img))
    print(f1)

img_dir = "dataset" # Enter Directory of all images 
data_path = os.path.join(img_dir,'*g')
files = glob.glob(data_path)
files.sort() #We sort the images in alphabetical order to match them to the xml files containing the annotations of the bounding boxes
testcomp=[]
testdataname =[]
for f1 in files:
    img = cv2.imread(f1)
    img = cv2.resize(img, (IMAGE_SIZE,IMAGE_SIZE))
    testcomp.append(np.array(img))
    testdataname.append(os.path.basename(f1))
    print(os.path.basename(f1))

testdataname

"""We create the variable y containing all the bounding boxe annotations (label). 
Before that, we will have to resize the annotations so that it fits the new size of the images (200*200). We create a function resizeannotation for that. 
"""

from lxml import etree
def resizeannotation(f):
    tree = etree.parse(f)
    for dim in tree.xpath("size"):
        width = int(dim.xpath("width")[0].text)
        height = int(dim.xpath("height")[0].text)
    for dim in tree.xpath("object/bndbox"):
        xmin = int(dim.xpath("xmin")[0].text)/(width/IMAGE_SIZE)
        ymin = int(dim.xpath("ymin")[0].text)/(height/IMAGE_SIZE)
        xmax = int(dim.xpath("xmax")[0].text)/(width/IMAGE_SIZE)
        ymax = int(dim.xpath("ymax")[0].text)/(height/IMAGE_SIZE)
    return [int(xmax), int(ymax), int(xmin), int(ymin)]

path = 'input/annotations'
text_files = ['input/annotations/'+f for f in sorted(os.listdir(path))]
y=[]
for i in text_files:
    y.append(resizeannotation(i))
print(y)

resizeannotation("input/annotations/Cars147.xml")

y[0]

"""We check X et y shape"""

np.array(X).shape

np.array(y).shape

"""Display some images of the dataset to check : """

plt.figure(figsize=(10,20))
for i in range(0,30) :
    plt.subplot(10,5,i+1)
    plt.axis('off')
    plt.imshow(X[i])

"""We can draw the rectangle containing the license plate using the OpenCV library"""

from PIL import Image

#Example with the first image of the dataset
image = cv2.rectangle(X[0],(y[0][0],y[0][1]),(y[0][2],y[0][3]),(0, 0, 255))
plt.imshow(image)
plt.show()
#img[top_left_y:bot_right_y, top_left_x:bot_right_x]
tempimage = X[0]
print(y[0])
cropimage = tempimage[y[0][3]:y[0][1],y[0][2]:y[0][0]]
cv2_imshow(cropimage)
plate = pytesseract.image_to_string(cropimage, lang='eng', config='--psm 6')      # The config to show that it is single block of line
print("Number plate is:", plate)

#Example with the second image of the dataset
image = cv2.rectangle(X[1],(y[1][0],y[1][1]),(y[1][2],y[1][3]),(0, 0, 255))
plt.imshow(image)
plt.show()

"""We prepare the data for the CNN :"""

#Transforming in array
X=np.array(X)
y=np.array(y)
testcomp = np.array(testcomp)

#Renormalisation
X = X / 255
y = y / 255
testcomp = testcomp/255

"""We split our dataset in two : training set/testing set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)

"""## CNN"""

from keras.models import Sequential

from keras.layers import Dense, Flatten

from keras.applications.vgg16 import VGG16

# Create the model
model = Sequential()
model.add(VGG16(weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(4, activation="sigmoid"))

model.layers[-6].trainable = False

model.summary()

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

train = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=120, batch_size=32, verbose=1)

# Test
scores = model.evaluate(X_test, y_test, verbose=0)
print("Score : %.2f%%" % (scores[1]*100))

def plot_scores(train) :
    accuracy = train.history['accuracy']
    val_accuracy = train.history['val_accuracy']
    epochs = range(len(accuracy))
    plt.plot(epochs, accuracy, 'b', label='Score apprentissage')
    plt.plot(epochs, val_accuracy, 'r', label='Score validation')
    plt.title('Scores')
    plt.legend()
    plt.show()

plot_scores(train)

"""## DETECTION """

print(testcomp.shape)
print(X_test.shape)
y_cnntest = model.predict(X_test)

y_cnntest = model.predict(X_test)
print(y_cnntest.shape)

plt.figure(figsize=(20,40))
for i in range(0,43) :
    plt.subplot(10,5,i+1)
    plt.axis('off')
    ny = y_cnntest[i]*255
    image = cv2.rectangle(X_test[i],(int(ny[0]),int(ny[1])),(int(ny[2]),int(ny[3])),(0, 255, 0))
    plt.imshow((image * 255).astype(np.uint8))

y_cnn = model.predict(testcomp)

y_cnn.shape

"""**Using data for compvision Final**"""

plt.figure(figsize=(20,40))
for i in range(0,296) :
    plt.subplot(30,10,i+1)
    plt.axis('off')
    ny = y_cnn[i]*255
    image = cv2.rectangle(testcomp[i],(int(ny[0]),int(ny[1])),(int(ny[2]),int(ny[3])),(0, 255, 0))
    plt.imshow((image * 255).astype(np.uint8))

for i in range(0,296) :
    ny = y_cnn[i]*255
    image = cv2.rectangle(testcomp[i],(int(ny[0]),int(ny[1])),(int(ny[2]),int(ny[3])),(0, 255, 0))

reader = easyocr.Reader(['en'])

"""**Sample **"""

testsample=[]
img = cv2.imread("dataset/car80.png")
img = cv2.resize(img, (IMAGE_SIZE,IMAGE_SIZE))
testsample.append(np.array(img))

testsample = np.array(testsample)

testsample = testsample/255

testsample.shape

y_cnnsample = model.predict(testsample)

ny = y_cnnsample[0]*255
image = cv2.rectangle(testsample[0],(int(ny[0]),int(ny[1])),(int(ny[2]),int(ny[3])),(0, 255, 0))
tempimage = testsample[0]
ny3 = (int(ny[3]))
ny2 = (int(ny[2]))
ny1 = (int(ny[1]))
ny0 = (int(ny[0]))
cropimage = tempimage[ny3:ny1,ny2:ny0]
cropimage = (cropimage* 255).astype(np.uint8)
plate = pytesseract.image_to_string(cropimage, lang='eng', config='--psm 6')      # The config to show that it is single block of line
result = reader.readtext(cropimage)
if not result:
  print('')
else:
  result = result[0]
  cv2_imshow((image* 255).astype(np.uint8))
  cv2_imshow(cropimage)
  print("Number plate:", result[1],"\nAccuracy:", result[-1])

testdataname[276]
image = cv2.imread("dataset/car80.png")

!apt-get -qq install texlive texlive-xetex texlive-latex-extra pandoc 
!pip install --quiet pypandoc

os.chdir('/content/drive/MyDrive/Colab Notebooks/ComputerVision_FinalProject/ml/')
#!jupyter nbconvert --to PDF "/content/drive/MyDrive/Colab Notebooks/ComputerVision_FinalProject/ml/compfinalCNN.ipynb"
!jupyter nbconvert --to pdf compfinalCNN.ipynb