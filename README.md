# E-puck Color Tracking Robot — Webots + OpenCV

## Overview

This project implements a camera-based color-tracking robot using the e-puck robot in Webots. The robot detects a red object in its camera image and adjusts its wheel speeds to steer toward the object.

The controller uses Python, OpenCV, and NumPy for image processing and Webots' controller API to control the robot.

## Objectives

- Capture images from the robot's onboard camera.
- Detect red-colored regions using HSV color thresholding.
- Estimate the horizontal position of the detected red region.
- Steer the robot toward the target using differential wheel speeds.
- Search for the target when it is not visible.

## Technologies Used

- **Simulator:** Webots
- **Programming language:** Python
- **Computer vision:** OpenCV
- **Numerical processing:** NumPy
- **Robot:** e-puck

## How It Works

1. **Image capture:** The e-puck camera provides an image during each simulation step.
2. **Image conversion:** The camera image is converted into a format that OpenCV can process.
3. **Color detection:** The image is converted from BGR to HSV color space. Two HSV ranges are used to detect red hues.
4. **Target localization:** A binary mask isolates red pixels, and image moments estimate their horizontal center.
5. **Steering:** The controller compares the target center with the image center and adjusts the left and right wheel speeds.
6. **Target search:** If no sufficient red signal is detected, the robot rotates in place to search for the target.

## Control Logic

| Target position | Robot response |
|---|---|
| Near the image center | Moves forward |
| Right of the image center | Turns right |
| Left of the image center | Turns left |
| No detectable red region | Rotates to search |

The current controller uses a proportional steering correction based on the horizontal image error.

## Requirements

- Webots installed
- Python interpreter compatible with the Webots controller environment
- OpenCV (`cv2`)
- NumPy

Install the Python dependencies using the interpreter configured for your Webots controller:

```bash
python -m pip install opencv-python numpy
```

If Webots uses a specific Python executable, run the command with that executable instead.

## Running the Simulation

1. Open the project world in Webots.
2. Confirm that the e-puck has an enabled camera and the expected wheel motors.
3. Assign `colour_detect` as the robot's controller.
4. Ensure OpenCV and NumPy are installed in the controller's Python environment.
5. Start the simulation.
6. Place a red target within the camera's field of view.
7. Observe the robot's steering response as the target moves across the image.
8. Move the target out of view and observe the search behavior.

## Testing and Evaluation

The controller should be tested under different target positions and visibility conditions.

Record the results in `results/test-results.md`, including:

- Test conditions
- Expected behavior
- Observed behavior
- Pass/fail status
- Notes or screenshots where useful

Do not report unrun tests as successful.

## Current Limitations

- Detection depends on lighting, target color, and the selected HSV thresholds.
- The controller estimates horizontal target position; it does not directly estimate distance.
- Multiple red regions may influence the calculated center because the current implementation processes the combined red mask.
- The robot may continue moving forward when the target is centered, so obstacle avoidance and collision prevention are not guaranteed.
- Performance may vary with target size, camera resolution, and scene conditions.

## Future Improvements

- Add a visual marker showing the detected target center.
- Tune HSV thresholds under different lighting conditions.
- Test multiple target sizes and distances.
- Use contour filtering to select one target instead of combining all red regions.
- Add distance estimation and a controlled stopping condition.
- Combine color tracking with obstacle avoidance.

## Project Status

**Status:** Basic red-object tracking implemented in Webots.

Testing results and performance claims should be updated as further experiments are completed.
