import gamepads

if __name__ == '__main__':
    shanwan_gamepad = gamepads.ShanWanGamepad()

    while True:
        gamepad_input = shanwan_gamepad.read_data()
        stick_right_y = gamepad_input.analog_stick_right.y
        stick_left_x = gamepad_input.analog_stick_left.x
        print(f'stick_right_y={stick_right_y}, stick_left_x={stick_left_x}')