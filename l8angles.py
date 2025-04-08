import numpy as np
from l8angles_cython import calculate_angles


def _get_corners(metadata_fp: str):
    with open(metadata_fp) as f:
        metadata = f.read()

    # Find the four corner coordinates
    import re

    ul = re.search(r"UL_CORNER\s*=\s*\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)", metadata)
    ur = re.search(r"UR_CORNER\s*=\s*\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)", metadata)
    ll = re.search(r"LL_CORNER\s*=\s*\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)", metadata)
    lr = re.search(r"LR_CORNER\s*=\s*\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)", metadata)

    # Parse each into pairs of floats
    ulx = float(ul.group(1))
    uly = float(ul.group(2))
    urx = float(ur.group(1))
    ury = float(ur.group(2))
    llx = float(ll.group(1))
    lly = float(ll.group(2))
    lrx = float(lr.group(1))
    lry = float(lr.group(2))

    # Confirm that some coordinates match
    assert uly == ury
    assert lly == lry
    assert ulx == llx
    assert urx == lrx

    return ulx, urx, uly, lly


def calculate_angles_xarray(
    metadata_fp,
    angle_type="BOTH",
    subsample=1,
    bands=None,
):
    """Compute per-pixel solar and sensor azimuth and zenith angles from coefficient files.

    Returns an xarray Dataset for each angle type.

    This function is a thin wrapper around the ``calculate_angles`` function to return
    coordinate-aware xarray objects instead of numpy arrays.
    """

    import xarray as xr

    if isinstance(bands, int):
        bands = [bands]
    if bands is None or 8 in bands:
        raise ValueError("Panchromatic band (band 8) is not supported in xarray interface")

    data = calculate_angles(
        metadata_fp,
        angle_type=angle_type,
        subsample=subsample,
        bands=bands,
    )

    ulx, urx, uly, lly = _get_corners(metadata_fp)
    pixel_size = 30.0 * subsample
    x = np.arange(ulx, urx + 1, pixel_size)
    y = np.arange(uly, lly - 1, -pixel_size)

    out = {}
    for k, v in data.items():
        ds = xr.Dataset(
            {f"B{b}": (["y", "x"], a) for b, a in zip(bands, v, strict=True)},
            coords={"x": (["x"], x), "y": (["y"], y)},
        )
        out[k] = ds

    return out


__all__ = [
    "calculate_angles",
    "calculate_angles_xarray",
]
