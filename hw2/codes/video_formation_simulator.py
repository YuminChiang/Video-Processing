import cv2
from rotated_rainbow import * 
from camera import *
from display import *

# Generate lights from a rotated rainbow
scene = RotatedRainbow()
elapsed_time_ms = 0 # in milli seconds
delta_time_ms_light = 10 # in milli seconds 

# Video simulation 側錄
fov = 60 # vertical fov in degrees
frames_per_second = 30 # 
image_width, image_height = 200, 150 # in pixels
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
scan_video = cv2.VideoWriter('scanning.mp4', fourcc, frames_per_second, (image_width, image_height))
camera = Camera(fov, image_width, image_height, frames_per_second)
display = Display(image_width, image_height)

# Timing setting
frame = 0 # camera 一整個畫面的 index
delta_time_ms_frame = 1000 / frames_per_second # frame 之間的間隔 delta t

# Illustrate the raster scanning processing by snapshoting the image on line rate
# Calculate the observation counter duration by setting it as the line interval divided by the number of rasters per line 
# (i.e., the image width).
elapsed_time_ms_observ = 0
line_interval = camera.get_line_interval()
delta_time_ms_observ = line_interval / image_width # 側錄 scaning 掃描到哪裡
frame_observ = 0 # 側錄 camera 的 frame

# TODO #1-1: Create a file handler for the output scanning.txt file for recording the scanning indices
# Check the recording format in slides.
# zero base   
# 1 2 3 5 7 8 first frame
# 1 3 4 5 6 7 second frame

# Constant for millisecond to second conversion
ms2sec = 0.001
while frame < 3:
    lights = scene.generate_lights(elapsed_time_ms * ms2sec)
    elapsed_time_ms += delta_time_ms_light

    camera.expose(lights) # freq response of lights

    if elapsed_time_ms >= frame * delta_time_ms_frame: # 當經過的時間已經到達要畫這個相機最新畫面的時候，開始啟動 scaning
        print('Start scanning for frame:', frame)
        elapsed_time_ms_observ = 0
        frame_observ = 0
        scan_idx_prev = 0
        camera.restart_scanning_frame()
        while not camera.frame_completed():
            camera.raster_scan(delta_time_ms_observ)

            # Display the scanning image. 產生觀察影像的過程，camera 的訊號衰減過後到達 display 的過程
            # If the observation timing precedes the completion of the frame, intermediate scanning results become visible.
            if (elapsed_time_ms_observ >= frame_observ * (0.1 * line_interval)):
                attenuation_image = camera.output_attenuation_image_scanned(scan_idx_prev,
                                                                 camera.get_scan_index()) # 把 camera 經過衰減的訊號存起來
                gc = camera.get_gamma()

                # Update latest scanned segment only for quick viz. freshing
                for idx in range(scan_idx_prev, camera.get_scan_index()):
                    y = int(idx / image_width)
                    x = idx - y * image_width
                    r, g, b = attenuation_image[y, x, :]
                    display_color = [r, g, b]
                    # TODO #2: Record brightness after correction (already done it on hw1)
                    vd = display.gamma_correct(display_color, gc) 
                    display_color = display.output_brightness(vd)
                    
                    rd, gd, bd = display_color[0], display_color[1], display_color[2]
                    display.write_buffer([x, y], rd, gd, bd)

                print('Observe scanned lines:', camera.scanned_lines, 'scan index:', camera.get_scan_index())
                display_image = display.output_buffer()
                scan_video.write(display_image)

                # TODO #1-2: Record current scan index into the output .txt file.

                frame_observ += 1
                scan_idx_prev = camera.get_scan_index()

            elapsed_time_ms_observ += delta_time_ms_observ

        # Clear the display buffer to prevent the retention of content from the previous frame.
        display.clear_buffer() 
        frame += 1

    print('Elapsed time in ms:', elapsed_time_ms)

# TODO #1-3: Close the output scanning.txt file.
scan_video.release()
