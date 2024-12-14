import cv2
import numpy as np
import utils

curveList = []
avgVal = 10

def getLaneCurve(img,display=2) :

    imgCopy = img.copy()
    imgResult = img.copy()
    #Step 1
    imgThres = utils.threshholding(img)
    
    #Step 2
    hT,wT,c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utils.drawPoints(img,points)

    #Step 3
    middlePoint,imgHist = utils.getHistogram(imgWarp,display =True,minPer=0.5,region=4)
    curveAveragePoint,imgHist = utils.getHistogram(imgWarp,display =True,minPer=0.9)
    #print(basePoint-midPoint)
    curveRaw = curveAveragePoint - middlePoint

    #Step 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal :
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    #Display Step5
    if display != 0:
       imgInvWarp = utils.warpImg(imgWarp, points, wT, hT,inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:hT//3,0:wT] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = wT // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                            [imgHist,imgLaneColor,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
        print("Showing Stacks")
    elif display == 1:
        cv2.imshow('Resutlt',imgResult)

    #Normalization
    curve = curve/100
    if curve>1 : curve == 1
    if curve<-1 : curve == -1

    #vid windows hehe
    cv2.imshow('Threshold',imgThres)
    cv2.imshow('Warp it up hehe',imgWarp)
    cv2.imshow('Warp with points',imgWarpPoints)
    cv2.imshow('Histogram',imgHist)
    return curve



if __name__ == '__main__':
    cap = cv2.VideoCapture('/Users/wangzhan/Documents/Python/WRO/Kasetmatepathfollowyay/venv/vid1.mp4')
    initialTrackBarVals = [102,80,20,214]
    utils.initializeTrackbars(initialTrackBarVals)
    frameCounter = 0
    

    while True :
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0
        timer = cv2.getTickCount()
        
        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        curve = getLaneCurve(img,display=2)
        print(curveList)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(img, 'FPS: ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3)


        cv2.imshow('video' ,img)
        cv2.waitKey(1)