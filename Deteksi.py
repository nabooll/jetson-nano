from ultralytics import YOLO
import cv2
import torch

# Load model YOLOv8 hasil training
model = YOLO('runs/detect/train/weights/best.pt')

# Buka kamera (0 untuk webcam internal, 1/2 untuk webcam eksternal)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Kamera tidak ditemukan.")
    exit()

print("✅ Kamera aktif. Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    # Deteksi objek dengan confidence threshold 0.5
    results = model(frame, conf=0.5)

    if len(results[0].boxes) > 0:
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

    # Tampilkan hasil
    cv2.imshow("Deteksi Karang Gigi (Hanya 1 Objek)", annotated_frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan window
cap.release()
cv2.destroyAllWindows()
