import numpy
from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension

sources = [
    "l8angles.pyx",
    "src/l8_angles.c",
    "src/ias_lib/ias_angle_gen_calculate_angles_rpc.c",
    "src/ias_lib/ias_angle_gen_find_scas.c",
    "src/ias_lib/ias_angle_gen_initialize.c",
    "src/ias_lib/ias_angle_gen_read_ang.c",
    "src/ias_lib/ias_angle_gen_utilities.c",
    "src/ias_lib/ias_angle_gen_write_image.c",
    "src/ias_lib/ias_geo_convert_dms2deg.c",
    "src/ias_lib/ias_logging.c",
    "src/ias_lib/ias_math_compute_unit_vector.c",
    "src/ias_lib/ias_math_compute_vector_length.c",
    "src/ias_lib/ias_math_find_line_segment_intersection.c",
    "src/ias_lib/ias_misc_convert_to_uppercase.c",
    "src/ias_lib/ias_misc_create_output_image_trim_lut.c",
    "src/ias_lib/ias_misc_write_envi_header.c",
    "src/ias_lib/ias_odl_free_tree.c",
    "src/ias_lib/ias_odl_get_field.c",
    "src/ias_lib/ias_odl_read_tree.c",
    "src/ias_lib/ias_parm_check_ranges.c",
    "src/ias_lib/ias_parm_map_odl_type.c",
    "src/ias_lib/ias_parm_provide_help.c",
    "src/ias_lib/ias_parm_read.c",
    "src/ias_lib/ias_satellite_attributes.c",
    "src/ias_lib/lablib3.c",
    "src/ias_lib/landsat8.c",
]

extensions = [
    Extension(
        name="l8angles",
        sources=sources,
        include_dirs=["src", "src/ias_lib", numpy.get_include()],
    ),
]

setup(
    name="l8angles",
    ext_modules=cythonize(extensions),
)
