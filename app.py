from flask import Flask, request, jsonify
#import torch
from PIL import Image
import io
from pyzbar.pyzbar import decode

app = Flask(__name__)

# YOLOv5 모델 로드
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='./yolov5x.pt', force_reload=True)

@app.route('/')
def index():
    return "AI Server is running!"

@app.route('/detect_barcode', methods=['POST'])
def detect_barcode():
    if 'file' not in request.files:
        return jsonify({'error': "파일 부분이 없습니다"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': "선택된 파일이 없습니다"}), 400

    # 이미지 파일 읽기
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))

    # 바코드 숫자 추출
    barcodes = decode(img)
    barcode_numbers = [barcode.data.decode('utf-8') for barcode in barcodes]

    if not barcode_numbers:
        return jsonify({'result': 0, 'message': 'No barcodes detected'}), 200
    else:
        return jsonify({'result': 1, 'barcodes': barcode_numbers}), 200

'''
@app.route('/detect_ai', methods=['POST'])
def detect_ai():
    if 'file' not in request.files:
        return jsonify({'error': "파일 부분이 없습니다"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': "선택된 파일이 없습니다"}), 400

    # 이미지 파일 읽기
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))

    # 객체 탐지 수행
    results = model(img, size=640)
    results.render()  # 탐지된 객체를 이미지에 그리기

    high_conf_barcodes = []
    for i, (*xyxy, conf, cls) in enumerate(results.xyxy[0]):
        # 좌표와 신뢰도 점수를 파이썬 정수와 부동소수점으로 명시적으로 변환
        x1, y1, x2, y2 = map(int, map(lambda x: x.item(), xyxy))
        conf = conf.item()

        if conf >= 0.6:  # 신뢰도가 0.6 이상인 경우만 처리
            crop_img = img.crop((x1, y1, x2, y2))
            barcodes = decode(crop_img)
            barcode_numbers = [barcode.data.decode('utf-8') for barcode in barcodes]
            high_conf_barcodes.extend(barcode_numbers)

    if not high_conf_barcodes:  # 정확도가 0.6 이상인 바코드를 인식하지 못한 경우
        return jsonify({'result': 0, 'message': 'No high-confidence barcodes detected'}), 200
    else:
        # 정확도가 0.6 이상인 바코드 숫자 추출 결과 반환
        return jsonify({'result': 1, 'barcodes': high_conf_barcodes}), 200
'''
if __name__ == '__main__':
    app.run(debug=True, port=5001)