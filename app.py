from flask import Flask, request, jsonify
#mport torch
#from PIL import Image
import io
#import base64
#import numpy as np
#import cv2

app = Flask(__name__)

# YOLOv5 모델 로드
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='./yolov5x.pt', force_reload=True)
@app.route('/')
def index():
    return "AI Server is running!"

# 첫 번째 엔드포인트: 항상 같은 바코드 번호 반환
@app.route('/detect_fixed', methods=['POST'])
def detect_fixed():
    if 'file' not in request.files:
        return jsonify({'error': "파일 부분이 없습니다"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': "선택된 파일이 없습니다"}), 400
    # 항상 같은 바코드 번호 반환
    return jsonify({'barcode': "880123456893"}), 200
'''
# 두 번째 엔드포인트: AI 모델을 사용하여 바코드 객체 추출 및 숫자 추출
@app.route('/detect_ai', methods=['POST'])
def detect_ai():
    if 'file' not in request.files:
        return jsonify({'error': "파일 부분이 없습니다"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': "선택된 파일이 없습니다"}), 400
    if file:
        # 이미지 파일 읽기
        image_bytes = file.read()
        img = Image.open(io.BytesIO(image_bytes))

        # 객체 탐지 수행
        results = model(img, size=640)
        results.render()  # 탐지된 객체를 이미지에 그리기
        
        # 정확도 필터링 및 클래스 이름 추출
        extracted_barcodes = []
        for *xyxy, conf, cls in results.xyxy[0]:
            if conf >= 0.6:  # 정확도가 0.6 이상인 경우
                class_name = results.names[int(cls)]
                extracted_barcodes.append(class_name)
        
        if not extracted_barcodes:  # 바코드를 인식하지 못한 경우
            return jsonify({'result': 0}), 200
        else:
            # 바코드 숫자 추출 로직 (여기서는 예시로 클래스 이름을 반환)
            return jsonify({'result': 1, 'barcodes': extracted_barcodes}), 200
'''
if __name__ == '__main__':
    app.run(debug=True, port=5001)