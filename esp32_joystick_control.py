import serial
import pyautogui
import time

# Replace 'COMX' with the appropriate COM port for your ESP32
ser = serial.Serial('COMX', 115200, timeout=1)

print("ESP32-Joystick Mouse Control (with X and Y)")
pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

# Low-pass filter constants
alpha = 0.2  # Adjust this value for desired smoothing (0.0 to 1.0)

x_smoothed = 0
y_smoothed = 0

while True:
    t0 = time.time()


    serial_buffer = []
    got_start_packet = False

    t_read = time.time()

    while True:
        try:
            received_data = ser.read(1).decode()
        except UnicodeDecodeError:
            continue
        if received_data == "E" and got_start_packet:
            break
        if got_start_packet == True:
            serial_buffer.append(received_data)
        if received_data == "S":
            got_start_packet = True

    print("Packet read took:", (time.time() - t_read) * 1000)

    received_data = "".join(serial_buffer)
    if received_data:
        print("Received:", received_data)

        # Split the received data by the comma
        values = received_data.split(',')

        if len(values) == 2:
            try:
                x = int(values[0])
                y = int(values[1])

                if 1880 < x < 1920:
                    print("Deadzone x")
                    # x = 2047 #actual middle on my joystick (without stick drift)
                    x = 1800  # real middle on my joystick (with stick drift)
                if 1840 < y < 1880:
                    print("Deadzone y")
                    # y = 2047 #actual middle on my joystick (without stick drift)
                    y = 1800  # real middle on my joystick (with stick drift)

                # Apply the low-pass filter
                x_smoothed = (alpha * x) + ((1 - alpha) * x_smoothed)
                y_smoothed = (alpha * y) + ((1 - alpha) * y_smoothed)

                target_x = int(x_smoothed * (screen_width / 3650))  # Adjust the scaling factor as needed, should be 2x middle of the joystick
                target_y = int(y_smoothed * (screen_height / 3500))  # Adjust the scaling factor as needed, should be 2x middle of the joystick

                pyautogui.moveTo(target_x, target_y)

            except ValueError:
                print("Invalid data format. Skipping.")
        else:
            print("Invalid data format. Skipping.")
    print("Time took:", (time.time() - t0) * 1000)
