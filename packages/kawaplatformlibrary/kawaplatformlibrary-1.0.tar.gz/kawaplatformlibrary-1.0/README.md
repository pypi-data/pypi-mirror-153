# Kawa Library

This project is the backbone behind the Builder Platform which is being developed by the DS and Engg teams.

## Modules

There are currently 6 modules which can be developed over a 3 month period. 

### Data

All data ingestion pipelines for various data sources are placed in this module. Currently only contains the sentinel2DataIngestion pipeline.

### Indices

All indices built using any satellite data is to be placed in this module.

Contains the foll

### Models

All models built to be displayed/used by/for users on the builder platform

### Post-Processing

Standardisation of post-processing steps such as pixel coordinates to geojson, mask shape to geojson and so on.

### Pre-Processing

Standardisation of pre-processing data such as creating masks from geojsons, SAR data pre-processing, splitting bands[if possible] 

### Data Storage

All data storage options such as storing on local[VM] or uploading to Kawa Cloud[GCP/AWS Bucket for VM]

## Prerequistes

To install the required libraries please run the following command : 

```
pip install -r requirements.txt
```

## Authours

_Add contributor names here_

* Gotam Dahiya
* Manya Chadha