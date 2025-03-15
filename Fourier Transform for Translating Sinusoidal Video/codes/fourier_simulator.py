from sinusoidal_pattern_generator import *
from fourier_transformer import *
from visualizer import *
import os.path
import time

# Create output folder
folder_out = "results"
if not os.path.exists(folder_out):
    os.makedirs(folder_out)

# Cache signal
def cache_signal(filepath, signal):
    with open(filepath, 'w') as file:
        # Write each float number to the file
        height, width, frames = signal.real.shape[0], signal.real.shape[1], signal.real.shape[2]
        for fy in range(height):
            for fx in range(width):
                for ft in range(frames):
                    # Write order: response_real, response_imag, fx, fy, ft
                    response_real = signal.real[fy, fx, ft]
                    response_imag = signal.imag[fy, fx, ft]
                    file.write(f"{response_real} {response_imag} {fx} {fy} {ft}\n")

# Load cached signal
def load_signal(filepath, signal_shape):
    height, width, frames = signal_shape[0], signal_shape[1], signal_shape[2]
    signal = np.zeros([height, width, frames], dtype=complex)
    with open(filepath, 'r') as file:
        content = file.read()
        vals = content.split()
        while len(vals) > 0:
            # TODO #1: Implement the file loading to load the cached content into signal 
            fy = int(vals[3])
            fx = int(vals[2])
            ft = int(vals[4])
            response_real = float(vals[0])
            response_imag = float(vals[1])
            signal[fy,fx,ft] = complex(response_real,response_imag)
            vals = vals[5:]
    return signal

fx_vid = 0.5 # Cycles per mm along horizontal direction
fy_vid = 0.0 # Cycles per mm along vertical direction
vx_vid = 0.2 # Speed along horizontal direction mm/sec
vy_vid = 0.2 # Speed along vertical direction in mm/sec
Tb = 0 # Beginning of the time
dt = 1 # Frame time in seconds
Te = 30 # End of the time in seconds
fps = (Te - Tb) / dt

# Physical Length of the image plane
h_mm = 10
w_mm = 10
d_mm = 15

# Height, width, and interval in pixels
height = 100
width = 100
intv = 5 # Interval for downsampling the frequency and spatial temporal variables

print('Generating the sinusoidal signal...')
pattern_generator = SinusoidalPatternGenerator(w_mm, h_mm, width, height, Tb, Te)
spatial_temporal_signal = pattern_generator.generate_moving_sinusoidals(fx_vid, fy_vid, fps, vx_vid, vy_vid, intv)

# Viz for Spatial Temporal Signals
visualize_spatial_temporal_signal(folder_out + '/spatial_temporal.mp4', spatial_temporal_signal, width, height, fps, intv)

# Viz the viewer perspective results
visualize_viewed_signal(folder_out + '/viewing.mp4', spatial_temporal_signal, width, height, fps, intv, w_mm, h_mm, d_mm)

xformer = FourierTransformer()

# Compute frequency response
print('Computing Fourier transform for the sinusoidal signal...')
start_time = time.time()
frequency_signal = xformer.dft_video(spatial_temporal_signal)
end_time = time.time()
print(f"Computation time: {end_time - start_time:.4f} sec")


# Cache the results for testing or debugging
cache_signal(folder_out + '/frequency.sg', frequency_signal)

'''
# Load cached signal if you do not want to compute the same transform again, used for debugging.
frequency_signal = load_signal(folder_out + '/frequency.sg', spatial_temporal_signal.shape)
'''

# Viz for Frequency Response 
visualize_frequency_signal(folder_out + '/frequency_response.mp4', frequency_signal, width, height, fps, intv)

# Reconstruct spatial temporal signal via inverse fourier transform
print('Recovering the spatial temporal signal by inverse Fourier transform...')
start_time = time.time()
recovered_signal = xformer.idft(frequency_signal)
end_time = time.time()
print(f"Computation time: {end_time - start_time:.4f} sec")

# Cache reconstructed signal
cache_signal(folder_out + '/reconstruction.sg', recovered_signal)

# Visualize reconstructed signal (SHOULD be visually the same as original spatial temporal signal)
visualize_recovered_signal(folder_out + '/reconstruction.mp4', recovered_signal, width, height, fps, intv)

# Shift the frequency signal
print('Shifting the frequency signal...')
dx = 0
dy = 5
dt = 0
resized_height, resized_width, frames = frequency_signal.shape[0], frequency_signal.shape[1], frequency_signal.shape[2]
shifted_frequency_signal = np.zeros([resized_height, resized_width, frames], dtype=complex)
# TODO #2: Implement a shifting operation to move the frequency responses. The shifted responses are stored in
# shifted_frequency_signal
shifted_frequency_signal = np.roll(frequency_signal, shift=(dy, dx, dt), axis=(0, 1, 2))

# Viz for Shifted Frequency signal 
visualize_frequency_signal(folder_out + '/shifted_frequency.mp4', shifted_frequency_signal, width, height, fps, intv)

# Generate the corresponding spatial temporal signal, it SHOULD be changed.
print('Generating new spatial temporal signal according to the shifted frequency signal...')
edited_spatial_temporal_signal = xformer.idft(shifted_frequency_signal)

# Cache the new spatial temporal signal
cache_signal(folder_out + '/edited_spatial_temporal.sg', edited_spatial_temporal_signal)

# Visualize the new spatial temporal signal
visualize_recovered_signal(folder_out + '/edited_spatial_temporal.mp4', edited_spatial_temporal_signal, width, height, fps, intv)

