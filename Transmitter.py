# transmitter.py
import time
import serial
import csv

# Open serial connection to TFMini Plus
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

# Transmission settings
bit_duration = 0.2   # seconds per bit
close_cmd = b'\x5A\x05\x05\x06'  # Placeholder: simulate "pulse"
far_cmd   = b'\x5A\x05\x05\x07'  # Placeholder: simulate "pause"

# Utility: Convert string to binary
def string_to_binary(message):
    return ''.join(format(ord(c), '08b') for c in message)

# Add markers + checksum
def prepare_message(message):
    checksum = sum(ord(c) for c in message) % 256
    full_message = f"<START>{message}<END>{chr(checksum)}"
    return string_to_binary(full_message)

def send_bit(bit, log_data):
    timestamp = time.time()
    if bit == '1':
        ser.write(close_cmd)  # Send "pulse"
        log_data.append([bit, timestamp, "Pulse"])
        print(f"Pulse 1 at {timestamp}")
    else:
        ser.write(far_cmd)    # Send "pause"
        log_data.append([bit, timestamp, "Pause"])
        print(f"Pause 0 at {timestamp}")
    time.sleep(bit_duration)

def transmit(binary_string):
    log_data = []
    print("Sending message:", binary_string)
    for bit in binary_string:
        send_bit(bit, log_data)
    return log_data

if __name__ == "__main__":
    try:
        message = "HELP"
        binary_message = prepare_message(message)

        log = transmit(binary_message)

        with open("transmission_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Bit Sent", "Timestamp", "Meaning"])
            writer.writerows(log)

        print("Transmission complete.")
    except KeyboardInterrupt:
        print("Transmission interrupted.")
    finally:
        ser.close()
