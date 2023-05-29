#key packages for the AI
import random
import csv
import sys
#key package for Aruco detection
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#key packages for serial communication with the arduino
import serial


#sets up Serial communication and ties it to the ser variable
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)


# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

square_pos = []
key = ["8a","8b","8c","8d","8e","8f","8g","8h","7a","7b","7c","7d","7e","7f","7g","7h","6a","6b","6c","6d","6e","6f","6g","6h","5a","5b","5c","5d","5e","5f","5g","5h","4a","4b","4c","4d","4e","4f","4g","4h","3a","3b","3c","3d","3e","3f","3g","3h","2a","2b","2c","2d","2e","2f","2g","2h","1a","1b","1c","1d","1e","1f","1g","1h"]
checkToggle = True
lossOld = 0
lossNew = 0
cacheOne = [1.4,1.2,1.3,1.5,1.6,1.3,1.2,1.4,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.2,0.3,0.5,0.6,0.3,0.2,0.4] #stores the board a move ago to save when lost
cacheTwo = [1.4,1.2,1.3,1.5,1.6,1.3,1.2,1.4,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.2,0.3,0.5,0.6,0.3,0.2,0.4]
board = [1.4,1.2,1.3,1.5,1.6,1.3,1.2,1.4,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.2,0.3,0.5,0.6,0.3,0.2,0.4] #list of the board, a sort of virtual Bo0ard
holder_board = [1.4,1.2,1.3,1.5,1.6,1.3,1.2,1.4,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.2,0.3,0.5,0.6,0.3,0.2,0.4] #saves the board to use for moving pieces
ruleBoard = [1.4,1.2,1.3,1.5,1.6,1.3,1.2,1.4,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.4,0.2,0.3,0.5,0.6,0.3,0.2,0.4] #used to check if peice still in check after move
#makes it able to read my giant string
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

#0=white
#1=black
#.1=pawn
#.2=knight
#.3=bishop
#.4=rook
#.5=queen
#.6=king


def inSquare(board_top,board_bottom,piece_top,piece_bottom):#this checks if a piece is in a square. All the inputs are corners, and should be an array of its coordinates[x,y]
    #gets the center of the piece
    centerX = int(piece_top[0]) - int(piece_bottom[0])
    centerX = centerX/2
    centerX = centerX + int(piece_bottom[0])
    centerY = int(piece_top[1]) - int(piece_bottom[1])
    centerY = centerY/2
    centerY = centerY + int(piece_bottom[1])
    #checks if the center of the piece is in the square using nesting if statements
    if(centerX < board_top[0] and centerX > board_bottom[0]):
        if(centerY < board_bottom[1] and centerY > board_top[1]):
            return True
    return False
def readBoard():
    global board
    sorted_pieces = []
    storePiece = []
    #scans the code
    #################################################
    ##PUT IN RASPBERRY PI CODE TO GET CAMERA CODE - STORE THE PICTURE IN THE VARIABLE 'img'
    #################################################
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,default = img)
    ap.add_argument("-t", "--type", type=str,
        default="DICT_4X4_250",
        help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())
    # load the input image from disk and resize it
    image = cv2.imread(args["image"])
    image = imutils.resize(image, width=600)
    # load the ArUCo dictionary, grab the ArUCo parameters, and detect
    # the markers
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
    # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for markerCorner, markerID in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            if(markerID > 64):
                storePiece.append([topRight,bottomLeft,markerID])
        count = 0
        for i in square_pos:
            if count == 63: #this makes sure that the ejection square doesn't add to the board size
                break
            found = False
            for q in storePiece:
                if (inSquare(i[0],i[1],q[0],q[1])):
                    #65 = black pawn
                    #66 = black knight
                    #67 = black bishop
                    #68 = black rook
                    #69 = black queen
                    #70 = black king
                    #71 = white pawn
                    #72 = white knight
                    #73 = white bishop
                    #74 = white rook
                    #75 = white queen
                    #76 = white king
                    if q[2] == 65:
                        sorted_pieces.append(1.1)
                        found = True
                        break
                    elif q[2] == 66:
                        sorted_pieces.append(1.2)
                        found = True
                        break
                    elif q[2] == 67:
                        sorted_pieces.append(1.3)
                        found = True
                        break
                    elif q[2] == 68:
                        sorted_pieces.append(1.4)
                        found = True
                        break
                    elif q[2] == 69:
                        sorted_pieces.append(1.5)
                        found = True
                        break
                    elif q[2] == 70:
                        sorted_pieces.append(1.6)
                        found = True
                        break
                    elif q[2] == 71:
                        sorted_pieces.append(0.1)
                        found = True
                        break
                    elif q[2] == 72:
                        sorted_pieces.append(0.2)
                        found = True
                        break
                    elif q[2] == 73:
                        sorted_pieces.append(0.3)
                        found = True
                        break
                    elif q[2] == 74:
                        sorted_pieces.append(0.4)
                        found = True
                        break
                    elif q[2] == 75:
                        sorted_pieces.append(0.5)
                        found = True
                        break
                    elif q[2] == 76:
                        sorted_pieces.append(0.6)
                        found = True
                        break
                count += 1
            if found == False:
                sorted_pieces.append(0)
        board = sorted_pieces
