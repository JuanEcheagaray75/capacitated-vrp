# Coppel Vehicle Routing Problem

- [Coppel Vehicle Routing Problem](#coppel-vehicle-routing-problem)
  - [Database](#database)
  - [Data cleaning](#data-cleaning)
    - [Geo-coding addresses](#geo-coding-addresses)
  - [Solving the VRP](#solving-the-vrp)
  - [Results](#results)
  - [Installation and usage](#installation-and-usage)
  - [License](#license)

## Database

For this project we received 4 different datasets. Here is a small overview of the information contained in these files:

- Assets to be delivered: Excel file with every purchase made on the company's website
- Types of vehicles that can be used:
  - Name of the model
  - Gasoline consumption
  - Maximum load capacity
- Product catalog:
  - Product category
  - Name of the product
  - Code
  - Volume
- Distribution Centers' locations (For this project we have focused solely in Monterrey)
  - Name of the distribution center
  - Location, both address and coordinates

## Data cleaning

[(Back to top)](#table-of-contents)

For the purposes of working with these databases we adopted the common library [pandas](https://pandas.pydata.org/)

### Geo-coding addresses

[(Back to top)](#table-of-contents)

- Mentioning how the usage of Photon as a geocoder seriously limits the number of addresses that are geocoded successfully.
- Purchasing a Google Maps comercial API key to improve both the performance and speed of the geocoding process.

## Solving the VRP

[(Back to top)](#table-of-contents)

## Results

[(Back to top)](#table-of-contents)

## Installation and usage

[(Back to top)](#table-of-contents)

This repo was designed and tested with Python 3.8 running on Ubuntu based on WSL2.

1. Clone the repository to the location of your choosing:
    - `git clone https://github.com/JuanEcheagaray75/coppel-vrp-tsp.git`
2. I recommend creating a virtual environment for this project, but feel free to skip this step>
    - `python3 -m venv .venv`
3. Activate the virtual environment:
    - `source .venv/bin/activate`
4. Install the dependencies:
    - `pip install -r requirements.txt`

## License

[(Back to top)](#table-of-contents)

[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)
