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

# === Muat model YOLOv8 hasil training ===
model = YOLO("runs/detect/train/weights/best.pt")

# Pindahkan model ke GPU kalau ada
if torch.cuda.is_available():
    model.to('cuda')
    print("✅ Menggunakan GPU untuk inferensi.")
else:
    print("⚠️ GPU tidak ditemukan, menggunakan CPU.")

# === Pilih sumber video ===
cam_index = 0
cap = cv2.VideoCapture(cam_index)

# Set resolusi kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ Kamera tidak ditemukan. Pastikan terhubung dengan benar.")
    exit()

frame_count = 0
results = None

# === Loop deteksi ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal membaca frame dari kamera.")
        break

    frame_count += 1

    # Deteksi setiap 3 frame
    if frame_count % 3 == 0:
        results = model(frame, conf=0.5)

    if results is not None and len(results[0].boxes) > 0:
        # Ada objek terdeteksi → relay ON (LOW jika relay aktif low)
        GPIO.output(relay1_pin, GPIO.LOW)
        GPIO.output(relay2_pin, GPIO.LOW)

        boxes = results[0].boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf:.2f}"

            # Gambar kotak merah
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        # Tidak ada objek → relay OFF
        GPIO.output(relay1_pin, GPIO.HIGH)
        GPIO.output(relay2_pin, GPIO.HIGH)

    # Tampilkan frame
    cv2.imshow("Deteksi Karang Gigi (Kotak Merah)", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resource
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