#making all the functions for the different pieces
def pawn(color,origX,origY,attack): #[if the pawn is white then 0, original x position, original y position, true if you want it to attack if in position to do so]
    global board
    ruleBoard = board
    f = 0
    #mechanic for making the pawn jump 2 places sometimes
    if color == 1 and origY == 2:
        if random.randint(1,2) == 1:
            f = 1
        else:
            f = 2
    elif color == 0 and origY == 7:
        if random.randint(1,2) == 1:
            f = 1
        else:
            f = 2
    if attack == 1:
        if color == 1:
            attackOne = read_board(origX+1,origY+1)
            attackTwo = read_board(origX-1,origY+1)
        else:
            attackOne = read_board(origX+1,origY-1)
            attackTwo = read_board(origX-1,origY-1)
        if attackOne != 0 and int(board[attackOne]) !=  color and attackTwo != 0 and int(board[attackTwo]) != color and board[attackOne] != 0 and board[attackTwo] != 0:
            if(random.randint(0,1)==0):
                updateBoard(read_board(origX,origY),attackOne,color+0.1)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    board = ruleBoard
            else:
                updateBoard(read_board(origX,origY),attackTwo,color+0.1)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    board = ruleBoard
        elif attackOne != 0 and int(board[attackOne]) !=  color and board[attackOne] != 0:
            updateBoard(read_board(origX,origY),attackOne,color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
        elif attackTwo != 0 and int(board[attackTwo]) != color and board[attackTwo] != 0:
            updateBoard(read_board(origX,origY),attackTwo,color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
        if color == 1 and board[read_board(origX,origY+f)] == 0:
            updateBoard(read_board(origX,origY),read_board(origX,origY+1),color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
                return False
        elif color == 0 and board[read_board(origX,origY-f)] == 0:
            updateBoard(read_board(origX,origY),read_board(origX,origY-1),color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
                return False
        else:
            return False
    else:
        if color == 1 and board[read_board(origX,origY+f)] == 0:
            updateBoard(read_board(origX,origY),read_board(origX,origY+1),color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
        elif color == 0 and board[read_board(origX,origY-f)] == 0:
            updateBoard(read_board(origX,origY),read_board(origX,origY-1),color+0.1)
            if check_check(color) == False and check_checkmate():
                return True
            else:
                board = ruleBoard
        else:
            return False
            
def knight(color,origX, origY):
    global board
    ruleBoard = board
    #checks if a move has already been made, fine for knight since not many possible moves.
    #long
    moveOne=False #-x,+y
    moveTwo=False #+x,+y
    moveThree=False #-x, -y
    moveFour=False #+x, -y
    #wide
    moveFive=False #-x,+y
    moveSix=False #+x,+y
    moveSeven=False #-x,-y
    moveEight=False #+x,-y
    while (moveOne == False or moveTwo==False or moveThree==False or moveFour==False or moveFive==False or moveSix==False or moveSeven==False or moveEight==False):
        i = random.randint(1,8) #picks a move
        if i==1 and moveOne==False:
            moveOne = True
            if origX-1 > 0 and origY+2 < 9:
                if int(board[read_board(origX-1,origY+2)]) != color:
                        updateBoard(read_board(origX,origY),read_board(origX-1,origY+2),color+0.2)
                        if check_check(color) == False and check_checkmate():
                            return True
                        else:
                            board = ruleBoard
        elif i==2 and moveTwo==False:
            moveTwo = True
            if origX+1 < 9 and origY+2 <9:
                if int(board[read_board(origX+1,origY+2)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX+1,origY+2),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard
        elif i==3 and moveThree==False:
            moveThree = True
            if origX-1 > 0 and origY-2 > 0:
                if int(board[read_board(origX-1,origY-2)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX-1,origY-2),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard           
        elif i==4 and moveFour==False:
            moveFour = True
            if origX+1 <9 and origY-2 >0:
                if int(board[read_board(origX+1,origY-2)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX+1,origY-2),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard
        elif i==5 and moveFive==False:
            moveFive = True
            if origY+1 > 9 and origX-2 < 0:
                if int(board[read_board(origX-2,origY+1)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX-2,origY+1),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard
        elif i==6 and moveSix==False:
            moveSix = True
            if origY+1 < 9 and origX+2 <9:
                if int(board[read_board(origX+2,origY+1)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX+2,origY+1),color+0.2)
                    if check_check(color) == False and check_checkmate():
                            return True
                    else:
                        board = ruleBoard
        elif i==7 and moveSeven==False:
            moveSeven = True
            if origY-1 > 0 and origX-2 > 0:
                if int(board[read_board(origX-2,origY-1)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX-2,origY-1),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard           
        elif i==8 and moveEight==False:
            moveEight = True
            if origY+1 <9 and origX-2 >0:
                if int(board[read_board(origX+2,origY-1)]) != color:
                    updateBoard(read_board(origX,origY),read_board(origX+2,origY-1),color+0.2)
                    if check_check(color) == False and check_checkmate():
                        return True
                    else:
                        board = ruleBoard
    return False
def bishop(color,origX,origY):
    global board
    ruleBoard = board
    moves = diag_move(origX, origY)
    used = [read_board(origX,origY)]
    while len(used) <=moves:
        ran = random.randint(1,4) #picks a direction. 1 = y+ x+, 2 = y- x+, 3 = y+ x-, 4 =y- x-
        if ran == 1:
            if origY != 8 and origX != 8:
                if origX > origY:
                    ran=random.randint(origX+1,8)-origX                    
                else:
                    ran=random.randint(origY+1,8)-origY
                ranY = origY + ran
                ranX = origX + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.3)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        elif ran == 2:
            if origY != 1 and origX != 8:
                if which_side(origX,origY) == 1:
                    ran=origY-random.randint(1,origY-1)
                else:
                    ran=random.randint(origX+1,8)-origX
                ranY = origY - ran
                ranX = origX + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.3)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        elif ran == 3:
           if origX != 1 and origY != 8:
                if which_side(origX,origY) == 1:
                    ran=origX-random.randint(1,origX-1)
                else:
                    ran=random.randint(origY+1,8)-origY
                ranX = origX-ran
                ranY = origY + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.3)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        else:
           if origX != 1 and origY != 1:
                if origX > origY:
                    ran=random.randint(1,origY+1)-origX                    
                else:
                    ran=random.randint(1,origX+1)-origY
                ranY = origY - ran
                ranX = origX - ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.3)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
    return False
def rook(color,origX,origY):
    global board
    ruleBoard = board
    #finds number of possible moves
    moves = 14
    used = [read_board(origX,origY)]
    while len(used) <=moves:
        ran = random.randint(1,4) #picks a direction. 1 = y+, 2 = y-, 3 = x+, 4 =x-
        if ran == 1:
            if origY != 8:
                ran = random.randint(origY+1,8)                
                if check_rules_cross(origX,origY,origX,ran, color, 0) == False and inList(used, read_board(origX,ran)) == False:
                    used.append(read_board(origX,ran))
                elif check_rules_cross(origX,origY,origX,ran, color, 0):
                    updateBoard(read_board(origX,origY),read_board(origX,ran),color+0.4)
                    if inList(used, read_board(origX,ran)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(origX,ran)) == False:
                        used.append(read_board(origX,ran))
                    board = ruleBoard
        elif ran == 2:
            if origY != 1:
                ran = random.randint(1,origY-1)                
                if check_rules_cross(origX,origY,origX,ran, color, 0) == False and inList(used, read_board(origX,ran)) == False:
                    used.append(read_board(origX,ran))
                elif check_rules_cross(origX,origY,origX,ran, color, 0):
                    updateBoard(read_board(origX,origY),read_board(origX,ran),color+0.4)
                    if inList(used, read_board(origX,ran)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(origX,ran)) == False:
                        used.append(read_board(origX,ran))
                    board = ruleBoard
        elif ran == 3:
           if origX != 8:
                ran = random.randint(origX+1,8)                
                if check_rules_cross(origX,origY,ran,origY, color, 0) == False and inList(used, read_board(ran,origY)) == False:
                    used.append(read_board(ran,origY))
                elif check_rules_cross(origX,origY,ran,origY, color, 0):
                    updateBoard(read_board(origX,origY),read_board(ran,origY),color+0.4)
                    if inList(used, read_board(ran,origY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ran,origY)) == False:
                        used.append(read_board(ran,origY))
                    board = ruleBoard
        else:
           if origX != 1:
                ran = random.randint(1,origX-1)
                if check_rules_cross(origX,origY,ran,origY, color, 0) == False and inList(used, read_board(ran,origY)) == False:
                    used.append(read_board(ran,origY))
                elif check_rules_cross(origX,origY,ran,origY, color, 0):
                    updateBoard(read_board(origX,origY),read_board(ran,origY),color+0.4)
                    if inList(used, read_board(ran,origY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ran,origY)) == False:
                        used.append(read_board(ran,origY))
                    board = ruleBoard
    return False
def queen(color,origX,origY):
    global board
    ruleBoard = board
    moves = 14 + diag_move(origX,origY)
    used = [read_board(origX,origY)]
    while len(used) <=moves:
        ran = random.randint(1,8) #picks a direction. 1 = y+ x+, 2 = y- x+, 3 = y+ x-, 4 =y- x-
        if ran == 1:
            if origY != 8 and origX != 8:
                if origX > origY:
                    ran=random.randint(origX+1,8)-origX                    
                else:
                    ran=random.randint(origY+1,8)-origY
                ranY = origY + ran
                ranX = origX + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.5)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        elif ran == 2:
            if origY != 1 and origX != 8:
                if which_side(origX,origY) == 1:
                    ran=origY-random.randint(1,origY-1)
                else:
                    ran=random.randint(origX+1,8)-origX
                ranY = origY - ran
                ranX = origX + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.5)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        elif ran == 3:
           if origX != 1 and origY != 8:
                if which_side(origX,origY) == 1:
                    ran=origX-random.randint(1,origX-1)
                else:
                    ran=random.randint(origY+1,8)-origY
                ranX = origX-ran
                ranY = origY + ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.5)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        elif ran == 4:
           if origX != 1 and origY != 1:
                if origX > origY:
                    ran=random.randint(1,origY+1)-origX                    
                else:
                    ran=random.randint(1,origX+1)-origY
                ranY = origY - ran
                ranX = origX - ran
                if check_rules_diag(origX,origY,ranX,ranY, color) == False and inList(used, read_board(ranX,ranY)) == False:
                    used.append(read_board(ranX,ranY))
                elif check_rules_diag(origX,origY,ranX,ranY, color):
                    updateBoard(read_board(origX,origY),read_board(ranX,ranY),color+0.5)
                    if inList(used, read_board(ranX,ranY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ranX,ranY)) == False:
                        used.append(read_board(ranX,ranY))
                    board = ruleBoard
        if ran == 5:
            if origY != 8:
                ran = random.randint(origY+1,8)
                if check_rules_cross(origX,origY,origX,ran, color, 0) == False and inList(used, read_board(origX,ran)) == False:
                    used.append(read_board(origX,ran))
                elif check_rules_cross(origX,origY,origX,ran, color, 0):
                    updateBoard(read_board(origX,origY),read_board(origX,ran),color+0.5)
                    if inList(used, read_board(origX,ran)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(origX,ran)) == False:
                        used.append(read_board(origX,ran))
                    board = ruleBoard
        elif ran == 6:
            if origY != 1:
                ran = random.randint(1,origY-1)                
                if check_rules_cross(origX,origY,origX,ran, color, 0) == False and inList(used, read_board(origX,ran)) == False:
                    used.append(read_board(origX,ran))
                elif check_rules_cross(origX,origY,origX,ran, color, 0):
                    updateBoard(read_board(origX,origY),read_board(origX,ran),color+0.5)
                    if inList(used, read_board(origX,ran)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(origX,ran)) == False:
                        used.append(read_board(origX,ran))
                    board = ruleBoard
        elif ran == 7:
           if origX != 8:
                ran = random.randint(origX+1,8)                
                if check_rules_cross(origX,origY,ran,origY, color, 0) == False and inList(used, read_board(ran,origY)) == False:
                    used.append(read_board(ran,origY))
                elif check_rules_cross(origX,origY,ran,origY, color, 0):
                    updateBoard(read_board(origX,origY),read_board(ran,origY),color+0.5)
                    if inList(used, read_board(ran,origY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ran,origY)) == False:
                        used.append(read_board(ran,origY))
                    board = ruleBoard
        else:
           if origX != 1:
                ran = random.randint(1,origX-1)
                if check_rules_cross(origX,origY,ran,origY, color, 0) == False and inList(used, read_board(ran,origY)) == False:
                    used.append(read_board(ran,origY))
                elif check_rules_cross(origX,origY,ran,origY, color, 0):
                    updateBoard(read_board(origX,origY),read_board(ran,origY),color+0.5)
                    if inList(used, read_board(ran,origY)) == False and check_check(color) == False and check_checkmate():
                        return True
                    elif inList(used, read_board(ran,origY)) == False:
                        used.append(read_board(ran,origY))
                    board = ruleBoard
    return False
def king(color,origX,origY):
    global board
    ruleBoard = board
    used = [read_board(origX,origY)]
    moves = 8
    while len(used) != moves:
        ran = random.randint(1,8) #x+,x-,y+,y-,x+y+,x+y-,x-y+,x-y-
        if ran == 1:
            if inList(used, read_board(origX+1,origY))==False and check_rules_cross(origX,origY,origX+1,origY,color,0):
                updateBoard(read_board(origX,origY),read_board(origX+1,origY),color+0.6)
                if  check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX+1,origY))
                board = ruleBoard
            elif inList(used, read_board(origX+1,origY)) == False:
                used.append(read_board(origX+1,origY))
                
        elif ran == 2:
            if check_rules_cross(origX,origY,origX-1,origY,color,0) and inList(used, read_board(origX-1,origY))==False:
                updateBoard(read_board(origX,origY),read_board(origX-1,origY),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX-1,origY))
                board = ruleBoard
            elif inList(used, read_board(origX-1,origY)) == False:
                used.append(read_board(origX-1,origY))
                
        elif ran == 3:
            if check_rules_cross(origX,origY,origX,origY+1,color,0) and inList(used, read_board(origX,origY+1))==False:
                updateBoard(read_board(origX,origY),read_board(origX,origY+1),color+0.6)
                if  check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX,origY+1))
                board = ruleBoard
            elif inList(used, read_board(origX,origY+1))==False:
                used.append(read_board(origX,origY+1))
                
        elif ran == 4:
            if check_rules_cross(origX,origY,origX,origY-1,color,0) and inList(used, read_board(origX,origY-1))==False:
                updateBoard(read_board(origX,origY),read_board(origX,origY-1),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX,origY-1))
                board = ruleBoard
            elif inList(used, read_board(origX,origY-1))==False:
                used.append(read_board(origX,origY-1))
                
        elif ran == 5:
            if check_rules_diag(origX,origY,origX+1,origY+1,color) and inList(used, read_board(origX+1,origY+1))==False:
                updateBoard(read_board(origX,origY),read_board(origX+1,origY+1),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX+1,origY+1))
                board = ruleBoard
            elif inList(used, read_board(origX+1,origY+1))==False:
                used.append(read_board(origX+1,origY+1))
                
        elif ran == 6:
            if check_rules_cross(origX,origY,origX+1,origY-1,color,0) and inList(used, read_board(origX+1,origY-1))==False:
                updateBoard(read_board(origX,origY),read_board(origX+1,origY-1),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX+1,origY-1))
                board = ruleBoard
            elif inList(used, read_board(origX+1,origY-1))==False:
                used.append(read_board(origX+1,origY-1))
                
        elif ran == 7:
            if check_rules_cross(origX,origY,origX-1,origY+1,color,0) and inList(used, read_board(origX-1,origY+1))==False:
                updateBoard(read_board(origX,origY),read_board(origX-1,origY+1),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX-1,origY+1))
                board = ruleBoard
            elif inList(used, read_board(origX-1,origY+1))==False:
                used.append(read_board(origX-1,origY+1))
                
        else:
            if check_rules_cross(origX,origY,origX-1,origY-1,color,0) and inList(used, read_board(origX-1,origY-1))==False:
                updateBoard(read_board(origX,origY),read_board(origX-1,origY-1),color+0.6)
                if check_check(color) == False and check_checkmate():
                    return True
                else:
                    used.append(read_board(origX-1,origY-1))
                board = ruleBoard
            elif inList(used, read_board(origX-1,origY-1))==False:
                used.append(read_board(origX-1,origY-1))
                
    return False
