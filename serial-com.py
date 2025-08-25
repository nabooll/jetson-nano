import serial
import time
angka = 0
# Configure the serial port
# For Jetson Nano, the UART port is typically /dev/ttyTHS1
# Verify the port name if issues arise
# Baud rate should match the Wemos's configured baud rate
ser = serial.Serial(
    port='/dev/ttyTHS1',  # Adjust this if your port is different
    baudrate=115200,      # Match this to your Wemos's baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             # Timeout in seconds
)

try:
    while True:
        data_to_send = str(angka)+"\n"
        print(f"Sending: {data_to_send.strip()}")
        ser.write(data_to_send.strip().encode('utf-8')) # Encode string to bytes

        # Optional: Read response from Wemos
        if ser.in_waiting > 0:
            received_data  = ser.read_until('\n').decode('utf-8', errors='ignore')
            print(f"Received from Wemos: {received_data}")
        angka+=10
        time.sleep(5) # Wait for 2 seconds before sending again

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    ser.close() # Close the serial port
    print("Serial port closed.")
