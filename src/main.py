import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone


basePath = os.path.dirname(__file__)
backgroundPath = os.path.join(basePath, "../Resources/Background.png")
folderModePath = os.path.join(basePath, "../Resources/Modes")
encodeFilePath = os.path.join(basePath, "../EncodeFile.p")

# Đọc ảnh nền
imgBackground = cv2.imread(backgroundPath)

# Đọc và lưu các chế độ hình ảnh vào danh sách
if not os.path.exists(folderModePath):
    print(f"Thư mục '{folderModePath}' không tồn tại!")
    exit()

modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgMode = cv2.imread(os.path.join(folderModePath, path))
    if imgMode is not None:
        imgModeList.append(imgMode)

print(f"Tổng số chế độ đã đọc: {len(imgModeList)}")

# Tải tệp mã hóa
if not os.path.exists(encodeFilePath):
    print(f"Tệp mã hóa không tồn tại tại đường dẫn: {encodeFilePath}")
    exit()

print("Đang tải tệp mã hóa ...")
with open(encodeFilePath, 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
print("Tệp mã hóa đã được tải thành công ...")

# Thiết lập camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()

    # Làm mới ảnh nền
    imgDisplay = imgBackground.copy()

    # Resize và chuyển đổi màu
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt và mã hóa
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgResized = cv2.resize(img, (563, 484))

    # Ghép ảnh video vào nền
    imgDisplay[220:220 + 484, 58:58 + 563] = imgResized
    imgDisplay[0:908, 790:790 + 419] = imgModeList[0]

    # Vẽ bounding box nếu phát hiện khuôn mặt
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            # Lấy tọa độ của khuôn mặt
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Thêm padding để mở rộng vùng bounding box
            padding_x = 10  # Padding ngang (giảm nếu cần)
            padding_y = 20  # Padding dọc (giảm nếu cần)
            
            # Tinh chỉnh tọa độ để căn chỉnh chính xác
            adjusted_x1 = max(30, x1 + 30 - padding_x)
            adjusted_x2 = min(30 + 563, x2 + 30 + padding_x)
            adjusted_y1 = max(200, y1 + 200 - padding_y)
            adjusted_y2 = min(200 + 484, y2 + 200 + padding_y)

            # Tính bounding box
            bbox = (adjusted_x1, adjusted_y1, adjusted_x2 - adjusted_x1, adjusted_y2 - adjusted_y1)
            imgDisplay = cvzone.cornerRect(imgDisplay, bbox, rt=0)




    # Hiển thị hình ảnh
    cv2.imshow("Face Attendance", imgDisplay)

    # Kiểm tra phím 'q' hoặc đóng cửa sổ
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Face Attendance", cv2.WND_PROP_VISIBLE) < 1:
        print("Cửa sổ đã bị đóng, dừng chương trình...")
        break

cap.release()
cv2.destroyAllWindows()
