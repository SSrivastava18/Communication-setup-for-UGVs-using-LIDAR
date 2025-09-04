LiDAR-Comms

A proof-of-concept communication system using a TFMini Plus LiDAR sensor to transmit and receive digital messages as binary pulses.

This project demonstrates how LiDAR can be repurposed for short-range data communication by encoding messages into pulses (object present = 1, object absent = 0) and decoding them back into text.


🚀 Features

Transmit ASCII messages over LiDAR pulses.

Start/Stop markers for reliable synchronization.

Checksum verification for error detection.

Transmission and reception logs in CSV format.

Configurable bit duration and distance threshold.


🛠 Hardware Requirements

TFMini Plus LiDAR Sensor (UART mode).

USB-to-UART adapter (CP2102 / FTDI).

Optional: two LiDARs (one as transmitter, one as receiver).

If using only one LiDAR, transmitter side simulates pulses by manually blocking/unblocking.


⚙️ Setup

1.Clone the repository:

git clone https://github.com/SSrivastava18/Communication-setup-for-UGVs-using-LIDAR.git

cd LiDAR-Comms

2.Install dependencies:

pip install pyserial


📡 Usage

Transmitter

Encodes and transmits a text message as LiDAR pulses.

Default message = "HELP".

python transmitter.py

Converts message into binary.

Adds <START> and <END> markers + checksum.

Sends pulses (1 = object close / 0 = object far).

Logs all transmitted bits to transmission_log.csv.

Receiver

Reads pulses from LiDAR and decodes them into text.

python receiver.py

Reads distance frames continuously.

Detects 1 (pulse) if distance ≤ 50cm, else 0.

Reconstructs binary into ASCII.

Looks for <START> … <END> markers.

Validates checksum.

Saves logs to reception_log.csv.


🔧 Configuration

Bit Duration (bit_duration)

Default = 0.2s. Must be the same in transmitter and receiver.

Pulse Threshold (pulse_threshold)

Default = 50cm. Adjust based on environment.

Message

In transmitter.py, change:

message = "HELP"


📜 License

MIT License © 2025 Saurabh Srivastava


