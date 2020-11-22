import cv2
import numpy as np
import utilis
import base64
import io
from PIL import Image

def main(data):
    questions = 10
    choices = 4
    widthImg = 700
    heightImg = 700
    answer_1 = [1, 1, 1, 1, 0, 0, 3, 3, 1, 3]
    answer_2 = [2, 1, 2, 1, 2, 1, 2, 1, 0, 0]
    answer_3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    answer_4 = [0, 0, 1, 0, 1, 2, 3, 2, 1, 2]


    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgBiggestContours = img.copy()
    imgFinal = img.copy()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)
    rectCon = utilis.rectCountour(contours)
    biggestContour = utilis.getCornerPoints(rectCon[3])
    biggestContour_1 = utilis.getCornerPoints(rectCon[0])
    biggestContour1 = utilis.getCornerPoints(rectCon[2])
    biggestContour2 = utilis.getCornerPoints(rectCon[1])

    if biggestContour.size != 0 and biggestContour_1.size != 0 and biggestContour1.size != 0 and biggestContour2.size != 0:
        cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour_1, -1, (0, 255, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour1, -1, (255, 0, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour2, -1, (255, 0, 0), 20)

    biggestContour = utilis.reorder(biggestContour)
    biggestContour_1 = utilis.reorder(biggestContour_1)
    biggestContour1 = utilis.reorder(biggestContour1)
    biggestContour2 = utilis.reorder(biggestContour2)

    # first
    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # second
    pt1_1 = np.float32(biggestContour_1)
    pt2_1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1, pt2_1)
    imgWarpColored_1 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # third
    pt1_1_1 = np.float32(biggestContour1)
    pt2_1_1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1_1, pt2_1_1)
    imgWarpColored_2 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # fourth
    pt1_1_2 = np.float32(biggestContour2)
    pt2_1_2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1_2, pt2_1_2)
    imgWarpColored_3 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # APPLY THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_1
    imgWarpGray_1 = cv2.cvtColor(imgWarpColored_1, cv2.COLOR_BGR2GRAY)
    imgThresh_1 = cv2.threshold(imgWarpGray_1, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_2
    imgWarpGray_2 = cv2.cvtColor(imgWarpColored_2, cv2.COLOR_BGR2GRAY)
    imgThresh_2 = cv2.threshold(imgWarpGray_2, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_3
    imgWarpGray_3 = cv2.cvtColor(imgWarpColored_3, cv2.COLOR_BGR2GRAY)
    imgThresh_3 = cv2.threshold(imgWarpGray_3, 100, 255, cv2.THRESH_BINARY_INV)[1]

    boxes_1 = utilis.splitBoxes(imgThresh)
    # cv2.imshow("Test",boxes_1[3])
    boxes_2 = utilis.splitBoxes(imgThresh_1)
    # cv2.imshow("Test1",boxes_1 [30])
    boxes_3 = utilis.splitBoxes(imgThresh_2)
    # cv2.imshow("Test2",boxes_2 [7])
    boxes_4 = utilis.splitBoxes(imgThresh_3)
    # cv2.imshow("Test3",boxes_3 [4])

    #############
    myPixelVal_1 = np.zeros((questions, choices))
    countC = 0
    countR = 0
    for image in boxes_1:
        totalpixels = cv2.countNonZero(image)
        myPixelVal_1[countR][countC] = totalpixels
        countC += 1
        if (countC == choices): countR += 1; countC = 0
        myIndex_1 = []
        for x in range(0, questions):
            counter = 0
            redunt = 0
            finalcounter = 0
            for y in range(0, choices):
                if (myPixelVal_1[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_1.append(data)
                            redunt += 1
                        else:
                            myIndex_1.pop();myIndex_1.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_1.append("no answer")
    ######################

    #################
    myPixelVal_2 = np.zeros((questions, choices))
    countC1 = 0
    countR1 = 0

    for image in boxes_2:
        totalpixels1 = cv2.countNonZero(image)
        myPixelVal_2[countR1][countC1] = totalpixels1
        countC1 += 1
        if (countC1 == choices): countR1 += 1; countC1 = 0
        myIndex_2 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_2[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_2.append(data)
                            redunt += 1
                        else:
                            myIndex_2.pop();myIndex_2.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_2.append("no answer")
    ###################

    #############################
    myPixelVal_3 = np.zeros((questions, choices))
    countC2 = 0
    countR2 = 0

    for image in boxes_3:
        totalpixels2 = cv2.countNonZero(image)
        myPixelVal_3[countR2][countC2] = totalpixels2
        countC2 += 1
        if (countC2 == choices): countR2 += 1; countC2 = 0
        myIndex_3 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_3[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_3.append(data)
                            redunt += 1
                        else:
                            myIndex_3.pop();myIndex_3.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_3.append("no answer")
    ###################

    #############################
    myPixelVal_4 = np.zeros((questions, choices))
    countC3 = 0
    countR3 = 0

    for image in boxes_4:
        totalpixels3 = cv2.countNonZero(image)
        myPixelVal_4[countR3][countC3] = totalpixels3
        countC3 += 1
        if (countC3 == choices): countR3 += 1; countC3 = 0
        myIndex_4 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_4[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_4.append(data)
                            redunt += 1
                        else:
                            myIndex_4.pop();myIndex_4.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_4.append("no answer")
    ###################

    #############################




    # Displaying Answer
    imgResult = imgWarpColored.copy()
    imgRawDrawing = np.zeros_like(imgResult)
    imgRawDrawing = utilis.showAnswers(imgRawDrawing, myIndex_1, answer_1, questions, choices)
    invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
    imgInWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp, 1, 0)

    imgResult_1 = imgWarpColored_1.copy()
    imgRawDrawing_1 = np.zeros_like(imgResult_1)
    imgRawDrawing_1 = utilis.showAnswers(imgRawDrawing_1, myIndex_2, answer_2, questions, choices)
    invMatrix_1 = cv2.getPerspectiveTransform(pt2_1, pt1_1)
    imgInWarp_1 = cv2.warpPerspective(imgRawDrawing_1, invMatrix_1, (widthImg, heightImg))
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp_1, 1, 0)

    imgResult_2 = imgWarpColored_2.copy()
    imgRawDrawing_2 = np.zeros_like(imgResult_2)
    imgRawDrawing_2 = utilis.showAnswers(imgRawDrawing_2, myIndex_3, answer_3, questions, choices)
    invMatrix_2 = cv2.getPerspectiveTransform(pt2_1_1, pt1_1_1)
    imgInWarp_2 = cv2.warpPerspective(imgRawDrawing_2, invMatrix_2, (widthImg, heightImg))
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp_2, 1, 0)

    imgResult_3 = imgWarpColored_3.copy()
    imgRawDrawing_3 = np.zeros_like(imgResult_3)
    imgRawDrawing_3 = utilis.showAnswers(imgRawDrawing_3, myIndex_4, answer_4, questions, choices)
    invMatrix_3 = cv2.getPerspectiveTransform(pt2_1_2, pt1_1_2)
    imgInWarp_3 = cv2.warpPerspective(imgRawDrawing_3, invMatrix_3, (widthImg, heightImg))
    imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp_3, 1, 0)

    pil_im =Image.fromarray(imgFinal)
    buff = io.BytesIO()
    pil_im.save(buff,format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return "" +str(img_str,'utf-8')

###########################################################
###########################################################
###########################################################

def main1(data):
    questions = 10
    choices = 4
    widthImg = 700
    heightImg = 700
    answer_1 = [1, 1, 1, 1, 0, 0, 3, 3, 1, 3]
    answer_2 = [2, 1, 2, 1, 2, 1, 2, 1, 0, 0]
    answer_3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    answer_4 = [0, 0, 1, 0, 1, 2, 3, 2, 1, 2]


    decoded_data = base64.b64decode(data)
    np_data = np.fromstring(decoded_data,np.uint8)
    img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgBiggestContours = img.copy()
    imgFinal = img.copy()
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)
    rectCon = utilis.rectCountour(contours)
    biggestContour = utilis.getCornerPoints(rectCon[3])
    biggestContour_1 = utilis.getCornerPoints(rectCon[0])
    biggestContour1 = utilis.getCornerPoints(rectCon[2])
    biggestContour2 = utilis.getCornerPoints(rectCon[1])

    if biggestContour.size != 0 and biggestContour_1.size != 0 and biggestContour1.size != 0 and biggestContour2.size != 0:
        cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour_1, -1, (0, 255, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour1, -1, (255, 0, 0), 20)
        cv2.drawContours(imgBiggestContours, biggestContour2, -1, (255, 0, 0), 20)

    biggestContour = utilis.reorder(biggestContour)
    biggestContour_1 = utilis.reorder(biggestContour_1)
    biggestContour1 = utilis.reorder(biggestContour1)
    biggestContour2 = utilis.reorder(biggestContour2)

    # first
    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # second
    pt1_1 = np.float32(biggestContour_1)
    pt2_1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1, pt2_1)
    imgWarpColored_1 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # third
    pt1_1_1 = np.float32(biggestContour1)
    pt2_1_1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1_1, pt2_1_1)
    imgWarpColored_2 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # fourth
    pt1_1_2 = np.float32(biggestContour2)
    pt2_1_2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1_1_2, pt2_1_2)
    imgWarpColored_3 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    # APPLY THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_1
    imgWarpGray_1 = cv2.cvtColor(imgWarpColored_1, cv2.COLOR_BGR2GRAY)
    imgThresh_1 = cv2.threshold(imgWarpGray_1, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_2
    imgWarpGray_2 = cv2.cvtColor(imgWarpColored_2, cv2.COLOR_BGR2GRAY)
    imgThresh_2 = cv2.threshold(imgWarpGray_2, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # APPLY THRESHOLD_3
    imgWarpGray_3 = cv2.cvtColor(imgWarpColored_3, cv2.COLOR_BGR2GRAY)
    imgThresh_3 = cv2.threshold(imgWarpGray_3, 100, 255, cv2.THRESH_BINARY_INV)[1]

    boxes_1 = utilis.splitBoxes(imgThresh)
    # cv2.imshow("Test",boxes_1[3])
    boxes_2 = utilis.splitBoxes(imgThresh_1)
    # cv2.imshow("Test1",boxes_1 [30])
    boxes_3 = utilis.splitBoxes(imgThresh_2)
    # cv2.imshow("Test2",boxes_2 [7])
    boxes_4 = utilis.splitBoxes(imgThresh_3)
    # cv2.imshow("Test3",boxes_3 [4])

    #############
    myPixelVal_1 = np.zeros((questions, choices))
    countC = 0
    countR = 0
    for image in boxes_1:
        totalpixels = cv2.countNonZero(image)
        myPixelVal_1[countR][countC] = totalpixels
        countC += 1
        if (countC == choices): countR += 1; countC = 0
        myIndex_1 = []
        for x in range(0, questions):
            counter = 0
            redunt = 0
            finalcounter = 0
            for y in range(0, choices):
                if (myPixelVal_1[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_1.append(data)
                            redunt += 1
                        else:
                            myIndex_1.pop();myIndex_1.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_1.append("no answer")
    ######################
    score_1 = 0
    for x in range(0, questions):
        if answer_1[x] == myIndex_1[x]:
            score_1 += 1
        else:
            score_1 += 0
    #################
    myPixelVal_2 = np.zeros((questions, choices))
    countC1 = 0
    countR1 = 0

    for image in boxes_2:
        totalpixels1 = cv2.countNonZero(image)
        myPixelVal_2[countR1][countC1] = totalpixels1
        countC1 += 1
        if (countC1 == choices): countR1 += 1; countC1 = 0
        myIndex_2 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_2[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_2.append(data)
                            redunt += 1
                        else:
                            myIndex_2.pop();myIndex_2.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_2.append("no answer")
    ###################
    score_2 = 0
    for x in range(0, questions):
        if answer_2[x] == myIndex_2[x]:
            score_2 += 1
        else:
            score_2 += 0
    #############################
    myPixelVal_3 = np.zeros((questions, choices))
    countC2 = 0
    countR2 = 0

    for image in boxes_3:
        totalpixels2 = cv2.countNonZero(image)
        myPixelVal_3[countR2][countC2] = totalpixels2
        countC2 += 1
        if (countC2 == choices): countR2 += 1; countC2 = 0
        myIndex_3 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_3[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_3.append(data)
                            redunt += 1
                        else:
                            myIndex_3.pop();myIndex_3.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_3.append("no answer")
    ###################
    score_3 = 0
    for x in range(0, questions):
        if answer_3[x] == myIndex_3[x]:
            score_3 += 1
        else:
            score_3 += 0
    #############################
    myPixelVal_4 = np.zeros((questions, choices))
    countC3 = 0
    countR3 = 0

    for image in boxes_4:
        totalpixels3 = cv2.countNonZero(image)
        myPixelVal_4[countR3][countC3] = totalpixels3
        countC3 += 1
        if (countC3 == choices): countR3 += 1; countC3 = 0
        myIndex_4 = []
        for x in range(0, questions):
            counter = 0
            finalcounter = 0
            redunt = 0
            for y in range(0, choices):
                if (myPixelVal_4[x][y] >= 1200):
                    if (finalcounter < 1):
                        if (redunt < 1):
                            data = y
                            myIndex_4.append(data)
                            redunt += 1
                        else:
                            myIndex_4.pop();myIndex_4.append("wrong");finalcounter += 1
                else:
                    counter += 1
                if (counter == 4):
                    myIndex_4.append("no answer")
    ###################
    score_4 = 0
    for x in range(0, questions):
        if answer_4[x] == myIndex_4[x]:
            score_4 += 1
        else:
            score_4 += 0
    #############################

    finalscore = score_1 + score_2 + score_3 + score_4
    return "Score is: " +str(finalscore)










