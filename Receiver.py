# receiver.py
import time
import serial
import csv

# Open serial connection to TFMini Plus
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

pulse_threshold = 50   # cm
bit_duration = 0.2     # must match transmitter

def read_distance():
    data = ser.read(9)  # Read 9-byte frame
    if len(data) == 9 and data[0] == 0x59 and data[1] == 0x59:
        distance = data[2] + data[3] * 256
        return distance
    return None

def binary_to_string(binary_string):
    return ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))

def receive(num_bits=256):
    received_bits = []
    log_data = []
    print("Receiving...")

    while len(received_bits) < num_bits:
        dist = read_distance()
        timestamp = time.time()

        if dist is not None:
            if dist <= pulse_threshold:
                received_bits.append('1')
                log_data.append([timestamp, dist, 1])
                print(f"Pulse detected at {timestamp} (dist={dist})")
            else:
                received_bits.append('0')
                log_data.append([timestamp, dist, 0])
                print(f"No pulse at {timestamp} (dist={dist})")

        time.sleep(bit_duration)

    binary_string = ''.join(received_bits)
    decoded = binary_to_string(binary_string)

    # Extract message between markers
    if "<START>" in decoded and "<END>" in decoded:
        try:
            core = decoded.split("<START>")[1]
            msg, checksum_char = core.split("<END>")
            received_checksum = ord(checksum_char)
            calculated_checksum = sum(ord(c) for c in msg) % 256

            print("Decoded Message:", msg)
            if received_checksum == calculated_checksum:
                print("Checksum OK")
            else:
                print("❌ Checksum mismatch! Message may be corrupted.")
        except Exception as e:
            print("Error parsing message:", e)
    else:
        print("No valid start/stop markers found in decoded data.")

    with open("reception_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Measured Distance", "Decoded Bit"])
        writer.writerows(log_data)

    return decoded

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("Reception interrupted.")
    finally:
        ser.close()
