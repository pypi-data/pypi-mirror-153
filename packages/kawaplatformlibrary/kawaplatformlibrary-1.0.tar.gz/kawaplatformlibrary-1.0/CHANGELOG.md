# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Version 1.0 - 2022-06-03](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v1.0.2rc) [Release]

### Unreleased

- Updated test and example files to reflect the current library version.

**Examples and test are broken as of now, due to this update. It has changed a lot of backend stuff.**

**As usual for a more stable user-experience use examples folder for creating code using kawaplatformlibrary**

### Added

- Added function for splitting a given date range dependent upon the days frequency.
- Added functionality for obtaining a bounding box from Point coordinates.

### Changed

- Changed output format for the Sentinel 2 data ingestion pipeline to accommodate the days frequency.
- Moved code for indices showcase from test to examples.
- Moved code for checking the library names from test to examples.
- Updated python version in setup.py to greater than 3.8


## [Version 1.0.2rc - 2022-05-05](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v1.0.2rc) [Pre-Release]

### Added

- A new test file for checking the module and sub-modules paths and names.
- New example for testing out the indices present in the library.
- Added Green Cluster model to the library.

### Changed

- Sys paths in test files have been changed along with the module and sub-module names. 

### Fixed

- Fixed errorneous function and class calls.
- Fixed test and examples to reflect the new module and sub-module convention.
- Removed duplicated parameters in kawaplatformlibrary.indices.evi_two.
- Fixed variable names in kawaplatformlibrary.indices.ndvi

## [Version 1.0rc2 - 2022-05-05](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v1.0rc2) [Pre-Release]

### Added

- Multiple tiles can now be mosaiced via the library itself.
- New profiles can be made using existing transformation matrixs and profiles.

### Fixed

- OSAVI formula is fixed where one variable was not defined in the function. 

## Version 0.1.3 - 2022-03-11 

### Added

- Added setup.py to allow for pip install.
- Added MANIFEST.in to include files used by the package.
- Shifted the library code to the folder kawaplatformlibrary.
- The examples folder is still outside the kawaplatformlibrary so that it can access that folder while testing.

### Changed

- Removed the sys paths from examples/download_tiles_mutli.py as that is no longer required.
- Had to change to 0.1.3 so that PyPi would allow me to upload it there.

### Fixed 

- Removed the examples folder from the package when installing so that people do not access it accidently.
- Fixed the import stattements in the indices folder 

## [Version 0.1](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v0.0.5) [Pre-Release]

### [Tag 0.0.5](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v0.0.5)

Introduced mutli-processing within the library for obtaining data from Sentinel 2 STAC API. Currently it is only present in data/sentinel2DataIngestion.py

Moved the preprocessing code to data folder so that all data ingestion codes can refer to all preprocessing codes. All centroids will be stored in preprocessing/satellitecentroids which will be accessed using Path from the pathlib library.

### [Tag 0.0.4](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v0.0.4)

Implemented multi-processing in examples/download_tiles_multi.py for testing and will be completely integrated into the library using the optimising_current_code.

### [Tag 0.0.2](https://github.com/KawaSpaceOrg/kawaplatformlibrary/tree/v0.0.2)

Currently works for downloading one Sentinel 2 Tile.

#### Features

##### Data

| File | Notes |
| :---:| :---: |
| sentinel2DataIngestion.py | Getting the links to sentinel 2 tiles for a specific area using the STAC API | 

##### Examples

| File | Notes |
| :---:| :---: |
| download_tiles.py | Example code for downloading a single Sentinel 2 tile from STAC API for a small AOI |

##### Postprocessing

| File | Notes |
| :---:| :---: |
| mosaic.py | For merging and resampling the various bands passed back |

##### Preprocessing

| File | Notes |
| :---:| :---: |
| splitGeojson.py | Splits a larger geojson into smaller square tiles of user-specified length. |

##### Indices

| File | Notes |
| :---:| :---: |
| bri.py | Browning Reflectance Index |
| ccci.py | Canopy Chlorophyll Content Index |
| cigreen.py | Chlorophyll Index Green |
| dswi.py | Disease Water Stress Index |
| evi.py | Enhanced Vegetaion Index |
| gemi.py | Global Environment Monitoring Index |
| mtvi_one.py | Modified Triangular Vegetation Index 1 |
| ndre.py | Normalised Difference Red-edge |
| ndvi.py | Normalised Vegetation Index |
| ndwi_crop.py | Normalised Difference Water Index (Crop Water) |
| ndwi_surface.py | Normalised Difference Water Index (Surface Water) |
| osavi.py | Optimised Soil-Adjusted Vegetation Index |
| savi.py | Soil-Adjusted Vegetation Index |

##### Satellite Centroids

| File | Notes |
| :---:| :---: |
| sentinel2_centroid_geojsons.geojson | GeoJSON of all centroids of Sentinel 2 data |