The ChessBot was a physical chessboard which could move pieces and read the board in order to play with another person. My chess algorithm slowly got better at chess by playing with other people. This was a mix between robotics, rudimentary machine learning, and computer vision. For this project I worked with a small team of 2 other people, where I was the team leader and main contributor.

For the Chess Algorithm, I used a very rudimentary Machine Learning algorithm which saved its loss conditions and then never repeated them. Through doing the algorithm like this I could ensure that the computer grew with the user and couldn’t be repeatedly beaten the same way. The reason the chess algorithm was less complicated than the rest of the project was because I had made it my freshman year of highschool, and then built around it 2 years later for this project during my junior year(when I had more experience). The algorithm was coded in python and was stored on a raspberry pi.

The board was able to move the pieces based off a rig I design which used stepper motors and rails to move an electro-magnet under the board. the magnet could attach to washers which were glued to all the pieces in order to move them around. I coded the robotics aspect of this project in C++ and ran it off an Arduino.

The machine would know where all the pieces were using a top-mounted camera and a type of fiducial called an Aruco tag. Each piece and each square had an indexed tag on it which made it easier to read by a camera. I then used the python library picamera in order to access the camera feed and the library cv2 in order to scan the aruco tags and recreate the real life board into an array in my program. All of this was done in python and stored on a raspberry pi.
