import cv2
import time
import os
import hand as htm


pTime = 0

cap = cv2.VideoCapture(0)  #1 webcam nên id sẽ mặc định là 0, nếu nhiều video có thể id la 1, 2, 3 4

FolderPath = "Fingers"
lst = os.listdir(FolderPath)
lst_2 = []
for i in lst:
    image = cv2.imread(f"{FolderPath}/{i}")
    print(f"{FolderPath}/{i}")
    lst_2.append(image)

detector = htm.handDetector(detectionCon=1)  # Sử dụng giá trị số nguyên đại diện cho ngưỡng tin cậy

fingerid = [4,8,12,16,20]
while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)  #Phát hiện vị trí
    print(lmList)


    if len(lmList) != 0:
        fingers = []

        #Viết cho ngón cái(điểm 4 nằm bên trái hay phải của điểm 3 )
        if lmList[fingerid[0]][1] < lmList[fingerid[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)



    #Viết cho ngón dài
        for id in range(1,5):
            if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)

        songontay = fingers.count(1)
        print(songontay)

    # chú ý mỗi bức ảnh sẽ đẩy về giá trị của 1 mảng có chiều rông, cao khác nhau
    # ví dụ ảnh 0.png : print(lst_2[0].shape) kết quả (126, 110, 3)
    # frame[0:126,0:110] = lst_2[0]
    # do các bức ảnh 0-5.png khác nhau các giá trị wisth, height nên phải get theo shape
        h, w, c = lst_2[songontay - 1].shape
        frame[0:h, 0:w] = lst_2[songontay - 1]  # nếu số ngón tay =0 thì lst_2[-1] đẩy về phần tử cuối cùng của list là ảnh 6

        # vẽ thêm hình chữ nhật hiện số ngón tay
        cv2.rectangle(frame,(0,200),(150,400),(0,255,0),-1)
        cv2.putText(frame,str(songontay),(30,390),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),5)

    #Viết ra fps
    cTime = time.time()   #Trả về số giây, tính từ 0:00:00 ngày 1/1/1970 theo gờ utc, gọi là (thời điểm bắt đầu thời gian)
    fps = 1/(cTime-pTime) #Tính fps Frames per-second - đây là chỉ số khung hình trên mỗi giây
    pTime = cTime
    #Show fps ra màn hình
    cv2.putText(frame,f"FPS: {int(fps)}",(150,170), cv2.FONT_HERSHEY_PLAIN, 3, (225,0,0),3)



    cv2.imshow("Đọc ảnh", frame)
    if cv2.waitKey(1) == ord("q"): #Độ trễ 1/1000s, nếu bấm q sẽ thoát
        break
cap.release() #Giải phóng camera
cv2.destroyAllWindows() #Thoát tất cả cửa sổ