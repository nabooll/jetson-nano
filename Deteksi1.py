from ultralytics import YOLO
import cv2

# Load model YOLOv8 hasil training
model = YOLO('runs/detect/train/weights/best.pt')

# Load gambar karang gigi
image_path = 'test.jpg'  # Ganti dengan nama file gambar kamu
frame = cv2.imread(image_path)

# Cek apakah gambar berhasil dibuka
if frame is None:
    print("Gagal membuka gambar.")
    exit()

# Deteksi objek pada gambar
results = model(frame)

# Gambar hasil deteksi (bounding box, label, dll.)
annotated_frame = results[0].plot()

# Tampilkan hasil deteksi
cv2.imshow("Deteksi Karang Gigi", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
