import os
import firebase_admin
from firebase_admin import credentials

basePath = os.path.dirname(__file__)
dataPath = os.path.join(basePath, "D:/Firebase Key/serviceAccountKey.json")
cred = credentials.Certificate(dataPath)
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-6ab4b-default-rtdb.asia-southeast1.firebasedatabase.app/"
})