#checks if piece follows rules
def check_rules_diag(origX,origY,newX,newY,color): #for bishop, queen, and king

    #this part checks if it crosses over another peice in an unruly way
    
    #uses this for the same function of a slope, slope will always be a variation of 1
    dX = newX-origX #delta X (for slope)
    dY = newY-origY #delta Y (for slope)
    #makes the makeshift slope
    if(dX >= 0):
        mX = 1
    else:
        mX = -1
    if(dY >= 0):
        mY = 1
    else:
        mY = -1
    #checks to see if it goes over a wall
    if (newX > 8 or newY > 8 or newX < 1 or newY < 1):
        return False
    #loop to see if there are collisions of other peices
    i = 0
    e = abs(dX)
    while (i<=e):
        if(board[read_board(i*mX+origX,i*mY+origY)] != 0):
            if color == int(board[read_board(i*mX+origX,i*mY+origY)]) and i != 0: #doesn't blow flags if takes a piece
                return False
            elif color != int(board[read_board(i*mX+origX,i*mY+origY)]):
                if color == 1:
                    color = 0
                else:
                    color = 1
        i += 1
    return True
def check_rules_cross(origX,origY,newX,newY,color,isPawn): #for rook, pawn, queen, and king
    #makeshift slope
    dX = newX-origX #delta X (for slope)
    dY = newY-origY #delta Y (for slope)
    if(dX >= 0):
        mX = 1
    else:
        mX = -1
    if(dY >= 0):
        mY = 1
    else:
        mY = -1
    #checks to see if it goes over a wall
    if (newX > 8 or newY > 8 or newX < 1 or newY < 1):
        return False
    #loop to see if there are collisions of other peices
    if dX == 0: #makes sure that the loop doesnt cancel out for 0, picks a valid value for the number of loops
        e = abs(dY)
    else:
        e = abs(dX)
    i = 0
    while (i<=e):
        if dX == 0:
            xVal = origX
            yVal = i*mY+origY
        else:
            yVal = origY
            xVal = i*mX+origX
        if(board[read_board(xVal,yVal)] != 0):
            if color == int(board[read_board(xVal,yVal)]) and i != 0: #doesn't blow flags if takes a piece
                return False
            elif color != int(board[read_board(xVal,yVal)]):
                if isPawn == 1:
                    return False
                if color == 1:
                    color = 0
                else:
                    color = 1
        i += 1
    return True
