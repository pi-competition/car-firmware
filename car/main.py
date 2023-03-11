import math
from gpiozero import CamJamKitRobot

target_x = None
target_y = None
self_x = None
self_y = None
self_angle = None

ctrl = CamJamKitRobot()

# TODO: TUNE
max_curve_angle = 45
speed = 1

# ctrl.forward()

def updateSelfPos(x, y, angle):
    self_x = x
    self_y = y
    self_angle = angle

def updateTargetPos(x, y):
    target_x = x
    target_y = y

def updateSpeed(speed_):
    speed = speed_

def drive(angle):
    curve_left = 0
    curve_right = 0
    if angle < 0: curve_left = abs(angle)/max_curve_angle
    elif angle > 0: curve_right = angle/max_curve_angle
    ctrl.forward(speed=speed, curve_left=curve_left, curve_right=curve_right)

def angle_correction():
    dx = target_x - self_x
    if dx == 0: dx = 0.0001
    dy = target_y - self_y
    # pronounced they-ta
    theta = math.atan(dy/dx)
    # now, compensate into a bearing
    if dx < 0:
        # negi, we work off 3/2 pi (270)
        # and then add mafs
        theta = (3/2) * math.pi  - theta
    else:
        theta = (1/2) * math.pi - theta

    # okay now do we turn left or right
    if self_angle == theta: return 0

    # turning left is as such:
    turning_left = self_angle - theta
    turning_left += 2*math.pi
    turning_left %= 2*math.pi

    turning_right = theta - self_angle
    turning_right += 2*math.pi
    turning_right %= 2*math.pi

    if turning_left < turning_right:
        return -turning_left
    else:
        return turning_right

def main():
    drive(angle_correction())
