## utilities
- **explore-data.py:** data exploration examples
- **check-311.py:** utility for exporting a CSV of TSI SRs for a given regular expression

## usage
To run:
1. download the `GeoJSON`?)-formatted files for the **OpenDataDC data 311 datasources** above, and place them in a `data` folder in the repo:
   - https://opendata.dc.gov/datasets/311-city-service-requests-in-2023/ as `2023-311.geojson`
   - https://opendata.dc.gov/datasets/311-city-service-requests-in-2022/ as `2022-311.geojson`
   - and so on; these files can be regenerated on demand to capture the newest info (including new resolution info for previous years)
2. either use the included conda environment (requires Anaconda or [miniconda](https://docs.conda.io/en/latest/miniconda.html)) to pull package dependencies through an environment:

   ```shell
   conda env create
   conda activate tsi-data
   ```

   or use `pip` (assumes python is already installed)

   ```shell
   pip install geopandas
   ```

3. run `check-311.py`

   ```shell
   python check-311.py
   ```
   
   or, within a Python terminal:

   ```python
    exec(open('check-311.py').read())
    ```
