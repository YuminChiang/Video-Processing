from human_visual_system import *
import numpy as np

class Camera():
    def __init__(self, fov, image_width, image_height, frames_per_second=30):
        # Projection matrix
        F = fov * np.pi / 180 
        w, h = image_width, image_height
        f = h / (2 * (np.tan(F / 2))) #Focal length
        self.P = np.array([[f, 0, w / 2],
                           [0, f, h / 2],
                           [0, 0, 1]])
        # Store focal length
        self.focal = f

        # Exposed image: # stored exposure information, value: 0 - 1
        self.exposed_image = np.zeros([h, w, 3]) 

        # Scanned image: raster scanning on the latent image
        self.scanned_image = np.zeros([h, w, 3])

        # Output attenuation image: raster scanning on the latent image
        self.attenuation_image = np.zeros([h, w, 3])

        # Store image size
        self.w = w
        self.h = h
        
        # Gamman correction parameters
        self.gc = 1.7

        # Record specified frame per second.
        self.fps = frames_per_second

        # Compute line rate and intervals according to fps and fsy
        # Line rate (lines per second) = fps * self.h (lines per frame)
        self.compute_line_rate()

        # Line interval = 1 / (line rate)
        self.compute_line_interval_ms()

        # Specify horizontal retrace time and vertical retrace time
        # Horizontal retrace time should not larger than line interval
        self.horizontal_retrace_time = 0.01 * self.line_interval

        # Set vertical retrace time in ms
        self.vertical_retrace_time = 0.05

        # Compute real scanning time and scanned lines in a frame
        self.compute_line_scanning_time()

        # Compute scanning time per raster
        self.compute_pixel_interval()

        # Scanned raster index
        self.scan_index = 0
        self.elapsed_time_ms_scan = 0
        self.scanned_lines = 0
        self.completed = False

    def compute_line_rate(self):
        # self.h denotes lines per frame
        self.line_rate =  self.fps * self.h

    def compute_line_interval_ms(self):
        sec2ms = 1000
        self.line_interval = sec2ms / self.line_rate

    def compute_line_scanning_time(self):
        self.line_scanning_time = self.line_interval - self.horizontal_retrace_time
    
    def compute_pixel_interval(self):
        self.pixel_interval = self.line_interval / self.w

    def get_focal_length(self):
        return self.focal
    def get_line_interval(self):
        return self.line_interval

    def get_raster_scanning_time(self):
        return self.pixel_interval

    def get_scan_index(self):
        return self.scan_index

    def expose(self, lights):
        # Assume the exposure is simultaneously on an area and the exposure time is 0
        # Here we use previous sharpe model for HVS as the camera sensor exposure model
        hvs = HumanVisualSystem()
        for light in lights: 
            r = g = b = 0 # Initialize r, g, b to zeros
            y = u = v = 0 # Initialize y, u, v to zeros

            # Get receptor responses
            r = hvs.red_cone_response(light)
            g = hvs.green_cone_response(light)
            b = hvs.blue_cone_response(light)

            # Capture lights in camera
            x = self.project_to_image_position(light.X)
            self.write_exposed_image(x, r, g, b)

    def raster_scan(self, delta_time_ms):
        # Line interval = self.pixel_interval * self.w  + self.horizontal_retrace_time
        t0 = self.elapsed_time_ms_scan
        t1 = self.elapsed_time_ms_scan + delta_time_ms
        sec2ms = 1000
        T_frame_ms = sec2ms / self.fps 
        l = self.scanned_lines

        if t1 <= T_frame_ms - self.vertical_retrace_time: # Before vertical retracing
           # Determine the elapsed time after horizontally retracing on current line
           t_line = t1 - l * self.line_interval
           if t_line <= self.line_scanning_time:
               # Line scanning
               scan_idx_next = (int) (t_line / self.pixel_interval)
               scan_idx_prev = self.scan_index - self.scanned_lines * self.w
               # The scanning is during horizontal retracing if next scan idx > self.w - 1
               for _ in range(scan_idx_prev, min(scan_idx_next, self.w)):
                   self.raster_scan_one_pixel()
           elif t_line <= self.line_interval: # Re-tracingg
               pass
           else:
               self.scanned_lines += 1
               self.scan_index = self.scanned_lines * self.w

           # Update elapsed time 
           self.elapsed_time_ms_scan = t1
        elif t1 <= T_frame_ms: # During vertical retracing
           # Update elapsed time 
           self.elapsed_time_ms_scan = t1
        else: # Finish vertical retracing
           self.completed = True
           self.elapsed_time_ms_scan = 0

    def raster_scan_one_pixel(self):
        # Recover image coordinate from raster index. 
        # Let (x[0], x[1]) denote the image coordinate, then r_idx = x[1] * w + x[0].
        x = [0, 0]
        x[1] = int(self.scan_index / self.w)
        x[0] = self.scan_index - x[1] * self.w

        # Record current target raster, after scanning it, the target raster is moved.
        r, g, b = self.exposed_image[x[1], x[0], :]
        self.write_scanned_image(x, r, g, b)

        # Increase scan index
        self.scan_index += 1

    def restart_scanning_frame(self):
        self.scanned_image = np.zeros([self.h, self.w, 3])
        self.attenuation_image = np.zeros([self.h, self.w, 3])
        self.completed = False
        self.scan_index = 0
        self.scanned_lines = 0

    def frame_completed(self):
        # Indicate whether frame scanning is completed or not.
        return self.completed

    def project_to_image_position(self, X):
        X = np.array(X)
        x = self.P @ X
        x /= x[2]
        # Flip Y to fit image direction
        x[1] = self.h - x[1] 
        # Floor to get integer position
        return x[:2].astype(int)

    def write_exposed_image(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.exposed_image[x[1], x[0], :] = [r, g, b]

    def write_scanned_image(self, x, r, g, b):
        if (x[1] >= 0 and x[1] < self.h and x[0] >= 0 and x[0] < self.w):
            self.scanned_image[x[1], x[0], :] = [r, g, b]

    def output_scanned_image(self):
        # Return scanned image 
        return self.scanned_image

    def output_attenuation_image(self):
        # Simulate camera output voltages to the display. 
        # Assuming the scanned image accurately stores brightness information, the output voltages to the display represent an image that distorts the scanned image.
        self.attenuation_image = np.zeros([self.h, self.w, 3])
        for y in range(self.h):
            for x in range(self.w):
                for idx, Bc in enumerate(self.scanned_image[y, x]):
                    self.attenuation_image[y, x, idx] = self.get_output_voltage(Bc)
        return self.attenuation_image

    # Used for quick viz. of scanning observation
    def output_attenuation_image_scanned(self, scan_idx_prev, scan_idx_next):
        for idx in range(scan_idx_prev, scan_idx_next):
            y = int(idx / self.w)
            x = idx - y * self.w
            for idx, Bc in enumerate(self.scanned_image[y, x]):
                self.attenuation_image[y, x, idx] = self.get_output_voltage(Bc)
        return self.attenuation_image

    def get_output_voltage(self, Bc):
        # Simulate signal attenuation in relation to input brightness on the voltage.
        return np.power(Bc, 1 / self.gc)

    def get_gamma(self):
        return self.gc
