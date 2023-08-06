import numpy as np
from matplotlib import pyplot as plt


def plot_spectrum(x: np.ndarray, eps: float = 1e-7):
    assert len(x.shape) == 1
    x_fft = np.fft.fft(x)
    x_fft_abs = np.abs(x_fft)
    x_fft_angle = np.angle(x_fft)
    f_dig = np.linspace(-np.pi, np.pi, x.shape[0])
    plt.subplot(2, 1, 1)
    plt.plot(f_dig, 10 * np.log10(x_fft_abs + eps))
    plt.ylabel("dB")
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.plot(f_dig, x_fft_angle)
    plt.grid()
    plt.show()
