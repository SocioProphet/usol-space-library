def box_corners(ra_deg: float, dec_deg: float, width_deg: float, height_deg: float, rot_deg: float = 0.0):
    # Returns approximate RA/Dec box corners. This intentionally does not apply
    # spherical projection correction in the v3 baseline.
    hw = width_deg / 2.0
    hh = height_deg / 2.0
    return [
        (ra_deg - hw, dec_deg - hh),
        (ra_deg - hw, dec_deg + hh),
        (ra_deg + hw, dec_deg + hh),
        (ra_deg + hw, dec_deg - hh),
    ]
