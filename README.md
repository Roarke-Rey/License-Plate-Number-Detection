# License-Plate-Number-Detection
Compared and evaluated various ways of object detection techniques by recognizing the license plates for different cars from a dataset. <br><br>
Two different approaches were used for comparison, one where OpenCV methods were used for processing an image, and the other approach involved training a Convolutional Neural Network model to detect the license plate in the image. <br><br>
The results proved that the CNN model approach was better at detecting license plates but the OpenCV techniques provided a higher accuracy result for the images it was able to detect the license plates from.<br>
## Models and Approaches
![image](https://user-images.githubusercontent.com/57321224/214947091-6af1e0a4-6389-4e07-9273-1fd4ca9637b8.png)

<br>
<h2> Quantitative Results</h2>
The OpenCV approach experimented with three different smoothing and edge detection techniques. When evaluating different smoothing techniques, the Canny edge detection algorithm was used, and the Gaussian smoothing technique was used while evaluating the different edge detection algorithms.
<br>
<div align="center">
<img width="281" alt="image" src="https://user-images.githubusercontent.com/57321224/214951183-7bfcf4cf-4c32-406c-b6b7-5c59b0eae537.png">
 </div>
The correctly detected image count was obtained by selecting all images from the approaches having an EasyOCR threshold accuracy higher than 0.4, which was selected as the error threshold accuracy.
<div align="center">
<img align="center" width="271" alt="image" src="https://user-images.githubusercontent.com/57321224/214951335-eaedf056-0760-4529-927d-d2fdc21bc54c.png">
</div>

On further comparison of the approaches on various error thresholds, we found that the CNN approach had a higher score for lesser thresholds, with OpenCV approach being the better approach with the increase in the threshold value.
<div align="center">
<img width="376" alt="image" src="https://user-images.githubusercontent.com/57321224/214952148-107e2fae-cc7f-4266-b3f4-d60880983e6c.png">
</div>

