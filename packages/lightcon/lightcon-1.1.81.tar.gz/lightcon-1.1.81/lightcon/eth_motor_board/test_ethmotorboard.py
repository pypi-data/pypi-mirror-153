
# Load from Python path
# from lightcon.eth_motor_board import EthMotorBoard

# Load from working dir
from eth_motor_board import EthMotorBoard

print("=== EthMotorBoard test ===")

motorb = EthMotorBoard()

MOTOR_IDX = 0

if motorb.connected:
    print("Resetting...")
    motorb.reset_motor(MOTOR_IDX)

    print("Position before: " + motorb.get_abs_pos(MOTOR_IDX))

    print("Moving 1000 steps forward...")
    motorb.move_rel(MOTOR_IDX, 1, 1000)
    motorb.wait_until_stopped(MOTOR_IDX)

    print("Position after: " + motorb.get_abs_pos(MOTOR_IDX))
