import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

basePath = os.path.dirname(__file__)
dataPath = os.path.join(basePath, "D:/Firebase Key/serviceAccountKey.json")
cred = credentials.Certificate(dataPath)
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-6ab4b-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')

data = {
    "20240001":
        {
            "Name": "Thanh Binh",
            "Nghề nghiệp": "Sinh viên",
            "Năm bắt đầu": 2022,
            "Tổng buổi có mặt": 6,
            "Xếp loại": "G",
            "Năm học thứ": 4,
            "Thời gian điểm danh cuối": "2022-12-13 00:54:34"
        },

    "20240002":
        {
            "Name": "Elon Musk",
            "Nghề nghiệp": "Tỷ phú",
            "Năm bắt đầu": 2022,
            "Tổng buổi có mặt": 0,
            "Xếp loại": "G",
            "Năm học thứ": 0,
            "Thời gian điểm danh cuối": "2024-12-27 23:59:34"
        },
    "20240003":
        {
            "Name": "Thanh Binh 2",
            "Nghề nghiệp": "Sinh viên",
            "Năm bắt đầu": 2024,
            "Tổng buổi có mặt": 9,
            "Xếp loại": "G",
            "Năm học thứ": 1,
            "Thời gian điểm danh cuối": "2024-12-13 12:54:34"
        }

}

for key,value in data.items():
    ref.child(key).set(value)