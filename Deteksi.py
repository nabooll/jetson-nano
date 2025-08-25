from ultralytics import YOLO
import cv2
import torch
import Jetson.GPIO as GPIO
import time

# Gunakan mode pin BOARD (nomor fisik)
GPIO.setmode(GPIO.BOARD)

# Tentukan pin untuk Relay
relay1_pin = 11  # Pin fisik 11 (BCM 17)
relay2_pin = 13  # Pin fisik 13 (BCM 27)

# Set pin sebagai output
GPIO.setup(relay1_pin, GPIO.OUT)
GPIO.setup(relay2_pin, GPIO.OUT)

# Awal relay mati (HIGH untuk relay aktif LOW, sesuaikan dengan tipe relay)
GPIO.output(relay1_pin, GPIO.HIGH)
GPIO.output(relay2_pin, GPIO.HIGH)

# Load model YOLOv8 hasil training
model = YOLO('runs/detect/train/weights/best.pt')


# Buka kamera (0 untuk webcam internal, 1/2 untuk webcam eksternal)
cap = cv2.VideoCapture(0)

# Set resolusi kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ Kamera tidak ditemukan.")
    exit()

print("✅ Kamera aktif. Tekan 'q' untuk keluar.")

frame_count = 0
results = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    # Deteksi objek dengan confidence threshold 0.5
    results = model(frame, conf=0.5)

    if len(results[0].boxes) > 0:
        # Ada objek terdeteksi → relay ON (LOW jika relay aktif low)
        GPIO.output(relay1_pin, GPIO.LOW)
        GPIO.output(relay2_pin, GPIO.LOW)

        # Ambil box dengan confidence tertinggi
        best_box = results[0].boxes[results[0].boxes.conf.argmax()]

        # Buat frame kosong dulu
        annotated_frame = frame.copy()

        # Ambil koordinat bounding box
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])
        conf = float(best_box.conf[0])
        cls = int(best_box.cls[0])
        label = f"{model.names[cls]} {conf:.2f}"

        # Gambar bounding box
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    else:
        annotated_frame = frame
        # Tidak ada objek → relay OFF
        GPIO.output(relay1_pin, GPIO.HIGH)
        GPIO.output(relay2_pin, GPIO.HIGH)

    # Tampilkan hasil
    cv2.imshow("Deteksi Karang Gigi (Hanya 1 Objek)", annotated_frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resource
GPIO.cleanup()

# Tutup kamera dan window
cap.release()
cv2.destroyAllWindows()
