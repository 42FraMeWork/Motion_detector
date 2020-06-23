import cv2, time
from datetime import datetime as dt
import pandas as pd

video = cv2.VideoCapture(0)

first_frame = None
status_list = [False, False]
times = []
df = pd.DataFrame(columns=['Start', 'End'])

while True:
    status = False
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)    

    if first_frame is None:
        first_frame = gray
        continue

    deltaframe = cv2.absdiff(first_frame, gray)
    
    
    treshframe = cv2.threshold(deltaframe, 30, 255, cv2.THRESH_BINARY)[1]
    treshframe = cv2.dilate(treshframe, None, iterations=2)

    cnts, _ = cv2.findContours(treshframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        status = True

    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] != status_list[-2]:
        times.append(dt.now())

    cv2.imshow("Gray", gray)
    cv2.imshow("Diff", deltaframe)
    cv2.imshow("Threshold", treshframe)
    cv2.imshow("color", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status:
            times.append(dt.now())
        break

for i in range(0, len(times), 2):
    df = df.append({'Start': times[i], 'End': times[i+1]}, ignore_index= True)
    

df.to_csv('Timestamps.csv')

video.release()
cv2.destroyAllWindows()