#!/usr/bin/python2
import cv2
import urllib
import numpy as np
import itertools
import os
from time import sleep

def findKeyPoints(img, template, distance=200):
    #detector
    #detector = cv2.FeatureDetector_create("SIFT")
    #descriptor = cv2.DescriptorExtractor_create("SIFT")

    #skp = detector.detect(img)
    #skp, sd = descriptor.compute(img, skp)

    #tkp = detector.detect(template)
    #tkp, td = descriptor.compute(template, tkp)
    surf = cv2.SURF(400)
    skp, sd = surf.detectAndCompute(img,None)
    tkp, td = surf.detectAndCompute(template,None)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])

    return skp_final, tkp_final

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    pts = []
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        pts.append((pt_b[0]-w2,pt_b[1]))
        cv2.line(newimg, pt_a, pt_b, (127, 0, 0))
    pts.sort()
    ptsd = {}
    for i in pts:
        try:
            ptsd[i] = ptsd[i]+1
        except:
            ptsd[i] = 1
    return newimg,ptsd

def find_dist(l):
    if(len(l)==0):
        return 0
    p = l[0]
    o = l[1:]
    avgd = 0
    for i in o:
        avgd += ((p[1]-i[1])**2+(p[2]-i[2])**2)**(1/2)
    return avgd

def match():
    #Get image from the drone/webcam over web API
    req = urllib.urlopen('http://127.0.0.1:8002/img.jpg')
    arr = np.asarray(bytearray(req.read()),dtype=np.uint8)
    imgg = cv2.imdecode(arr,-1)
    #Preprocessing image
    img = cv2.cvtColor(imgg, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(5,5),0)
    _, img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #Getting pattern and processing it
    tempp = cv2.imread('pattern.jpg')
    pattern = cv2.cvtColor(tempp, cv2.COLOR_BGR2GRAY)
    _, pattern = cv2.threshold(pattern,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #SIFT/SURF + FLANN
    dist = 50
    num = -1
    skp, tkp = findKeyPoints(img, pattern, dist)

    #Draw keypoints in image and give cordinates of then
    matches, pts = drawKeyPoints(img, pattern, skp, tkp, num)
    newimg = imgg.copy()
    newtemp = pattern.copy()

    #Filter, only the most important keypoints (w>3)
    w = 3
    gptsx = []
    gptsy = []
    for i in pts:
        if(pts[i]<w):
            continue
        cv2.circle(newimg,i,pts[i]*2,(255,0,0),1)
        gptsx.append(i[0])
        gptsy.append(i[1])
    for i in range(0,len(tkp)):
        cv2.circle(newtemp,(int(tkp[i].pt[0]),int(tkp[i].pt[1])),2,(255,0,0),1)

    #Find the average keypoints position (the pattern has usually
    #90% of the detected points, we eliminate points far from it
    cx = sum(gptsx)/len(gptsx)
    cy = sum(gptsy)/len(gptsy)
    gpts = []
    for x,y in zip(gptsx,gptsy):
        gpts.append((x-cx)**2+(y-cy)**2)
    gptsm = min(sum(gpts)/len(gpts),5000)
    gpts = zip(gpts,gptsx,gptsy)
    gpts.sort()
    tmp = 0
    for i in gpts:
        if(i[0]<gptsm):
            tmp = tmp + 1
        else:
            break
    if(tmp<3):
        return
    gpts = gpts[:tmp]
    #print(gpts)
    dist = find_dist(gpts)
    duh,x,y = zip(*gpts)
    #print(dist,x,y)
    cx = int(sum(x)/len(x))
    cy = int(sum(y)/len(y))
    os.system("date")
    print(cx,cy,newimg.shape)
    if cx < newimg.shape[1]/2-50:
        print('goleft')
        #req = urllib.urlopen('http://127.0.0.1:8002/rotatel')
    if cx > newimg.shape[1]/2+50: 
        print('goright')
        #req = urllib.urlopen('http://127.0.0.1:8002/rotater')
    if cy > (newimg.shape[0]/2)+50:
        print('godown')
        req = urllib.urlopen('http://127.0.0.1:8002/down')
    if cy < (newimg.shape[0]/2)-50: 
        print('goup')
        req = urllib.urlopen('http://127.0.0.1:8002/up')
    #print(dist)
    if dist < 7:
        print('gofront')
        #req = urllib.urlopen('http://127.0.0.1:8002/front')
    if dist > 12:
        print('goback')
        #req = urllib.urlopen('http://127.0.0.1:8002/back')
    cv2.line(newimg,(0,cy),(10000,cy),(0,0,255))
    cv2.line(newimg,(cx,0),(cx,10000),(0,0,255))
    #cv2.imwrite("template_marked.jpg", newtemp)
    #cv2.imwrite("image_marked.jpg", newimg)
    #cv2.imwrite("matches.jpg", matches)
    cv2.imshow('template', newtemp)
    cv2.imshow('newimage', newimg)
    cv2.imshow('matches', matches)
    if cv2.waitKey() & 0xff == 27: return
    sleep(0.5)
match()
while True:
    try:
        match()
    except:
        print('error')
        break
req = urllib.urlopen('http://127.0.0.1:8002/down')
      #  req = urllib.urlopen('http://127.0.0.1:8002/down')
       # req = urllib.urlopen('http://127.0.0.1:8002/down')
req = urllib.urlopen('http://127.0.0.1:8002/stop')
req = urllib.urlopen('http://127.0.0.1:8002/land')
