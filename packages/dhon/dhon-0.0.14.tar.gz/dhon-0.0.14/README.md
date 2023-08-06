# Dhon

*Dhon (ধন) - Assamese word for money*

A cli currency conversion tool

> Note: rates are updated weekly (source limitation)

## Usage

Here are some examples:

`100 USD to INR` - converts 100 USD to INR

`EUR to JPY` - converts 1 EUR to JPY

`420 GBP INR` - converts 420 GBP to INR

## Features

* supports 32 currencies
* you can force update using `--update`
* easy to use?
* no API used

## Features to be added

* better `--update` flag parsing
    * maybe using `argparse`
* `--reverse` flag as a qol update
* lines changed info when updating

## Data source

[This](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml) xml file which is updated weekly.
