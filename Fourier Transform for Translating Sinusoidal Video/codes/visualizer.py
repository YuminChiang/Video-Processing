import cv2
import numpy as np
from camera import *

def visualize_spatial_temporal_signal(filename, signal, width, height, fps, intv):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    image = np.zeros([height, width, 3], dtype = np.uint8)

    # Frame index of viz.
    f_viz = 0 
    frames = signal.shape[2]
    for f in range(frames):
        for y in range(height):
            if y % intv == 0:
                # Get corrsponding y in signal
                resized_y = y // intv 
                for x in range(width):
                    if x % intv == 0:
                        # Get corresponding x in signal
                        resized_x = x // intv 
                        
                        # Get corresponding signal
                        b = signal[resized_y, resized_x, f]

                        # Dump to signal if current frame is filled.
                        if (f > f_viz):
                            video.write(image)  
                            f_viz += 1

                        # Normalization
                        b_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

                        # Draw response with thickness as the specified interval
                        image[y:y+intv, x:x+intv, :] = int(b_viz * 255) # Mapping to integer
    video.release()

def visualize_viewed_signal(filename, signal, width, height, fps, intv, w_mm, h_mm, d_mm):
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    image = np.zeros([height, width, 3], dtype = np.uint8)

    # Create camera for simulating the viewer
    fov = 60
    viewer = Camera(fov, width, height, fps) #Treat a viewer with camera
    
    # Frame index of viz
    f_viz = 0
    frames = signal.shape[2]
    for f in range(frames):
        for y in range(height):
            if y % intv == 0:
                # Get corresponding y 
                resized_y = y // intv
                for x in range(width):
                    if x % intv == 0: 
                        # Get corresponding x
                        resized_x = x // intv
                        
                        # Get corresponding signal
                        b = signal[resized_y, resized_x, f]

                        # Initialization for the projected position
                        c = x
                        r = y 

                        # TODO #5: Update projected position on the viewer

                        # Dump to signal if current frame is filled. 
                        if (f > f_viz):
                            video.write(image)
                            f_viz += 1

                        # Normalization
                        b_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

                        # Draw response with thickness as the specified interval
                        if r > 0 and r < height - intv and c > 0 and c < width - intv:
                            image[r:r+intv, c:c+intv, :] = int(b_viz * 255) # Mapping to integer
    video.release()

def compute_response_magnitudes(frequency_signal):
    height, width, frames = frequency_signal.shape[0], frequency_signal.shape[1], frequency_signal.shape[2]
    magnitudes = np.zeros([height, width, frames], dtype=float)
    # Compute the magnitude on each 3D coordinate and the max/min values.
    for ft in range(frames):
        for fy in range(height):
            for fx in range(width):
                response_real = frequency_signal.real[fy, fx, ft]
                response_imag = frequency_signal.imag[fy, fx, ft]
                magnitudes[fy, fx, ft] = np.sqrt(np.pow(response_real, 2) + np.pow(response_imag, 2)) 
    min_mag, max_mag = np.min(magnitudes), np.max(magnitudes)
    return magnitudes, min_mag, max_mag

def visualize_frequency_signal(filename, signal, width, height, fps, intv):
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    image = np.zeros([height, width, 3], dtype=np.uint8)

    # Viz the magnitude
    magnitudes, min_mag, max_mag = compute_response_magnitudes(signal)
    
    # Frame index for viz.
    f_viz = 0
    resized_height, resized_width, frames = signal.shape[0], signal.shape[1], signal.shape[2]
    for f in range(frames):
        for y in range(height):
            if y % intv == 0:
                # Get corresponding y in signal
                resized_y = y // intv
                for x in range(width):
                    if x % intv == 0:
                        # Get corresponding x in signal
                        resized_x = x // intv

                        # Get corresponding signal magnitude
                        mag = magnitudes[resized_y, resized_x, f]

                        # Dump to signal if current frame is filled. 
                        if (f > f_viz):
                            video.write(image)
                            f_viz += 1

                        # Normalization
                        if (max_mag == min_mag):
                            mag_viz = 0
                        else:
                            mag_viz = (mag - min_mag) / (max_mag - min_mag) # Mapping the value from (min_mag, max_mag) to (0, 1)

                        # Draw response with thickness as the specified interval
                        image[y:y+intv, x:x+intv, :] = int(mag_viz * 255) # Mapping to integer

                        # Dump image for better viewing
                        image_filename = f'results/frame-{f}.png'
                        cv2.imwrite(image_filename, image)

    video.release()

def visualize_recovered_signal(filename, signal, width, height, fps, intv):
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    image = np.zeros([height, width, 3], dtype = np.uint8)

    # Frame index for viz.
    f_viz = 0
    frames = signal.shape[2]
    for f in range(frames):
        for y in range(height):
            if y % intv == 0:
                # Get corresponding y in signal
                resized_y = y // intv
                for x in range(width):
                    if x % intv == 0:
                        # Get corresponding x in signal
                        resized_x = x // intv

                        # Get real-part of the corresponding signal
                        b = signal.real[resized_y, resized_x, f]

                        # Clamping the signal to (-1, 1) to remove the computing error
                        b = max(-1, min(b, 1))
                        
                        # Dump to signal if current frame is filled.
                        if (f > f_viz):
                            video.write(image)  
                            f_viz += 1

                        # Normalization
                        b_viz = (b + 1) / 2 # Mapping the value from (-1, 1) to (0, 1)

                        # Draw response with thickness as the specified interval
                        image[y:y+intv, x:x+intv, :] = int(b_viz * 255) # Mapping to integer
    video.release()
