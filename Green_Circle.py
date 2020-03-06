import cv2
import numpy as np
import sys
import zedstreamer
kernel_size = 5 #for gaussian filter

if __name__ == '__main__':


    # ZedCamera()
    # zed.setCamSettings(brightness=4,
    #                    contrast=0,
    #                    hue=0,
    #                    sat=4,
    #                    gain=60,
    #                    exp=75)

    # zed.setCamSettings(brightness=6,
    #                    contrast=5,
    #                    hue=0,
    #                    sat=4,
    #                    gain=60,
    #                    exp=200)


    i = 0
    zed = zedstreamer.ZedCamera()
    while True:
        #ret, src = zed.read()
        image = zed.getImage("Right")
        # src = np.array(src[:, :, :3])
        
        # filter with guassian blur
        blur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

        #convert to HSV - mask for green
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (40, 40, 40), (70, 255, 255))

        #threshold
        ret2, threshImage = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(threshImage, kernel, iterations=1)
        opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

        #contour
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        # calculate Area
        for c in contours:
            area = cv2.contourArea(c)

            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            area2 = 3.14 * radius * radius

            x, y, w, h = cv2.boundingRect(c)
            areaRect = (int(w) * int(h))

            if area > 300 and area / area2 > 0.6:
                img = cv2.circle(image, center, radius, (255, 0, 0), 2)

                cv2.putText(img, 'Area: ' + str(area),
                            center,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 0))
                #cv2.putText(image, "Area: " + str(area), (x-20, y), cv2.CV_FONT_HERSHEY_SIMPLEX, 2, 255)
                if area/areaRect > 0.25:
                    # draw a green rectangle to visualize the bounding rect
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if image is not None:

            cv2.imshow("Original",image)
            cv2.imshow('Frame',mask)

            keyPressed = cv2.waitKey(33)
            if keyPressed == ord("s"):
                cv2.imwrite("{}_{}.png".format("debu_output", i), vision.getSourceImg())
                i += 1
            elif keyPressed == ord("q"):
                cv2.destroyAllWindows()
                sys.exit()
