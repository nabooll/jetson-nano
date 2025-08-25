import Jetson.GPIO as GPIO
import time

# Gunakan mode pin BCM (nomor pin sesuai Broadcom SOC)
GPIO.setmode(GPIO.BOARD)

# Tentukan pin untuk Relay
relay1_pin = 11  # Ubah sesuai dengan pin yang kamu pakai
relay2_pin = 13  # Ubah sesuai dengan pin yang kamu pakai

# Set pin sebagai output
GPIO.setup(relay1_pin, GPIO.OUT)
GPIO.setup(relay2_pin, GPIO.OUT)

print("=== Kontrol Relay 2 Channel ===")
print("Ketik 'Y' untuk menyalakan relay, 'N' untuk mematikan relay, atau 'Q' untuk keluar.")

try:
    while True:
        command = input("Perintah (Y/N/Q): ").strip().upper()

        if command == 'Y':
            GPIO.output(relay1_pin, GPIO.HIGH)  # Relay aktif (tergantung tipe relay, HIGH/LOW bisa terbalik)
            GPIO.output(relay2_pin, GPIO.HIGH)
            print("Relay 1 & 2 AKTIF.")

        elif command == 'N':
            GPIO.output(relay1_pin, GPIO.LOW)
            GPIO.output(relay2_pin, GPIO.LOW)
            print("Relay 1 & 2 MATI.")

        elif command == 'Q':
            print("Keluar program...")
            break

        else:
            print("Perintah tidak dikenali. Gunakan Y/N/Q.")

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh user.")

finally:
    GPIO.cleanup()
    print("GPIO dibersihkan.")
