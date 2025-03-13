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
        # Compute 3D DFT manually
        # for k1 in range(height):
        #     for k2 in range(width):
        #         for k3 in range(frames):
        #             sum_val = 0
        #             for n1 in range(height):
        #                 for n2 in range(width):
        #                     for n3 in range(frames):
        #                         exponent = -2j * np.pi * ((k1 * n1 / height) + (k2 * n2 / width) + (k3 * n3 / frames))
        #                         sum_val += input_signal[n1, n2, n3] * np.exp(exponent)
        #             output_signal[k1, k2, k3] = sum_val
        for k1 in range(height):
            for k2 in range(width):
                for k3 in range(frames):
                    output_signal[k1, k2, k3] = np.sum(
                        input_signal * np.exp(-2j * np.pi * (
                            (k1 * np.arange(height)[:, None, None] / height) +
                            (k2 * np.arange(width)[None, :, None] / width) +
                            (k3 * np.arange(frames)[None, None, :] / frames)
                        ))
                    )

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
        # Compute 3D Inverse DFT manually
        # for n1 in range(height):
        #     for n2 in range(width):
        #         for n3 in range(frames):
        #             sum_val = 0
        #             for k1 in range(height):
        #                 for k2 in range(width):
        #                     for k3 in range(frames):
        #                         exponent = 2j * np.pi * ((k1 * n1 / height) + (k2 * n2 / width) + (k3 * n3 / frames))
        #                         sum_val += input_signal[k1, k2, k3] * np.exp(exponent)
        #             output_signal[n1, n2, n3] = sum_val / (height * width * frames)  # Normalize
        for n1 in range(height):
            for n2 in range(width):
                for n3 in range(frames):
                    output_signal[n1, n2, n3] = np.sum(
                        input_signal * np.exp(2j * np.pi * (
                            (n1 * np.arange(height)[:, None, None] / height) +
                            (n2 * np.arange(width)[None, :, None] / width) +
                            (n3 * np.arange(frames)[None, None, :] / frames)
                        ))
                    ) / (height * width * frames)

        return output_signal
