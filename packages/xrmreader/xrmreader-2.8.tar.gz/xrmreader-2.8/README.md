## Reading and preprocessing x-ray projection data in Zeiss .txrm format

This package extends the [dxchange reader](https://github.com/data-exchange/dxchange "Dxchange github") to read the Zeiss proprietary data format .txrm to python lists or arrays. In particular, the import of metadata from the file headers is extended to access information needed for reconstructing x-ray projection data, e.g. acquired on Zeiss x-ray microscopes. Further, the package contains some simple functions to preprocess x-ray projections in preparation for reconstruction. These include flat field correction, revision of detector shifts, downsampling, conversion into line integral domain and truncation correction.  

For installation, please run
```shell
conda install -c conda-forge dxchange
pip install xrmreader
```

This example code uses [pyconrad](https://git5.cs.fau.de/PyConrad/pyCONRAD "Pyconrad github") for visualization.

```python
import xrmreader
import pyconrad.autoinit
from edu.stanford.rsl.conrad.data.numeric import NumericGrid


projection_data = r'your_file.txrm'

metadata = xrmreader.read_metadata(projection_data)
print(metadata)

# load raw data
raw_projections = xrmreader.read_txrm(projection_data)
NumericGrid.from_numpy(raw_projections).show('Raw projections')

# preprocess data in individual steps
projections = xrmreader.read_txrm(projection_data)
projections = xrmreader.divide_by_reference(projections, metadata['reference'])
projections = xrmreader.revert_shifts(projections, metadata['x-shifts'], metadata['y-shifts'])
projections = xrmreader.downsample(projections, spatial_factor=2)
projections = xrmreader.negative_logarithm(projections)
projections = xrmreader.truncation_correction(projections)
NumericGrid.from_numpy(projections).show('Preprocessed projections version 1')

# load and preprocess data in one step (this does the same thing as the individual steps above, but needs less memory)
preprocessed_projections = xrmreader.read_and_preprocess_txrm(projection_data)
NumericGrid.from_numpy(preprocessed_projections).show('Preprocessed projections version 2')
```
