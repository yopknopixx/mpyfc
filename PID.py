import time

LOOP_TIME_SECONDS = 0.002


class PID_Controller:
    def __init__(self, max_output, min_output):
        # PID constant values need to be tuned for each setup
        self.kp = {
            "roll": 0.43714285,
            "pitch": 0.43714285,
            "yaw": 1.714287,
        }
        self.ki = {
            "roll": 0.255,
            "pitch": 0.255,
            "yaw": 0.3428571,
        }
        self.kd = {
            "roll": 0.01571429,
            "pitch": 0.01571429,
            "yaw": 0.00,
        }
        self.max_output = max_output
        self.min_output = min_output
        self.integral_roll = 0
        self.integral_pitch = 0
        self.integral_yaw = 0
        self.last_error = [0] * 3
        self.last_time = 0
        self.error_roll = 0
        self.error_pitch = 0
        self.error_yaw = 0
        self.max_integral = 150

    # property for roll pitch and yaw angles
    def get_state(self):
        return {
            "angles": [(x - 1500) / 16.666 for x in [self.roll, self.pitch, self.yaw]],
            "targets": [self.roll_target, self.pitch_target, self.yaw_target],
        }

    def set_state(self, angles, targets):
        # print(angles, targets)
        if targets[3] < 1200:
            self.reset_I()
        self.roll = angles["roll"] * 16.666 + 1500
        self.pitch = angles["pitch"] * 16.666 + 1500
        self.yaw = angles["yaw"] * 16.666 + 1500
        self.target_roll = targets[0]
        self.target_pitch = targets[1]
        self.target_yaw = targets[2]
        self.update()

    def calculate_errors(self):
        # calculate errors
        self.last_error = [self.error_roll, self.error_pitch, self.error_yaw]
        self.error_roll = self.roll - self.target_roll
        self.error_pitch = self.pitch - self.target_pitch
        self.error_yaw = self.yaw - self.target_yaw
        # print(self.error_roll, self.error_pitch, self.error_yaw)

    def update(self):
        # calculate errors
        self.calculate_errors()

        # calculate integral
        self.integral_roll += self.error_roll * LOOP_TIME_SECONDS
        self.integral_pitch += self.error_pitch * LOOP_TIME_SECONDS
        self.integral_yaw += self.error_yaw * LOOP_TIME_SECONDS

        # calculate derivative
        self.derivative_roll = (
            self.error_roll - self.last_error[0]
        ) / LOOP_TIME_SECONDS
        self.derivative_pitch = (
            self.error_pitch - self.last_error[1]
        ) / LOOP_TIME_SECONDS
        self.derivative_yaw = (self.error_yaw - self.last_error[2]) / LOOP_TIME_SECONDS

        # calculate output
        self.output_roll = (
            self.kp["roll"] * self.error_roll
            + self.ki["roll"]
            * max(min(self.integral_roll, self.max_integral), -self.max_integral)
            + self.kd["roll"] * self.derivative_roll
        )
        self.output_pitch = (
            self.kp["pitch"] * self.error_pitch
            + self.ki["pitch"]
            * max(min(self.integral_pitch, self.max_integral), -self.max_integral)
            + self.kd["pitch"] * self.derivative_pitch
        )
        self.output_yaw = (
            self.kp["yaw"] * self.error_yaw
            + self.ki["yaw"]
            * max(min(self.integral_yaw, self.max_integral), -self.max_integral)
            + self.kd["yaw"] * self.derivative_yaw
        )

        # limit output
        self.output_roll = min(max(self.min_output, self.output_roll), self.max_output)
        self.output_pitch = min(
            max(self.min_output, self.output_pitch), self.max_output
        )
        self.output_yaw = min(max(self.min_output, self.output_yaw), self.max_output)

        # save last error
        self.last_error = [self.error_roll, self.error_pitch, self.error_yaw]

    def reset_I(self):
        self.integral_roll = 0
        self.integral_pitch = 0
        self.integral_yaw = 0

    @property
    def outputs(self):
        return [self.output_roll, self.output_pitch, self.output_yaw]

    @property
    def errors(self):
        return [self.error_roll, self.error_pitch, self.error_yaw]
