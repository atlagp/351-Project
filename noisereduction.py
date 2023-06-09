from scipy.fftpack import fft, ifft
import scipy.io.wavfile as wav
import scipy.signal as sg
import numpy as np

# mpg123 -w foo.wav foo.mp3

def halfwave_rectification(array):
    # This func computes teh half wave rectification with a threshold of 0
    #I: 1D np.array, O: 1D np.array
    halfwave = np.zeros(array.size)
    halfwave[np.argwhere(array > 0)] = 1
    return halfwave

class Wiener:
    #Ty "improved Signal-to-Noise Ratio Estimation for Speech Enhancement"
    def __init__(self, SR, WAV_DATA, *T_NOISE):
        """
        Input: WAV_FILE
            T_NOISE: float, Time in seconds
        """
        self.WAV_FILE, self.T_NOISE = WAV_FILE, T_NOISE
        self.FS, self.x = (SR, WAV_DATA) 
        self.NFFT, self.SHIFT, self.T_NOISE = 2**10, 0.5, T_NOISE
        self.FRAME = int(0.02*self.FS) #Frame 20ms

        # Computes the offset and number of frames for overlap
        self.OFFSET = int(self.SHIFT*self.FRAME)

        #Hanning window and energy EW
        self.WINDOW = sg.hann(self.FRAME)
        self.EW = np.sum(self.WINDOW)

        self.channels = np.arange(self.x.shape[1]) if self.x.shape != (self.x.size,)  else np.arange(1)
        if len(self.channels) == 1:
            self.x = np.array([self.x]).T
        length = self.x.shape[0] if len(self.channels) > 1 else self.x.size
        self.frames = np.arange((length - self.FRAME) // self.OFFSET + 1)
        # Evaluating noise psd with n_noise
        self.Sbb = self.welchs_periodogram()

    @staticmethod
    def a_posteriori_gain(SNR):
        """
        Function that computes the a posteriori gain G of Wiener filtering.
            Input :
                SNR : 1D np.array, Signal to Noise Ratio
            Output :
                G : 1D np.array, gain G of Wiener filtering
        """
        G = (SNR - 1)/SNR
        return G
    
    @staticmethod
    def a_priori_gain(SNR):
        """
        Function that computes the a priori gain G of Wiener filtering.
            Input :
                SNR : 1D np.array, Signal to Noise Ratio
            Output :
                G : 1D np.array, gain G of Wiener filtering
        """
        G = SNR/(SNR + 1)
        return G

    def welchs_periodogram(self):
        """
        Estimation of the Power Spectral Density (Sbb) of the stationnary noise
        with Welch's periodogram given prior knowledge of n_noise points where
        speech is absent.
            Output :
                Sbb : 1D np.array, Power Spectral Density of stationnary noise
        """
        # Initialising Sbb
        Sbb = np.zeros((self.NFFT, self.channels.size))

        self.N_NOISE = int(self.T_NOISE[0]*self.FS), int(self.T_NOISE[1]*self.FS)
        # Number of frames used for the noise
        noise_frames = np.arange(((self.N_NOISE[1] -  self.N_NOISE[0])-self.FRAME) // self.OFFSET + 1)
        for channel in self.channels:
            for frame in noise_frames:
                i_min, i_max = frame*self.OFFSET + self.N_NOISE[0], frame*self.OFFSET + self.FRAME + self.N_NOISE[0]
                x_framed = self.x[i_min:i_max, channel]*self.WINDOW
                X_framed = fft(x_framed, self.NFFT)
                Sbb[:, channel] = frame * Sbb[:, channel] / (frame + 1) + np.abs(X_framed)**2 / (frame + 1)
        return Sbb

    def moving_average(self):
        # Initialising Sbb
        Sbb = np.zeros((self.NFFT, self.channels.size))
        # Number of frames used for the noise
        noise_frames = np.arange((self.N_NOISE - self.FRAME) + 1)
        for channel in self.channels:
            for frame in noise_frames:
                x_framed = self.x[frame:frame + self.FRAME, channel]*self.WINDOW
                X_framed = fft(x_framed, self.NFFT)
                Sbb[:, channel] += np.abs(X_framed)**2
        return Sbb/noise_frames.size

    def wiener(self):
        """
        Function that returns the estimated speech signal using overlapp - add method
        by applying a Wiener Filter on each frame to the noised input signal.
        
            Output :
                s_est : 1D np.array, Estimated speech signal
                
        """
        # Initialising estimated signal s_est
        s_est = np.zeros(self.x.shape)
        for channel in self.channels:
            for frame in self.frames:
                ############# Initialising Frame ###################################
                # Temporal framing with a Hanning window
                i_min, i_max = frame*self.OFFSET, frame*self.OFFSET + self.FRAME
                x_framed = self.x[i_min:i_max, channel]*self.WINDOW

                # Zero padding x_framed
                X_framed = fft(x_framed, self.NFFT)

                ############# Wiener Filter ########################################
                # Apply a priori wiener gains G to X_framed to get output S
                SNR_post = (np.abs(X_framed)**2/self.EW)/self.Sbb[:, channel]
                G = Wiener.a_priori_gain(SNR_post)
                S = X_framed * G

                ############# Temporal estimated Signal ############################
                # Estimated signals at each frame normalized by the shift value
                temp_s_est = np.real(ifft(S)) * self.SHIFT
                s_est[i_min:i_max, channel] += temp_s_est[:self.FRAME]  # Truncating zero padding
        return (self.FS, s_est/s_est.max())

    def wiener_two_step(self):
        """
        Function that returns the estimated speech signals using overlapp - add method
        by applying a Two Step Noise Reduction on each frame (s_est_tsnr) to the noised input signal (x).
        
            Output :
                s_est_tsnr, s_est_hrnr : 1D np.array, 1D np.array
                
        """
        # Typical constant used to determine SNR_dd_prio
        beta = 0.98

        # Initialising output estimated signal
        s_est_tsnr = np.zeros(self.x.shape)

        # Initialising matrix to store previous values.
        # For readability purposes, -1 represents past frame values and 0 represents actual frame values.
        S = np.zeros((2, self.NFFT), dtype='cfloat')
        for channel in self.channels:
            for frame in self.frames:
                ############# Initialising Frame ###################################
                # Temporal framing with a Hanning window
                i_min, i_max = frame*self.OFFSET, frame*self.OFFSET + self.FRAME
                x_framed = self.x[i_min:i_max, channel]*self.WINDOW

                # Zero padding x_framed
                X_framed = fft(x_framed, self.NFFT)

                ############# Wiener Filter ########################################
                # Computation of spectral gain G using SNR a posteriori
                SNR_post = np.abs(X_framed)**2/self.EW/self.Sbb[:, channel]
                G = Wiener.a_priori_gain(SNR_post)
                S[0, :] = G * X_framed

                ############# Directed Decision ####################################
                # Computation of spectral gain G_dd using output S of Wiener Filter
                SNR_dd_prio = beta*np.abs(S[-1, :])**2/self.Sbb[:, channel] + (1 - beta)*halfwave_rectification(SNR_post - 1)
                G_dd = Wiener.a_priori_gain(SNR_dd_prio)
                S_dd = G_dd * X_framed

                ############# Two Step Noise Reduction #############################
                # Computation of spectral gain G_tsnr using output S_dd of Directed Decision
                SNR_tsnr_prio = np.abs(S_dd)**2/self.Sbb[:, channel]
                G_tsnr = Wiener.a_priori_gain(SNR_tsnr_prio)
                S_tsnr = G_tsnr * X_framed

                ############# Temporal estimated Signal ############################
                # Estimated signal at frame normalized by the shift value
                temp_s_est_tsnr = np.real(ifft(S_tsnr))*self.SHIFT
                s_est_tsnr[i_min:i_max, channel] += temp_s_est_tsnr[:self.FRAME] # Truncating zero padding

                ############# Update ###############################################
                # Rolling matrix to update old values (Circshift in Matlab)
                S = np.roll(S, 1, axis=0)
        wav.write(self.WAV_FILE+'_wiener_two_step.wav', self.FS,s_est_tsnr/s_est_tsnr.max() )
