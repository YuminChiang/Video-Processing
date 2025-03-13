# This class provides utility functions for generating standard 3D sinusoidal patterns 
import numpy as np

class SinusoidalPatternGenerator():
    '''
    Inputs:
        w_mm: plane width in milli meters
        h_mm: plane height in milli meters
        width: number of pixels on the horizontal direction
        height: number of pixels on the vertical direction
        Tb: Beginning of the time
        Te: End of the time
    '''
    def __init__(self, w_mm, h_mm, width, height, Tb, Te):
        self.w_mm = w_mm
        self.h_mm = h_mm
        self.width = width
        self.height = height
        self.Te = Te
        self.Tb = Tb

    '''
    Inputs:
        fx: frequency on horizontal direction in cycles per mm
        fy: frequency on vertical direction in cycles per mm
        ft: frequency on temporal direction in frames per sec
        vx: velocity along horizontal direction in mm/sec
        vy: velocity along vertical direction in mm/sec
        intv: Interval for downsampling the frequency and spatial temporal variables
    Outputs:
        video: temporal spatial signal. A list of 4D vectors: [b, x, y, t], where x, y, t represents the temporal
        sample, and b represents the brightness (singal) on (x, y, t)
    '''
    def generate_moving_sinusoidals(self, fx, fy, ft, vx, vy, intv):
        # Set video dimension
        pix_per_mm = self.width / self.w_mm # Resolution

        # Build time sequence with the interval (Tb, Te, dt) 
        times = []
        dt = self.Te / ft
        t = self.Tb
        while t < self.Te:
            times.append(t)
            t += dt

        # Pre-compute video samples based on the interval
        frames = len(times)
        resized_height = (self.height - 1) // intv + 1
        resized_width = (self.width - 1) // intv + 1
        video = np.zeros([resized_height, resized_width, frames])
        for f in range(frames): # Frame
            for y in range(self.height):
                if y % intv == 0: # Downsampling for reducing the computing
                    for x in range(self.width):
                        if x % intv == 0: # Downsampling for reducing the computing
                            # Compute input signal value as the brightness according to the specified sin pattern
                            x_mm = x / pix_per_mm # In mm
                            y_mm = y / pix_per_mm # In mm
                            t = times[f]
                            dx = vx * t
                            dy = vy * t
                            b = np.sin(fx * 2 * np.pi * (x_mm + dx) + fy * 2 * np.pi * (y_mm + dy)) # Should located in (-1, 1)
                            resized_y = y // intv
                            resized_x = x // intv
                            video[resized_y, resized_x, f] = b
 
        return video
