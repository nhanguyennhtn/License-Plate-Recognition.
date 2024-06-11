from flask import Flask, request, jsonify, Blueprint
from ultralytics import YOLO
import base64
from io import BytesIO
<<<<<<< Updated upstream
=======
import os
import torch
import tkinter as tk
from tkinter import filedialog
import time
>>>>>>> Stashed changes

webcam_bp = Blueprint('webcam', __name__)

# Load the YOLOv8 model
model = YOLO("D:/TTTe/code/Version_Kq/bestAuto43.pt")
<<<<<<< Updated upstream
=======
reader = easyocr.Reader(['en'])
>>>>>>> Stashed changes


def decode_image(image_data):
    header, encoded = image_data.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return np.array(image)

<<<<<<< Updated upstream
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image
=======
def filter_ocr_result(ocr_result):
    filtered_result = []
    for detection in ocr_result:
        text = detection[1]  # Giả sử detection là một tuple và text là phần tử thứ hai
        filtered_text = ''.join([char for char in text if char not in ['-', '"', '.','*',' ',',']])
        filtered_result.append(filtered_text)
    return filtered_result
>>>>>>> Stashed changes

@webcam_bp.route('/api/webcam-model', methods=['POST'])
def upload_frame_external():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
    image_data = data['image']
    image_np = decode_image(image_data)

<<<<<<< Updated upstream
    results = model.predict(image_np)

    if results:
        # Lấy thông tin các khung bao và nhãn từ kết quả dự đoán
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Tọa độ khung bao
        classes = results[0].boxes.cls.cpu().numpy()  # Các lớp (chỉ số) của các đối tượng
        names = results[0].names  # Tên các lớp đối tượng
=======
    # Đo thời gian giải mã hình ảnh từ base64
    start_time = time.time()
    image = decode_image(image_base64)
    decode_time = time.time() - start_time

    # Đo thời gian lưu hình ảnh dưới định dạng JPEG
    start_time = time.time()
    temp_image_path = "temp_image1.jpeg"
    save_image_as_jpeg(image, temp_image_path)
    save_time = time.time() - start_time

    # Đo thời gian mở hình ảnh từ tệp JPEG
    start_time = time.time()
    jpeg_image = Image.open(temp_image_path)
    open_time = time.time() - start_time

    # Đo thời gian dự đoán đối tượng bằng mô hình YOLO
    start_time = time.time()
    results = model.predict(jpeg_image)
    predict_time = time.time() - start_time

    detected_objects = []
    chars = []
    converted_labels = []
    ocr_result = []

    # Đo thời gian xử lý kết quả dự đoán và OCR
    start_time = time.time()
    for result in results:
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        names = result.names
>>>>>>> Stashed changes

        # Tạo danh sách các đối tượng cùng với tọa độ khung bao
        detected_objects = [(names[int(cls)], (x1, y1, x2, y2)) for cls, (x1, y1, x2, y2) in zip(classes, boxes)]

<<<<<<< Updated upstream
        # Chuyển đổi tọa độ YOLO thành tọa độ trung bình của các khung bao
        converted_labels = [(int((x1 + x2) / 2), int((y1 + y2) / 2)) for (x1, y1, x2, y2) in boxes]

        # Tính toán tọa độ trung bình theo trục y của toàn bộ biển số
        all_y_centers = [y for _, (x, y) in zip(detected_objects, converted_labels)]
        avg_y = sum(all_y_centers) / len(all_y_centers) if all_y_centers else 0

        # Phân loại các đối tượng vào phần trên hoặc phần dưới dựa trên tọa độ trung tâm của chúng
        upper_half = [(obj, center) for obj, center in zip(detected_objects, converted_labels) if center[1] <= avg_y]
        lower_half = [(obj, center) for obj, center in zip(detected_objects, converted_labels) if center[1] > avg_y]

        # Sắp xếp các đối tượng trong phần trên từ trái sang phải
        sorted_upper_half = sorted(upper_half, key=lambda x: x[1][0])

        # Sắp xếp các đối tượng trong phần dưới từ trái sang phải
        sorted_lower_half = sorted(lower_half, key=lambda x: x[1][0])

        # Kết hợp lại hai danh sách đã sắp xếp
        sorted_objects = sorted_upper_half + sorted_lower_half

        # In ra danh sách các đối tượng đã sắp xếp
        print("In ra box")
        for obj in sorted_objects:
            if obj[0] == 'box':
                print("Khung biển số [", obj[0], "] mang tọa độ tại:", obj[1])
        print("\n")

        # In ra danh sách các đối tượng đã sắp xếp
        print("Danh sách các ký tự đã sắp xếp:")
        for obj in sorted_objects:
            if obj[0] != 'box':
                print(obj[0], "tại tọa độ:", obj[1])

        # Ghi kết quả vào tệp tin
        file_name = "F:/Data_TT/BienSo.txt"
        with open(file_name, "w") as file:
            for obj in sorted_objects:
                if obj[0] != 'box':
                    file.write(obj[0] + ' ')
        print("\nĐã lưu trữ vào tệp tin '{}'.".format(file_name))

        # Hiển thị và lưu ảnh dự đoán
        results[0].save('F:/Data_TT/KQ')

        # Chuyển ảnh đã xử lý về dạng base64
        image_pil = Image.fromarray(image_np)
        draw = ImageDraw.Draw(image_pil)
        for obj, (x1, y1, x2, y2) in detected_objects:
            confidence = 0  # Bạn có thể cập nhật confidence nếu cần thiết
            if obj == 'box':
                draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
                draw.text((x1, y1), f"{obj} {confidence:.2f}", fill="red")
            else:
                draw.rectangle([(x1, y1), (x2, y2)], outline="green", width=3)
                draw.text((x1, y1), f"{obj} {confidence:.2f}", fill="green")

        encoded_image = encode_image(image_pil)
        return jsonify({'detections': detected_objects, 'image': encoded_image})
    else:
        return jsonify({'detections': [], 'image': None})
=======
            if cls == 31:
                detected_objects.append((name, (x1, y1, x2, y2)))
                cropped_image = image.crop((x1, y1, x2, y2))
                cropped_image = np.array(cropped_image)
                ocr_result = reader.readtext(cropped_image)
    process_results_time = time.time() - start_time

    # Tổng thời gian xử lý
    total_time = decode_time + save_time + open_time + predict_time + process_results_time



# Trong hàm detect()
    filtered_ocr_result = filter_ocr_result(ocr_result)
    combined_ocr_result = ''.join(filtered_ocr_result)


    response = {
        "detected_objects": detected_objects,
        # "ocr_result": [detection[1] for detection in ocr_result],
        "ocr_result": combined_ocr_result,
        "timing": {
            "decode_time": decode_time,
            "save_time": save_time,
            "open_time": open_time,
            "predict_time": predict_time,
            "process_results_time": process_results_time,
            "total_time": total_time
        }
    }

    return jsonify(response)
>>>>>>> Stashed changes
