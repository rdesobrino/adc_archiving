# adc_archiving

This repository contains scripts and helper templates for generating eml metadata for the Arctic Data Center of UAV data products with minimal manual configuring. 

GDAL is required for execution. 
## metadata.py

Currently: run metadata.py from the command line with an input csv containing the correctly formatted fields. Template is found in lib folder. 
```commandline
python metadata.py -i input_fields.csv
```
.xml files will be output to eml folder. 