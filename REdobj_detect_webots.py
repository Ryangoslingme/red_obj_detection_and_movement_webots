import cv2
from controller import Robot
import numpy as np

# Initialize robot
robot = Robot()
TIMESTEP = int(robot.getBasicTimeStep())
MAX_SPEED = 6.28

# 1. Initialize Camera
camera = robot.getDevice('camera')
camera.enable(TIMESTEP)
width = camera.getWidth()
height = camera.getHeight()

# 2. Initialize Motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

print('Camera and motors initialized. Starting color tracking...', flush=True)

# Main simulation loop
while robot.step(TIMESTEP) != -1:
  # Capture image from Webots camera
  image = camera.getImage()
  if image is None:
    continue

  # Convert Webots raw image buffer into OpenCV format (BGRA to BGR)
  frame = np.frombuffer(image, np.uint8).reshape((height, width, 4))
  bgr_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

  # Convert BGR to HSV color space (ideal for color tracking)
  hsv = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)

  # Define threshold ranges for RED color in HSV
  lower_red1 = np.array([0, 120, 70])
  upper_red1 = np.array([10, 255, 255])
  lower_red2 = np.array([170, 120, 70])
  upper_red2 = np.array([180, 255, 255])

  # Combine masks to catch all shades of red
  mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
  mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
  mask = mask1 + mask2

  # Calculate image moments to locate the center of the red rectangle
  m = cv2.moments(mask)

  if m['m00'] > 300:  # If a red object is detected in frame
    # X-coordinate of the object center
    cx = int(m['m10'] / m['m00'])

    # Distance from center of image frame
    image_center = width / 2
    error = cx - image_center

    # Proportional turning speed
    turn_correction = 0.005 * error

    if abs(error) < 10:
      # Object is centered: drive straight toward it
      left_speed = 0.5 * MAX_SPEED
      right_speed = 0.5 * MAX_SPEED
      print('TARGET CENTERED -> Moving Forward', flush=True)

    elif error > 0:
      # Object is to the right: turn right
      left_speed = 0.4 * MAX_SPEED
      right_speed = (0.4 - turn_correction) * MAX_SPEED
      print('TARGET ON RIGHT -> Turning Right', flush=True)

    else:
      # Object is to the left: turn left
      left_speed = (0.4 + turn_correction) * MAX_SPEED
      right_speed = 0.4 * MAX_SPEED
      print('TARGET ON LEFT -> Turning Left', flush=True)

  else:
    # No red object seen: spin in place to search for it
    left_speed = 0.2 * MAX_SPEED
    right_speed = -0.2 * MAX_SPEED
    print('SEARCHING FOR RED RECTANGLE...', flush=True)

  # Apply motor velocities
  left_motor.setVelocity(left_speed)
  right_motor.setVelocity(right_speed)
