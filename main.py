import cv2
from PIL import Image
from util import get_limits

colors = {
    "Blue": [255, 0, 0],
    "Green": [0, 255, 0],
    "Red": [0, 0, 255]
}

cap = cv2.VideoCapture(0)

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

            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_value, 5)
            cv2.putText(frame, color_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, bgr_value, 2, cv2.LINE_AA)

            detected_color = color_name
            #break  # ถ้าเจอสีไหนแล้วก็ไม่ต้องตรวจสีอื่นในเฟรมนี้

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
