from astropy.io import fits
import numpy as np


def open_fits(path: str):
    return fits.open(path)


def sample_pixel(hpx_map: np.ndarray, nside: int, ra_deg: float, dec_deg: float):
    import healpy as hp

    theta = np.radians(90.0 - dec_deg)
    phi = np.radians(ra_deg)
    pix = hp.ang2pix(nside, theta, phi, nest=False)
    return hpx_map[pix]


def bilinear_sample(hpx_map, nside: int, ra_deg: float, dec_deg: float, nest: bool = False):
    """Sample a HEALPix map using healpy.get_interp_val."""
    import healpy as hp

    theta = np.radians(90.0 - dec_deg)
    phi = np.radians(ra_deg)
    return hp.get_interp_val(hpx_map, theta, phi, nest=nest)


def beam_solid_angle(fwhm_deg: float):
    """Approximate Gaussian beam solid angle in steradians."""
    sigma_rad = np.radians(fwhm_deg) / (2.0 * (2.0 * np.log(2)) ** 0.5)
    return 2.0 * np.pi * sigma_rad**2
