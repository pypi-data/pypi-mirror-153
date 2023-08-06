# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyepy',
 'eyepy.core',
 'eyepy.data',
 'eyepy.io',
 'eyepy.io.heyex',
 'eyepy.io.heyex.specification',
 'eyepy.io.heyex.specification.vol_export',
 'eyepy.io.heyex.specification.xml_export',
 'eyepy.quantification',
 'eyepy.quantification.utils']

package_data = \
{'': ['*']}

install_requires = \
['imagecodecs>=2021.11.20,<2022.0.0',
 'itk>=5.2.1,<6.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'scikit-image>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'eyepie',
    'version': '0.6.7',
    'description': 'The Python package for working with ophthalmological data.',
    'long_description': '# eyepy\n\n[![PyPI version](https://badge.fury.io/py/eyepie.svg)](https://badge.fury.io/py/eyepie)\n[![DOI](https://zenodo.org/badge/292547201.svg)](https://zenodo.org/badge/latestdoi/292547201)\n\n\n\nThis package is under active development and things might change without\nbackwards compatibility. If you want to use eyepy in your project make sure to\npin the version in your project requirements.\n\n\n## Features\n\n* Import HEYEY XML and VOL exports\n* Import B-Scans from a folder\n* Import public [AMD Dataset from Duke University](https://people.duke.edu/~sf59/RPEDC_Ophth_2013_dataset.htm)\n* Import data of the [RETOUCH Challenge](https://retouch.grand-challenge.org/).\n* Compute Drusen voxel annotation from BM and RPE layer segmentations\n* Quantify voxel annotations on a customizable circular grid\n* Plot annotated localizer\n* Plot annotated B-scans\n* Save and load EyeVolume objects\n\n## Getting Started\n\n### Installation\nTo install the latest version of eyepy run `pip install -U eyepie`. It is `eyepie` and not `eyepy` for installation with pip.\n\n### Import Data\nWhen you don\'t hava a supported OCT volume at hand you can check out our sample dataset to get familiar with `eyepy`.\n```python\nimport eyepy as ep\n# Import HEYEX XML export\nev = ep.data.load("drusen_patient")\n```\n\n`eyepy` currently supports the HEYEX XML and VOL export format. Support for additional formats is easy to implement.\n\n```python\nimport eyepy as ep\n# Import HEYEX XML export\nev = ep.import_heyex_xml("path/to/folder")\n# Import HEYEX VOL export\nev = ep.import_heyex_vol("path/to/file.vol")\n```\n\nWhen only B-scans exist in a folder `eyepy` might still be able to import them. B-scans are expected to be ordered and distributed with equal distance on a quadratic area.\n```python\nimport eyepy as ep\n# Import B-scans from folder\nev = ep.import_bscan_folder("path/to/folder")\n```\n\nPublic OCT datasets often have their own data formats. `eyepy` can already import volumes from two of the biggest OCT datasets.\n```python\nimport eyepy as ep\n# Import DUKE volume\nev = ep.import_duke_mat("path/to/volume.mat")\n# Import RETOUCH volume\nev = ep.import_retouch("path/to/folder")\n```\n\n### The EyeVolume Object\nWhen `eyepy` imports OCT data, it always returns an EyeVolume object. This object provides a unified interface to data imported from various sources.\n\nYou can use this object to perform common actions on the OCT volume such as:\n\n+ Access Meta information from the loaded data if available `ev.meta`\n+ Access an associated localizer image `ev.localizer`. When no localizer image is available `eyepy` generates one using a mean projection.\n+ Access associated layer voxel and A-scan annotations\n+ Plot annotated localizer image associated to the volume `ev.plot()`\n+ Iterate over the volume to retrieve EyeBscan objects `for bscan in ev:`\n\n### Compute Drusen and Quantify\nHere we compute and quantify drusen for our sample data which has manual layer annotations for BM and RPE.\n\nIn the resulting plot on the left, the scale is the drusen height in voxel and on the right, the drusen volume in mm³\n\n```python\nimport matplotlib.pyplot as plt\nimport eyepy as ep\n\n# Import example data\nev = ep.data.load("drusen_patient")\ndrusen_map = ep.drusen(ev.layers["RPE"], ev.layers["BM"], ev.shape, minimum_height=2)\nev.add_voxel_annotation(drusen_map, name="drusen")\n\nfig, axes = plt.subplots(1, 2, figsize=(5, 10))\n\n# Configure quantification grid for drusen quantification\nev.volume_maps["drusen"].radii = [1.5, 2.5]\nev.volume_maps["drusen"].n_sectors = [4, 8]\nev.volume_maps["drusen"].offsets = [0, 45]\n\n# Plot drusen projection and quantification\nev.plot(ax=axes[0], projections=["drusen"])\nev.plot(ax=axes[1], quantification="drusen")\naxes[0].axis("off")\naxes[1].axis("off")\n```\n![Example quantification](examples/drusen_quantification.jpeg)\n\nTo access the quantification as a dictionary use `ev.volume_maps["drusen"].quantification`\n\n### Interact with individual B-scans\nIf you index into an EyeVolume object you get EyeBscan objects.\n\n```python\nimport numpy as np\n\nfig, ax = plt.subplots(1,1, figsize=(9,3))\nbscan = ev[40]\nbscan.plot(layers=["BM", "RPE"], areas=["drusen"], region=np.s_[150:300, :], ax=ax)\nax.axis("off")\n```\n\n![Example quantification](examples/bscan_visualization.jpeg)\n\n# Related Projects:\n\n+ [OCT-Converter](https://github.com/marksgraham/OCT-Converter): Extract raw optical coherence tomography (OCT) and fundus data from proprietary file formats. (.fds/.fda/.e2e/.img/.oct/.dcm)\n+ [eyelab](https://github.com/MedVisBonn/eyelab): A GUI for annotation of OCT data based on eyepy\n',
    'author': 'Olivier Morelle',
    'author_email': 'oli4morelle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MedVisBonn/eyepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
