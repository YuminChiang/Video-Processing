import numpy as np

class FourierTransformer():
    def __init__(self):
        pass

    '''
    Inputs:
        - video: 3D numpy array with real numbers
    Outputs:
        - output_signal: 3D numpy array with complex numbers
    '''
    def dft_video(self, video):
        # Convert the input video type into complex type
        video_complex = video.astype(complex)
        return self.dft(video_complex)

    '''
    Inputs:
        - input_signal: 3D numpy array with complex numbers. 
    Outputs:
        - output_signal: 3D numpy array with complex numbers.
    '''
    def dft(self, input_signal):
        # Get width, height, frames of the input_signal.
        height, width, frames = input_signal.real.shape[0], input_signal.real.shape[1], input_signal.real.shape[2] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros([height, width, frames], dtype=complex)
        
        # TODO #3: Implement 3D fourier transform for output_signal according to the DSFT formulas provided in the slides.
        # You are NOT ALLOWED to use any third party API to execute the Fourier transform 

        return output_signal

    '''
    Inputs:
        - input_signal: 3D numpy array with complex numbers
    Outputs:
        - output_signal: 3D numpy array with complex numbers.
    '''
    def idft(self, input_signal):
        # Get width, height, frames of the input_signal.
        height, width, frames = input_signal.real.shape[0], input_signal.real.shape[1], input_signal.real.shape[2] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros([height, width, frames], dtype=complex)
        
        # TODO #4: Implement 3D inverse Fourier transform for output_signal according to the IDSFT formulas provided in the slides.
        # You are NOT ALLOWED to use any third party API to execute the inverse Fourier transform 

        return output_signal
