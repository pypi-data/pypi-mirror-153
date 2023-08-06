from setuptools import setup, find_packages

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

#def download_data(url='http://...'):
    # Download; extract data to disk.
    # Raise an exception if the link is bad, or we can't connect, etc.

#def load_data():
#    if not os.path.exists(DATA_DIR):
#        download_data()
#    data = read_data_from_disk(DATA_DIR)
#    return data

setup(
    name="madys",
    version="0.2.0",
    author='Vito Squicciarini',
    author_email='vito.squicciarini@inaf.it',
    description='Manifold Age Determination for Young Stars',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vsquicciarini/madys',
    project_urls={
        "Bug Tracker": "https://github.com/vsquicciarini/madys/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
    'numpy', 'scipy', 'astropy', 'pandas', 'matplotlib', 'astroquery', 'sh', 'h5py', 'astroquery', 'tabulate'],
    packages=['madys'],
    include_package_data=True,
    package_data={
    'madys': [r'info_filters.txt',
              r'isochrones/BHAC15/*',
              r'isochrones/PARSEC/*',
              r'isochrones/ATMO_2020/*.txt',
              r'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/MKO_WISE_IRAC/*',
              r'isochrones/PHOENIX/AMES_Cond/*',
              r'isochrones/PHOENIX/AMES_Dusty/*',
              r'isochrones/Sonora/Bobcat/*',
    ],},
    zip_safe=False
)
#              'isochrones/MIST/*',
#              'isochrones/STAREVOL/*',
#              'isochrones/SPOTS/*',
#              'isochrones/B97/*',
#              'isochrones/PM13/*',
#              'isochrones/SB12/*',
#              'isochrones/Dartmouth/*',
#              'isochrones/Geneva/iso/*',
#              'isochrones/PHOENIX/BT_NextGen/*',
#              'isochrones/PHOENIX/BT_Settl/*',
#              'isochrones/PHOENIX/NextGen/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRCAM_MASK210R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRCAM_MASK335R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRCAM_MASK430R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRCAM_MASKLWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRCAM_MASKSWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_coronagraphy/JWST_coron_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_photometry/JWST_phot_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_photometry/JWST_phot_NIRCAM_modA/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_photometry/JWST_phot_NIRCAM_modA_mean/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_photometry/JWST_phot_NIRCAM_modB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_CEQ/JWST_photometry/JWST_phot_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRCAM_MASK210R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRCAM_MASK335R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRCAM_MASK430R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRCAM_MASKLWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRCAM_MASKSWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_coronagraphy/JWST_coron_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_photometry/JWST_phot_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_photometry/JWST_phot_NIRCAM_modA/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_photometry/JWST_phot_NIRCAM_modA_mean/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_photometry/JWST_phot_NIRCAM_modB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/JWST_photometry/JWST_phot_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_strong/MKO_WISE_IRAC/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_NIRCAM_MASK210R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_NIRCAM_MASK335R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_NIRCAM_MASK430R/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_NIRCAM_MASKLWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_coronagraphy/JWST_coron_NIRCAM_MASKSWB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_sweak/JWST_coronagraphy/JWST_coron_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_photometry/JWST_phot_MIRI/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_photometry/JWST_phot_NIRCAM_modA/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_photometry/JWST_phot_NIRCAM_modA_mean/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_photometry/JWST_phot_NIRCAM_modB/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/JWST_photometry/JWST_phot_NIRISS/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/ATMO_NEQ_weak/MKO_WISE_IRAC/*',
#              'isochrones/ATMO_2020/evolutionary_tracks/vega_spectrum/*',
#              'extinction/*',
