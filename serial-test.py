import serial
import time

def find_correct_baudrate():
    baud_rates = [9600, 19200, 38400, 57600, 115200, 230400]
    
    for baud in baud_rates:
        try:
            print(f"Testing baud rate: {baud}")
            with serial.Serial('/dev/ttyTHS1', baud, timeout=1) as ser:
                ser.write(b"TEST\n")
                time.sleep(0.5)
                if ser.in_waiting > 0:
                    response = ser.read_all()
                    if response and b"TEST" in response or len(response) > 0:
                        print(f"Possible match at {baud}: {response}")
                        return baud
        except Exception as e:
            print(f"Error at {baud}: {e}")
    
    return None

# Cari baud rate yang benar
correct_baud = find_correct_baudrate() or 115200
print(f"Using baud rate: {correct_baud}")

# Lanjutkan dengan baud rate yang ditemukan
ser = serial.Serial(
    port='/dev/ttyTHS1',
    baudrate=correct_baud,
    timeout=1
)

angka = 0
try:
    while True:
        # Send as simple string
        data_to_send = f"{angka}\n"
        print(f"Sending: {data_to_send.strip()}")
        ser.write(data_to_send.encode())
        
        time.sleep(0.5)  # Beri waktu lebih untuk respons
        
        # Baca semua data yang available
        if ser.in_waiting > 0:
            try:
                # Baca sebagai raw bytes dulu
                raw_data = ser.read_all()
                print(f"Raw response: {raw_data}")
                print(f"Hex response: {raw_data.hex()}")
                
                # Coba decode sebagai string
                try:
                    decoded = raw_data.decode('utf-8').strip()
                    print(f"Decoded: {decoded}")
                except:
                    print("Cannot decode as UTF-8, treating as binary")
                    
            except Exception as e:
                print(f"Read error: {e}")
        else:
            print("No response from Wemos")
        
        angka += 10
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting")
finally:
    ser.close()
