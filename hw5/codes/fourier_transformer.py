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
        for fx in range(height):
            for fy in range(width):
                for ft in range(frames):
                    output_signal[fx, fy, ft] = np.sum(
                        input_signal * np.exp(-2j * np.pi * (
                            (fx * np.arange(height)[:, None, None] / height) +
                            (fy * np.arange(width)[None, :, None] / width) +
                            (ft * np.arange(frames)[None, None, :] / frames)
                        ))
                    )

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
        output_signal[...] = input_signal

        for fx in range(height):
            for fy in range(width):
                output_signal[fx, fy, :] = self.fft_numpy(output_signal[fx, fy, :])

        for fx in range(height):
            for ft in range(frames):
                output_signal[fx, :, ft] = self.fft_numpy(output_signal[fx, :, ft])

        for fy in range(width):
            for ft in range(frames):
                output_signal[:, fy, ft] = self.fft_numpy(output_signal[:, fy, ft])

        # output_signal = np.apply_along_axis(self.fft_numpy, axis=2, arr=output_signal) # time axis
        # output_signal = np.apply_along_axis(self.fft_numpy, axis=1, arr=output_signal) # width axis
        # output_signal = np.apply_along_axis(self.fft_numpy, axis=0, arr=output_signal) # height axis
        
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
        for x in range(height):
            for y in range(width):
                for t in range(frames):
                    output_signal[x, y, t] = np.sum(
                        input_signal * np.exp(2j * np.pi * (
                            (x * np.arange(height)[:, None, None] / height) +
                            (y * np.arange(width)[None, :, None] / width) +
                            (t * np.arange(frames)[None, None, :] / frames)
                        ))
                    ) / (height * width * frames) # Normalize

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
        output_signal[...] = input_signal
        output_signal = np.conj(output_signal)

        for x in range(height):
            for y in range(width):
                output_signal[x, y, :] = self.fft_numpy(output_signal[x, y, :])

        for x in range(height):
            for t in range(frames):
                output_signal[x, :, t] = self.fft_numpy(output_signal[x, :, t])

        for y in range(width):
            for t in range(frames):
                output_signal[:, y, t] = self.fft_numpy(output_signal[:, y, t])
        
        # output_signal = np.apply_along_axis(self.fft_numpy, axis=2, arr=output_signal)  # time axis
        # output_signal = np.apply_along_axis(self.fft_numpy, axis=1, arr=output_signal)  # width axis
        # output_signal = np.apply_along_axis(self.fft_numpy, axis=0, arr=output_signal)  # height axis

        output_signal = np.conj(output_signal) / (height * width * frames)

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
        output_signal = np.fft.fft(input_signal)

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
        if not (num_samples > 0 and (num_samples & (num_samples - 1)) == 0):
            raise ValueError("Number of samples must be a power of 2 for successive doubling FFT")

        if num_samples == 1:
            output_signal[0] = input_signal[0]
            return output_signal

        even_indices = input_signal[0::2]  # even part
        odd_indices = input_signal[1::2]   # odd part

        even_fft = self.fft(even_indices)
        odd_fft = self.fft(odd_indices)

        # twiddle factor: W_M^u = e^(-j 2π u / M)
        half_samples = num_samples // 2
        twiddle = np.exp(-2j * np.pi * np.arange(half_samples) / num_samples)

        output_signal[0:half_samples] = even_fft + twiddle * odd_fft
        output_signal[half_samples:num_samples] = even_fft - twiddle * odd_fft

        return output_signal



