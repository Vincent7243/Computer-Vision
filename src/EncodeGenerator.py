import cv2
import face_recognition
import pickle
import os

basePath = os.path.dirname(__file__)
folderPath = os.path.join(basePath, "../Images")
encodeFilePath = os.path.join(basePath, "../EncodeFile.p")


pathList = os.listdir(folderPath)
print(f"Danh sách ảnh: {pathList}")

imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

print(f"Danh sách ID sinh viên: {studentIds}")

def fineEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Bắt đầu quá trình mã hóa ...")
encodeListKnown = fineEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Quá trình mã hóa hoàn tất")

with open(encodeFilePath, 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print(f"Tệp mã hóa đã được lưu thành công tại: {encodeFilePath}")
