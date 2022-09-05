from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST" :
        imagefile = request.files['image']
        filename = "output.jpg"
        print("\nReceived image File name : " + imagefile.filename)
        imagefile.save("./images/" + filename)
        img = Image.open(imagefile.stream)
        return jsonify({
            "message": "Image Uploaded Successfully ",
        })
        
        
@app.route('/proses', methods=['GET'])
def image_proses():    
    scalePercent = 1
    image = cv2.imread('./images/output.jpg')                
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define white color range
    lowerWhite = np.array([0,0,168])
    upperWhite = np.array([172,111,255])

    lowerYellow = np.array([0, 0, 0])
    upperYellow = np.array([255, 255, 200])

    lowerBlack = np.array([0, 0, 0])
    upperBlack = np.array([255, 255, 140])
    
    lowerPatah = np.array([0, 0, 0])
    upperPatah = np.array([255, 255, 160])

    # Threshold the HSV image to get only blue colors
    maskWhite = cv2.inRange(hsv, lowerWhite, upperWhite)
    maskYellow = cv2.inRange(hsv, lowerYellow, upperYellow)
    maskBlack = cv2.inRange(hsv, lowerBlack, upperBlack)
    maskPatah = cv2.inRange(hsv, lowerPatah, upperPatah)
    
    #white count presentase
    whiteRation = cv2.countNonZero(maskWhite)/(image.size/3)
    whiteColor = (whiteRation* 100) / scalePercent
    whiteResult = np.round(whiteColor,1)
    
    
    #yellow count presentase
    yellowRation = cv2.countNonZero(maskYellow)/(image.size/0.2)
    yellowColor = (yellowRation* 100) / scalePercent
    yellowResult = np.round(yellowColor,2)

    #black count presentase
    blackRation = cv2.countNonZero(maskBlack)/(image.size/0.1)
    blackColor = (blackRation* 100) / scalePercent
    blackResult = np.round(blackColor,2)
    
    patahRation = cv2.countNonZero(maskPatah)/(image.size/0.1)
    patahColor = (patahRation* 100) / scalePercent
    patahResult = np.round(patahColor,2)
        
    print(f"Persentase warna putih {whiteResult}%")
    print(f"Persentase warna kuning {yellowResult}%")
    print(f"Persentase warna kuning {blackResult}%")
    print(f"Persentase warna kuning {patahResult}%")
    
    return jsonify({
        'beras_putih': whiteResult,
        'beras_kuning': yellowResult,
        'beras_hitam': blackResult,
        'beras_patah': patahResult,
    })
    

    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
