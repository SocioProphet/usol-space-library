from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np


def open_spectrum_cube(path: str):
    return fits.open(path)


def planck_nu(nu_hz, T=2.725):
    h = 6.62607015e-34
    k = 1.380649e-23
    c = 299792458.0
    nu = np.asarray(nu_hz, dtype=float)
    x = h * nu / (k * T)
    return (2.0 * h * nu**3) / (c**2) / (np.exp(x) - 1.0)


def residual_to_planck(nu_hz, I_nu, T=2.725):
    return np.asarray(I_nu) - planck_nu(nu_hz, T=T)


def plot_spectrum(nu_hz, I_nu, T=2.725):
    plt.figure()
    plt.loglog(nu_hz, I_nu, label="Measured")
    plt.loglog(nu_hz, planck_nu(nu_hz, T), label=f"Planck {T:.3f} K")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("I_ν (W m⁻² sr⁻¹ Hz⁻¹)")
    plt.legend()
    plt.title("FIRAS Spectrum vs. Planck Law")
    plt.tight_layout()
