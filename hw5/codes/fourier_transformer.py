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
    def dft_video(self, video, fast=False):
        # Convert the input video type into complex type
        video_complex = video.astype(complex)
        return self.fast_dft(video_complex) if fast == True else self.dft(video_complex)

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
        
        # Provide the implementation in HW4 

        return output_signal

    '''
    Inputs:
        - input_signal: 3D numpy array with complex numbers. 
    Outputs:
        - output_signal: 3D numpy array with complex numbers.
    '''
    def fast_dft(self, input_signal):
        # Get width, height, frames of the input_signal.
        height, width, frames = input_signal.real.shape[0], input_signal.real.shape[1], input_signal.real.shape[2] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros([height, width, frames], dtype=complex)
        
        # TODO #1: Implement 3D fourier transform for output_signal in terms of multi-pass 1D DFT
        # You can call either np.fft.fft for fast 1D DFT (wrap it into self.fft_numpy) or call your self implementation (define them into
        # self.fft)

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
        
        # Provide the implementation in HW4 

        return output_signal

    '''
    Inputs:
        - input_signal: 3D numpy array with complex numbers
    Outputs:
        - output_signal: 3D numpy array with complex numbers.
    '''
    def fast_idft(self, input_signal):
        # Get width, height, frames of the input_signal.
        height, width, frames = input_signal.real.shape[0], input_signal.real.shape[1], input_signal.real.shape[2] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros([height, width, frames], dtype=complex)
        
        # TODO #2: Implement 3D inverse fourier transform for output_signal in terms of multi-pass 1D DFT and conjugate complex numbers.
        # You can call either np.fft.fft for fast 1D DFT (wrap it into np.fft_numpy) or call your self implementation (define them into
        # self.fft)

        return output_signal


    '''
    Inputs:
        - input_signal: 1D numpy array with complex numbers. 
    Outputs:
        - output_signal: 1D numpy array with complex numbers.
    '''
    def fft_numpy(self, input_signal):
        # Get number of samples of the input_signal.
        num_samples = input_signal.real.shape[0] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros(num_samples, dtype=complex)

        # TODO #3: Incorporate numpy fft.fft API for the fast 1D DFT 

        return output_signal


    '''
    Inputs:
        - input_signal: 1D numpy array with complex numbers. 
    Outputs:
        - output_signal: 1D numpy array with complex numbers.
    '''
    def fft(self, input_signal):
        # Get number of samples of the input_signal.
        num_samples = input_signal.real.shape[0] 

        # Get frequency response by computing fourier dft on the input signals
        output_signal = np.zeros(num_samples, dtype=complex)

        # TODO #4: Implement the successive doubling method provided in the course slides 
        # Note that the number of samples should be power of 2 (handle the signal shape before calling this API)

        return output_signal



