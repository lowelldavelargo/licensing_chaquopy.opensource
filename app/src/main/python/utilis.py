import cv2
import numpy as np

def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def rectCountour(countours):

    rectCon = []
    for i in countours:
        area = cv2.contourArea(i)
        #print("Area",area)
        if area>50:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            #print("Corner Points",len (approx))
            if len(approx)==4:
                rectCon.append(i)
        rectCon = sorted(rectCon,key=cv2.contourArea,reverse=True)

    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def splitBoxes(img):
    rows = np.vsplit(img,10)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,4)
        for box in cols:
            boxes.append(box)
    return boxes


def showAnswers(img,myIndex,ans,questions,choices):
    secW = int(img.shape[1] / questions)
    secH = int(img.shape[0] / choices)
    flag = 0
    color = 25
    for x in range(0, questions):
        for y in range(0, choices):
##########0
            if (myIndex[x] == 0 and flag == 0):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 150) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 0):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 150) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 0 ):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 150) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 0):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 150) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 0 ):
                flag += 1
                break
############1
            if (myIndex[x] == 0 and flag == 1):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 250) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 1):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 250) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 1):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 250) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 1):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 250) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 1 ):
                flag += 1
                break
##############2
            if (myIndex[x] == 0 and flag == 2):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 350) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 2):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 350) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 2):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 350) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 2):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 350) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 2 ):
                flag += 1
                break
############3
            if (myIndex[x] == 0 and flag == 3):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 450) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 3):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 450) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 3):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 450) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 3):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 450) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 3 ):
                flag += 1
                break
#################4
            if (myIndex[x] == 0 and flag == 4):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 550) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 4):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 550) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 4):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 550) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 4):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 550) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 4 ):
                flag += 1
                break
##########5
            if (myIndex[x] == 0 and flag == 5):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 650) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 5):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 650) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 5):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 650) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 5):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 650) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 5 ):
                flag += 1
                break
#############6
            if (myIndex[x] == 0 and flag == 6):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 760) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 6):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 760) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 6):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 760) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 6):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 760) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 6 ):
                flag += 1
                break
#############7
            if (myIndex[x] == 0 and flag == 7):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 860) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 7):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 860) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 7):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 860) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 7):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 860) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 7 ):
                flag += 1
                break
###############8
            if (myIndex[x] == 0 and flag == 8):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 970) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 8):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 970) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 8):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 970) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 8):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 970) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 8 ):
                flag += 1
                break
#############9
            if (myIndex[x] == 0 and flag == 9):
                cX = (0 * secW + 20) + secW
                cY = (x * secH - 1070) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 1 and flag == 9):
                cX = (1 * secW + 120) + secW
                cY = (x * secH - 1070) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 2 and flag == 9):
                cX = (2 * secW + 220) + secW
                cY = (x * secH - 1070) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == 3 and flag == 9):
                cX = (3 * secW + 320) + secW
                cY = (x * secH - 1070) + secH
                if(ans[x] == myIndex[x]):
                        myColor = (0,255,0)
                else: myColor = (255,0,0)
                cv2.circle(img, (cX, cY), color, myColor, cv2.FILLED)
                flag += 1
                break
            if (myIndex[x] == "no answer" or myIndex[x] == "wrong" and flag == 9 ):
                flag += 1
                break

    return img






