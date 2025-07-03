import cv2
from PIL import Image
import serial
import time
from util import get_limits

# กำหนดสีใน BGR พร้อมชื่อ
colors = {
    "Blue": [255, 0, 0],
    "Green": [0, 255, 0],
    "Red": [0, 0, 255]
}

# เปิดพอร์ต Serial ให้ตรงกับพอร์ตที่ Arduino เชื่อมต่อ (เช่น COM3, /dev/ttyUSB0)
ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # รอให้พอร์ต Serial พร้อมใช้งาน

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_color = None

    for color_name, bgr_value in colors.items():
        lowerLimit, upperLimit = get_limits(color=bgr_value)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox

            # วาดกรอบสี่เหลี่ยมและชื่อสี
            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_value, 5)
            cv2.putText(frame, color_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, bgr_value, 2, cv2.LINE_AA)

            detected_color = color_name
            break  # ถ้าเจอสีไหนแล้วก็ไม่ต้องตรวจสีอื่นในเฟรมนี้

    # ส่งข้อความสีไปยัง Arduino ถ้าตรวจพบสี
    if detected_color is not None:
        ser.write((detected_color + '\n').encode('utf-8'))
    else:
        # ส่งข้อความว่างหรือปิดไฟ (ถ้าต้องการ)
        ser.write(b'None\n')

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
