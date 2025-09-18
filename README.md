# Modeling streamflow drought

> _A newer version of the software may be available. See https://code.usgs.gov/wma/vizlab/modeling-drought/-/releases to view all releases._

This repo uses Python and Javascript to build a data visualization website about the methodology behind USGS streamflow drought modeling.

**The data visualization website can be viewed at [https://water.usgs.gov/vizlab/modeling-drought](https://water.usgs.gov/vizlab/modeling-drought).**

## Building the data visualizations

1. In the project directory, use a conda environment manager (we recommend [Miniforge](https://github.com/conda-forge/miniforge)) to install the environment: `conda env create -f environment.yaml`.
2. To recreate the data visualizations, use `snakemake --cores 1`. This will rebuild the interactive `.svg` images within the webpage.
3. You can modify the plot scripts by editing the `.py` files in `Task1/src` and `Task2/src`. 

There are other locations in this directory that you may also want to visit to adjust or edit the figures.

- The `Task_Data` directory holds the datafiles used to generate the visualizations
- The `Task_config` directory holds a `parameters.yaml` file that you can use to adjust the colors and look of the visualizations. It also houses a `.py` file with the functions used and the default parameters used for [`matplotlib`](https://matplotlib.org/).
- `src/assets/svgs` will house the `.svg` files used for the website.


## Building the website locally

Clone the repo. In the directory, run `npm install` to install the required modules. Once the dependencies have been installed, run `npm run dev` to run locally from your browser.

To build the website locally you'll need `node.js` `v22.14.0` and `npm` `v10.9.2` or higher installed. To manage multiple versions of `npm`, you may [try using `nvm`](https://betterprogramming.pub/how-to-change-node-js-version-between-projects-using-nvm-3ad2416bda7e).

## Citation

Kwang, Jeffrey, Corson-Dosch, Hayley, Diaz, Jeremy, Archer, Althea, Carr, Mandie, and Nell, Cee. 2025. Modeling Streamflow Drought. U.S. Geological Survey software release. Reston, VA. [https://doi.org/10.5066/P14RLGAU](https://doi.org/10.5066/P14RLGAU)

## Consulting subject matter experts
John Hammond consulted on the development of this website as a subject matter expert.

## Additional information
* We welcome contributions from the community. See the [guidelines for contributing](https://github.com/DOI-USGS/modeling-drought/) to this repository on GitHub.
* [Disclaimer](https://code.usgs.gov/wma/vizlab/modeling-drought/-/blob/main/DISCLAIMER.md)
* [License](https://code.usgs.gov/wma/vizlab/modeling-drought/-/blob/main/LICENSE.md)