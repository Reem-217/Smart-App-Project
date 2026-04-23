# Egypt Soil Dataset

This dataset contains soil property measurements across Egypt, retrieved from the **ISRIC SoilGrids v2.0** API.

## Dataset Specifications

- **Source:** [SoilGrids (ISRIC)](https://www.isric.org/explore/soilgrids)
- **Coverage:** Egypt (Lat: 22.0 to 31.7, Lon: 24.7 to 36.9)
- **Resolution:** 250m (sampled at 0.5-degree grid intervals)
- **Depth:** 0-5 cm (Topsoil)
- **Format:** CSV (`egypt_soil_dataset.csv`)

## Features

| Column | Property | Unit | Description |
| :--- | :--- | :--- | :--- |
| `lat` | Latitude | Decimal Degrees | WGS84 Coordinate |
| `lon` | Longitude | Decimal Degrees | WGS84 Coordinate |
| `phh2o` | pH index | pH | Soil acidity/alkalinity in water |
| `clay` | Clay content | % | Mass fraction of clay particles |
| `soc` | Soil Organic Carbon | g/kg | Organic carbon content by mass |
| `sand` | Sand content | % | Mass fraction of sand particles |
| `silt` | Silt content | % | Mass fraction of silt particles |
| `nitrogen` | Total Nitrogen | g/kg | Total nitrogen content |

## Data Processing & Scaling

The raw data from SoilGrids v2.0 is often returned with a conventional scaling factor. This dataset has been pre-processed as follows:
- **pH, Clay, Sand, Silt, Nitrogen:** Values are divided by 10 (e.g., a raw value of `75` in pH becomes `7.5`).
- **SOC:** Converted from dg/kg to g/kg (divided by 10).