#checks if king in check
def check_check(color):
    i = 0
    king = 0
    while i < len(board):
        if board[i] == color + 0.6:
            king = i 
            break
        i += 1
    i = 0
    while i < len(board):
        x = decodeX(i)
        y = decodeY(i)        
        if board[i] == round(1.1 - color,1):
            if color == 1:
                if i - 7 == king or i - 9 == king:
                    return True
            else:
                if i + 7 == king or i + 9 == king:
                    return True
        elif board[i] == round(1.2 - color,1):
            if i - 17 == king or i - 15 == king or i + 17 == king or i + 15 == king:
                return True
        elif board[i] == round(1.3 - color,1):
            z = 1
            while x + z < 9 or y + z < 9: #y+x+
                if check_rules_diag(x,y,x+z,y+z,color):
                    if read_board(x+z,y+z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x + z < 9 or y - z > 0:#y-x+
                if check_rules_diag(x,y,x+z,y-z,color):
                    if read_board(x+z,y-z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x - z > 0 or y + z < 9:#y+x-
                if check_rules_diag(x,y,x-z,y+z,color):
                    if read_board(x-z,y+z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x - z > 0 or y - z > 0:#y-x-
                if check_rules_diag(x,y,x-z,y-z,color):
                    if read_board(x-z,y-z) == king:
                        return True
                else:
                    break
                z += 1
        elif board[i] == round(1.4 - color,1):
            z = 1
            while x+z < 9:#x+
                if check_rules_cross(x,y,x+z,y,color,0):
                    if read_board(x+z,y) == king:
                        return True
                else:
                    break
                z += 1                
            z = 1
            while x-z > 0:#x-
                if check_rules_cross(x,y,x-z,y,color,0):
                    if read_board(x-z,y) == king:
                        return True
                else:
                    break
                z += 1             
            z = 1 
            while y+z < 9:#y+
                if check_rules_cross(x,y,x,y+z,color,0):
                    if read_board(x,y+z) == king:
                        return True
                else:
                    break
                z += 1             
            z = 1
            while y-z > 0:#y-
                if check_rules_cross(x,y,x,y-z,color,0):
                    if read_board(x,y-z) == king:
                        return True
                else:
                    break
                z += 1             
        elif board[i] == round(1.5 - color,1):
            z = 1
            while x + z < 9 or y + z < 9: #y+x+
                if check_rules_diag(x,y,x+z,y+z,color):
                    if read_board(x+z,y+z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x + z < 9 or y - z > 0:#y-x+
                if check_rules_diag(x,y,x+z,y-z,color):
                    if read_board(x+z,y-z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x - z > 0 or y + z < 9:#y+x-
                if check_rules_diag(x,y,x-z,y+z,color):
                    if read_board(x-z,y+z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x - z > 0 or y - z > 0:#y-x-
                if check_rules_diag(x,y,x-z,y-z,color):
                    if read_board(x-z,y-z) == king:
                        return True
                else:
                    break
                z += 1
            z = 1
            while x+z < 9:#x+
                if check_rules_cross(x,y,x+z,y,color,0):
                    if read_board(x+z,y) == king:
                        return True
                else:
                    break
                z += 1                
            z = 1
            while x-z > 0:#x-
                if check_rules_cross(x,y,x-z,y,color,0):
                    if read_board(x-z,y) == king:
                        return True
                else:
                    break
                z += 1             
            z = 1 
            while y+z < 9:#y+
                if check_rules_cross(x,y,x,y+z,color,0):
                    if read_board(x,y+z) == king:
                        return True
                else:
                    break
                z += 1             
            z = 1
            while y-z > 0:#y-
                if check_rules_cross(x,y,x,y-z,color,0):
                    if read_board(x,y-z) == king:
                        return True
                else:
                    break
                z += 1                 
        elif board[i] == round(1.6 - color,1):
            if i + 8 == king or i - 8 == king or i+1 == king or i-1 == king or i + 7 == king or i - 7 == king or i + 9 == king or i - 9 == king:
                return True
        i += 1
    return False
#prints screen for troubleshooting
def print_screen():
    i = 0
    printBoard = []
    while i < 64:
        if board[i] == 0:
            printBoard.append("XXX")
        else:
            printBoard.append(str(board[i]))
        i += 1
    print(printBoard[0],printBoard[1],printBoard[2],printBoard[3],printBoard[4],printBoard[5],printBoard[6],printBoard[7])
    print(printBoard[8],printBoard[9],printBoard[10],printBoard[11],printBoard[12],printBoard[13],printBoard[14],printBoard[15])
    print(printBoard[16],printBoard[17],printBoard[18],printBoard[19],printBoard[20],printBoard[21],printBoard[22],printBoard[23])
    print(printBoard[24],printBoard[25],printBoard[26],printBoard[27],printBoard[28],printBoard[29],printBoard[30],printBoard[31])
    print(printBoard[32],printBoard[33],printBoard[34],printBoard[35],printBoard[36],printBoard[37],printBoard[38],printBoard[39])
    print(printBoard[40],printBoard[41],printBoard[42],printBoard[43],printBoard[44],printBoard[45],printBoard[46],printBoard[47])
    print(printBoard[48],printBoard[49],printBoard[50],printBoard[51],printBoard[52],printBoard[53],printBoard[54],printBoard[55])
    print(printBoard[56],printBoard[57],printBoard[58],printBoard[59],printBoard[60],printBoard[61],printBoard[62],printBoard[63])
    #need to fix formating on screen when print_screen declared

#saves the board possition and last move
#def save_board():
    
#converts x and y values into a list value
def read_board(x,y):
    hold = 8*y
    holdOne = 8-x
    return(hold-holdOne-1)
def inList(l,v):
    for x in l:
        if x == v:
            return True
    return False
def diag_move(origX,origY):
    moves = 0
    i = [origX,origY]
    while i[0] < 9 and i[1] < 9 and i[0] > 0 and i[1] > 0: #y+ x+
        moves += 1
        i = [i[0]+1,i[1]+1]
    moves -= 1
    i = [origX,origY]
    while i[0] < 9 and i[1] < 9 and i[0] > 0 and i[1] > 0: #y+ x-
        moves += 1
        i = [i[0]-1,i[1]+1]
    moves -= 1
    i = [origX,origY]
    while i[0] < 9 and i[1] < 9 and i[0] > 0 and i[1] > 0: #y- x+
        moves += 1
        i = [i[0]+1,i[1]-1]
    moves -=1
    i = [origX,origY]
    while i[0] < 9 and i[1] < 9 and i[0] > 0 and i[1] > 0: #y- x-
        moves += 1
        i = [i[0]-1,i[1]-1]
    moves -= 1
    i = [origX,origY]
    return moves
def decodeY(i):
    i = int(i/8)
    return i + 1
def decodeX(i):
    i = i%8
    return i + 1
def run(color):
    moves = 64
    used = []
    global fileOld
    global fileNew
    global cacheOne
    global cacheTwo
    global board
    global ruleBoard
    global tooLong
    moves = 64
    used = []
    while len(used) < moves:
        ran = random.randint(0,63)
        if inList(used, ran) == False:
            used.append(ran)
            if board[ran] == 0.1 + color:
                if random.randint(1,2) ==  1:
                    if pawn(color, decodeX(ran), decodeY(ran), 0):
                        return True
                else:
                    if pawn(color, decodeX(ran), decodeY(ran), 1):
                        return True
            elif board[ran] == 0.2 + color:
                if knight(color,decodeX(ran),decodeY(ran)):
                    return True 
            elif board[ran] == 0.3 + color:
                if bishop(color,decodeX(ran),decodeY(ran)):
                    return True 
            elif board[ran] == 0.4 + color:
                if rook(color,decodeX(ran),decodeY(ran)):
                    return True 
            elif board[ran] == 0.5 + color:
                if queen(color,decodeX(ran),decodeY(ran)):
                    return True 
            elif board[ran] == 0.6 + color:
                if king(color,decodeX(ran),decodeY(ran)):
                    return True
    if check_check(color):
        print("checkmate")
    else:
        print("stalemate")
    antiSpacer = [str(compress(cacheTwo))] #this is to prevent it from making every number a different cell. It stupid but whatever.
    with open('cacheboard.csv','a',newline='') as csvFile:
        fileOld = csv.writer(csvFile)
        fileOld.writerow(antiSpacer)
    antiSpacer = [str(compress(cacheOne))] #this is to prevent it from making every number a different cell. It stupid but whatever.
    with open('moveboard.csv','a',newline='') as csvFile:
        fileNew = csv.writer(csvFile)
        fileNew.writerow(antiSpacer)
def updateBoard(orig,pos,val):
    global board
    bruhBoard = board
    board = []
    i = 0
    while i < 64:
        i += 1
        if i - 1 == pos:
            board.append(val)
        elif i - 1 == orig:
            board.append(0)
        else:
            board.append(bruhBoard[i - 1])
def which_side(x,y): #1 = less, 2 = on line, 3 = more
    if y == 1:
        if x < 8:
            return 1
        else:
            return 2
    elif y == 2:
        if x < 7:
            return 1
        elif x == 7:
            return 2
        else:
            return 3
    elif y == 3:
        if x < 6:
            return 1
        elif x == 6:
            return 2
        else:
            return 3
    elif y == 4:
        if x < 5:
            return 1
        elif x == 5:
            return 2
        else:
            return 3
    elif y == 5:
        if x < 4:
            return 1
        elif x == 4:
            return 2
        else:
            return 3
    elif y == 6:
        if x < 3:
            return 1
        elif x == 3:
            return 2
        else:
            return 3
    elif y == 7:
        if x < 2:
            return 1
        elif x == 2:
            return 2
        else:
            return 3
    else:
        if x > 1:
            return 3
        else:
            return 2
def compress(board):
    #converts from list into intiger to add to the file
    #nothing = 00
    #white pawn = 01
    #white knite = 02
    #white bishop = 03
    #white rook = 04
    #white queen = 05
    #white king = 06
    #black pawn = 11
    #black knite = 12
    #black bishop = 13
    #black rook = 14
    #black queen = 15
    #black king = 16
    tempBoard = 1
    i = 0
    while i != 63:
        tempBoard = tempBoard * 100
        if board[i] == 0.1:
            tempBoard = tempBoard+1
        elif board[i] == 0.2:
            tempBoard = tempBoard+2
        elif board[i] == 0.3:
            tempBoard = tempBoard+3
        elif board[i] == 0.4:
            tempBoard = tempBoard+4
        elif board[i] == 0.5:
            tempBoard = tempBoard+5
        elif board[i] == 0.6:
            tempBoard = tempBoard+6
        elif board[i] == 1.1:
            tempBoard = tempBoard+11
        elif board[i] == 1.2:
            tempBoard = tempBoard+12
        elif board[i] == 1.3:
            tempBoard = tempBoard+13
        elif board[i] == 1.4:
            tempBoard = tempBoard+14
        elif board[i] == 1.5:
            tempBoard = tempBoard+15
        elif board[i] == 1.6:
            tempBoard = tempBoard+16
        i += 1
    return tempBoard
def unCompress(): #converts the csv into a list
    global listOld
    global listNew
    with open('cacheboard.csv', 'r') as csv_file:
        readOld = csv.reader(csv_file)
        ret = []
        for line in readOld:
            ret.append(line)
        listOld = ret
    with open('moveboard.csv', 'r') as csv_file:
        readNew = csv.reader(csv_file)
        ret = []
        for line in readNew:
            ret.append(line)
        listNew = ret
def intLen(num):
   return len(str(num))
   
def check_checkmate():
    global checkToggle
    global board
    boardHold = board
    if inList(listOld, compress(cacheOne)):
        if listNew[listOld.index(compress(cacheOne))] == compress(board):
            return False
    if checkToggle == True:
        checkToggle = False
        if run(1) == False: #remember to replace with color variable
            board = boardHold
            checkToggle = True
            return False
        else:
            board = boardHold
            checkToggle = True
    return True
def promote():
    switch = 0
    if color == 1:
        if board[56] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(56,56,1.2)
            else:
                print("promote to queen")
                updateBoard(56,56,1.5)
        elif board[57] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(57,57,1.2)
            else:
                print("promote to queen")
                updateBoard(57,57,1.5)
        elif board[58] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(58,58,1.2)
            else:
                print("promote to queen")
                updateBoard(58,58,1.5)
        elif board[59] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(59,59,1.2)
            else:
                print("promote to queen")
                updateBoard(59,59,1.5)
        elif board[60] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(60,60,1.2)
            else:
                print("promote to queen")
                updateBoard(60,60,1.5)
        elif board[61] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(61,61,1.2)
            else:
                print("promote to queen")
                updateBoard(61,61,1.5)
        elif board[62] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(62,62,1.2)
            else:
                print("promote to queen")
                updateBoard(62,62,1.5)
        elif board[63] == 1.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(63,63,1.2)
            else:
                print("promote to queen")
                updateBoard(63,63,1.5)
    if color == 0:
        if board[0] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(0,0,0.2)
            else:
                print("promote to queen")
                updateBoard(0,0,0.5)
        elif board[1] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(1,1,0.2)
            else:
                print("promote to queen")
                updateBoard(1,1,0.5)
        elif board[2] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(2,2,0.2)
            else:
                print("promote to queen")
                updateBoard(2,2,0.5)
        elif board[3] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(3,3,0.2)
            else:
                print("promote to queen")
                updateBoard(3,3,0.5)
        elif board[4] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(4,4,0.2)
            else:
                print("promote to queen")
                updateBoard(4,4,0.5)
        elif board[5] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(5,5,0.2)
            else:
                print("promote to queen")
                updateBoard(5,5,0.5)
        elif board[6] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(6,6,0.2)
            else:
                print("promote to queen")
                updateBoard(6,6,0.5)
        elif board[7] == 0.1:
            ran = random.randint(2,3)
            if ran == 2:
                print("promote to knight")
                updateBoard(7,7,0.2)
            else:
                print("promote to queen")
                updateBoard(7,7,0.5)
def user_promote():
    if color != 1:
        if board[56] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(56,56,1.2)
            elif ran == "bishop":
                updateBoard(56,56,1.3)
            elif ran == "rook":
                updateBoard(56,56,1.4)
            else:
                updateBoard(56,56,1.5)
        elif board[57] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(57,57,1.2)
            elif ran == "bishop":
                updateBoard(57,57,1.3)
            elif ran == "rook":
                updateBoard(57,57,1.4)
            else:
                updateBoard(57,57,1.5)
        elif board[58] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(58,58,1.2)
            elif ran == "bishop":
                updateBoard(58,58,1.3)
            elif ran == "rook":
                updateBoard(58,58,1.4)
            else:
                updateBoard(58,58,1.5)
        elif board[59] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(59,59,1.2)
            elif ran == "bishop":
                updateBoard(59,59,1.3)
            elif ran == "rook":
                updateBoard(59,59,1.4)
            else:
                updateBoard(59,59,1.5)
        elif board[60] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(60,60,1.2)
            elif ran == "bishop":
                updateBoard(60,60,1.3)
            elif ran == "rook":
                updateBoard(60,60,1.4)
            else:
                updateBoard(60,60,1.5)
        elif board[61] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(61,61,1.2)
            elif ran == "bishop":
                updateBoard(61,61,1.3)
            elif ran == "rook":
                updateBoard(61,61,1.4)
            else:
                updateBoard(61,61,1.5)
        elif board[62] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(62,62,1.2)
            elif ran == "bishop":
                updateBoard(62,62,1.3)
            elif ran == "rook":
                updateBoard(62,62,1.4)
            else:
                updateBoard(62,62,1.5)
        elif board[63] == 1.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(63,63,1.2)
            elif ran == "bishop":
                updateBoard(63,63,1.3)
            elif ran == "rook":
                updateBoard(63,63,1.4)
            else:
                updateBoard(63,63,1.5)
    else:
        if board[0] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(0,0,0.2)
            elif ran == "bishop":
                updateBoard(0,0,0.3)
            elif ran == "rook":
                updateBoard(0,0,0.4)
            else:
                updateBoard(0,0,0.5)
        elif board[1] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(1,1,0.2)
            elif ran == "bishop":
                updateBoard(1,1,0.3)
            elif ran == "rook":
                updateBoard(1,1,0.4)
            else:
                updateBoard(1,1,0.5)
        elif board[2] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(2,2,0.2)
            elif ran == "bishop":
                updateBoard(2,2,0.3)
            elif ran == "rook":
                updateBoard(2,2,0.4)
            else:
                updateBoard(2,2,0.5)
        elif board[3] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(3,3,0.2)
            elif ran == "bishop":
                updateBoard(3,3,0.3)
            elif ran == "rook":
                updateBoard(3,3,0.4)
            else:
                updateBoard(3,3,0.5)
        elif board[4] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(4,4,0.2)
            elif ran == "bishop":
                updateBoard(4,4,0.3)
            elif ran == "rook":
                updateBoard(4,4,0.4)
            else:
                updateBoard(4,4,0.5)
        elif board[5] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(5,5,0.2)
            elif ran == "bishop":
                updateBoard(5,5,0.3)
            elif ran == "rook":
                updateBoard(5,5,0.4)
            else:
                updateBoard(5,5,0.5)
        elif board[6] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(6,6,0.2)
            elif ran == "bishop":
                updateBoard(6,6,0.3)
            elif ran == "rook":
                updateBoard(6,6,0.4)
            else:
                updateBoard(6,6,0.5)
        elif board[7] == 0.1:
            ran = input("what do you want to promote your pawn to")
            if ran == "knight":
                updateBoard(7,7,0.2)
            elif ran == "bishop":
                updateBoard(7,7,0.3)
            elif ran == "rook":
                updateBoard(7,7,0.4)
            else:
                updateBoard(7,7,0.5)
def inputFunction(original,new):
    updateBoard(original,new,board[original])
#unCompress()
#if input("what color are you?") == "white":
#    color = 0
#else:
#    color = 1
#if color == 0:
#    while True:
#        if run(color):
#            cacheTwo = cacheOne
#            cacheOne = board
#            print_screen()
#            inputOne = key.index(input("original"))
#            inputTwo = key.index(input("new"))
#            inputFunction(inputOne,inputTwo)
#            #user_promote()
#        else:
#            break    
#else:
#    while True:
#        inputOne = key.index(input("original"))
#        inputTwo = key.index(input("new"))
#        inputFunction(inputOne,inputTwo)
#        user_promote()
#        if run(color):
#            cacheTwo = cacheOne
#            cacheOne = board
#            print_screen()
#        else:
#            break

def sendToArduino(): #this sends the movement information to the arduino
    count = 0
    differences = []
    hold = [] #holds the data I need to send
    #finds every difference between the 2 boards and appends it into a list. 
    for i in board:
        if i != holder_board[count]:
            differences.append(count)
        count += 1
    #finds where the piece moved from 
    for i in differences:
        if board[i] == 0:
            hold.append(i)
        else:
            w = i
    hold.append(w)
    #checks if a piece needs to be removed 
    if holder_board[w] != 0:
        hold.append(1)
    #compiles the data into one string delimited by a space
    w = str(hold[0]) + " " + str(hold[1])
    if len(hold) == 3: #this is to prevent errors from taking a value that doesn't exist
        w = w + " " + hold[2]
    w = w + "\n" #the raspberry pi will be expecting a new line argument
    ser.write(w.encode('utf-8'))

#scans the board to check where every square is

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
IMG = rawCapture.array


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,default = IMG)
ap.add_argument("-t", "--type", type=str,
    default="DICT_4X4_250",
    help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# load the input image from disk and resize it
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)


# load the ArUCo dictionary, grab the ArUCo parameters, and detect
# the markers
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
    parameters=arucoParams)
temp = {} #this temporarily stores the coordinates with the ID, to make organization easier(because the aruco scanning code does not read it 1,2,3...)
# verify *at least* one ArUco marker was detected
if len(corners) > 0:
    # flatten the ArUco IDs list
    ids = ids.flatten()

    # loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        temp[markerID] = [topRight,bottomLeft]
#sorts the board positions 
tempTwo = sorted(temp)
for i in tempTwo:
    square_pos.append(temp.get(i))

#################################################
##SEND SIGNAL TO ARDUINO TO INDICATE THAT IT'S READY
#################################################

color = 0 #people are going to be locked white

#starts the actual AI
if color == 0:
    while True:
        readBoard()
        holder_board = board
        ser.flush()
        while ser.in_waiting < 0: #waits to recieve button press from arduino
            continue
        if run(color):
            cacheTwo = cacheOne
            cacheOne = board
            #user_promote()
        else:
            break    