import math
import time
#import server.main
from gpiozero import CamJamKitRobot

target_x = None
target_y = None
self_x = None
self_y = None
self_angle = None

ctrl = CamJamKitRobot()

# TODO: TUNE
max_curve_angle = math.pi / 2
speed = 0.7

# ctrl.forward()

def updateSelfPos(x, y, angle):
    print("updateSelfPos")
    # print(x, y, angle)
    global self_x
    global self_y
    global self_angle
    self_x = x
    self_y = y
    self_angle = angle

def updateTargetPos(x, y):
    print("updateTargetPos")
    global target_x
    global target_y
    target_x = x
    target_y = y

def updateSpeed(speed_):
    speed = speed_

def stop():
    print("sropped")
    ctrl.stop()

def drive(angle):
    return None
    if angle is None: return None
    # do some wrangling
    # angle should be from -pi to pi
    angle += math.pi
    angle = angle % (2*math.pi)
    angle -= math.pi
    print(angle)
    curve_left = 0
    curve_right = 0
    if angle < 0: curve_left = min(1, abs(angle)/max_curve_angle)
    elif angle > 0: curve_right = min(1, angle/max_curve_angle)
    print(curve_left, curve_right)
    ctrl.forward(speed=speed, curve_left=curve_left, curve_right=curve_right)

def bearingBetween2Points(s_x, s_y, d_x, d_y):
    dx = d_x - s_x
    dy = d_y - s_y
    if dx == 0: dx = 0.001
    theta = math.atan(abs(dy/dx))
    if dx < 0:
        if dy < 0:
            return (3/2) * math.pi - theta
        else:
            return (3/2) * math.pi + theta
    else:
        if dy < 0:
            return (1/2) * math.pi + theta
        else:
            return (1/2) * math.pi - theta


def angle_correction():
    global self_angle
    if target_x is None: return None
    target_dir = bearingBetween2Points(self_x, self_y, target_x, target_y)
    # target_dir += 2*math.pi
    # self_angle += 2*math.pi
    print(target_dir, self_angle)
    correction = target_dir - self_angle
    correction += 2*math.pi
    correction %= 2*math.pi

    if correction > math.pi:
        correction = -(2*math.pi - correction)

    print(correction)

    if (abs(correction) > math.pi * (1/4)):
        print("spinning since correction", correction)
        # more than 45deg, should prolly spin
        if correction < 0:
            ctrl.left()
        else:
            ctrl.right()
        return None
    """
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
    """
    
    scale = abs(correction) / (math.pi * (1/2))
    if scale > 1: scale = 1
    if correction < 0:
        ctrl.forward(speed=speed, curve_left = scale)
    else:
        ctrl.forward(speed=speed, curve_right = scale)

    return None

    if turning_left < turning_right:
        return -turning_left
    else:
        return turning_right


def main():
    drive(angle_correction())
