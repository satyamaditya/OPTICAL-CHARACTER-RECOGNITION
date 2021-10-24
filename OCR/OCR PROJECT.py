'''
Assignment By - ADITYA JHA

Project - Extract invoice number, invoice date, line items from invoice images.

Project Details - After my research toward this assignment, i found, this is the problem of OCR (OPTICAL CHARACTER RECOGNITION)
                  Basically the work of OCR is to transform & extract the data from semi-structured(BILLs, INVOICES)
                  or un-structured(CONTRACT, LEGAL DOCUMENTS) to structured format(CSV, EXCEL, XML, DATABASES).
                  Although TOOLS of OCR are available in the market like- ABBYY, ROSSUM, AUTOMATION ANYWHERE, XTRACTA,
                  But just for the sake of Assignment, I did this Project with the help of CV2 (Computer Vision) and PYTESSERACT (python library
                  for OCR).
'''

# importing required libraries.............................

import pytesseract
import cv2
import os
import random
pytesseract.pytesseract.tesseract_cmd=r'C:\\Users\\aditya\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


'''here, i just import the entire IMAGE directory with the help of OS library of python,
   and read image with the help of CV2 (computer vision)'''

for j,i in enumerate(os.listdir('C:\\Users\\aditya\\Downloads\\assignmentPic\\')):     # use enumerate just for getting INDEX also
    img=cv2.imread('C:\\Users\\aditya\\Downloads\\assignmentPic\\'+i)
    img1= cv2.resize(img, (1230, 1170))                                               # i have to resize this, to see the entire image.

    mydata=[]                                                                        # created list, just to store info of invoice no.,date & line item

    print(f'#########----extracting data from TEST{j}------###################')

    ''' for extracting the info from images, 1st of all, i have to give coordinates points to find REGION OF INTEREST, 
    and crop the particular area, from where PYTESSERACT can extract the data without getting any MESSY text.
    '''
    # FUNCTION OF FINDING REGION OF INTEREST.........................
    circle = []
    counter = 0
    counter2 = 0
    point1 = []
    point2 = []
    mypoints = []
    mycolor = []


    def mousepoints(event, x, y, flags, params):
        global counter, point1, point2, counter2, circle, mycolor
        if event == cv2.EVENT_LBUTTONDOWN:
            if counter == 0:
                point1 = int(x ), int(y );
                counter += 1
                mycolor = (random.randint(0, 2) * 200, random.randint(0, 2) * 200, random.randint(0, 2) * 200)
            elif counter == 1:
                point2 = int(x ), int(y )
                name = input('enter name:-')
                mypoints.append([point1, point2, name])
                counter = 0
            circle.append([x, y, mycolor])
            counter2 += 1


    while True:
        # to display the points.....
        for x, y, color in circle:
            cv2.circle(img1, (x, y), 3, color, cv2.FILLED)
        cv2.imshow('original', img1)
        cv2.setMouseCallback('original', mousepoints)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            roi = mypoints                              # here i got REGION OF INTEREST.
            break
    print(roi)
    for x,r in enumerate(roi):
        imgcrop=img1[r[0][1]:r[1][1],r[0][0]:r[1][0]]         # crop the REGION OF INTEREST....
        cv2.imshow(str(x),imgcrop)
        print(f'{r[2]}: {pytesseract.image_to_string(imgcrop)}')         # print for the sake of view.
        mydata.append(pytesseract.image_to_string(imgcrop).replace('\n',' '))   # here i APPEND info(invoice no., date & line items) in list


    ''' with the help of FILE I/O, we append/write the data into CSV file
    '''

    with open('invoice.csv','a+') as f:
        for data in mydata:
            f.write(str(data)+',')
        f.write('\n')

cv2.waitKey(0)
cv2.destroyAllWindows()

''' in the end, i complete my assignment
    i develop this project STATICALLY because the format & structure of all Invoice images
    was pretty different. I can develop this project DYNAMICALLY too, If the format & structure of each image was same,
    we can easily extract all of the information in ONE GO.
    {HERE I HAD TO FIND REGION OF INTEREST OF EACH IMAGE (one by one, inside the for loop), because Format is different}
'''


