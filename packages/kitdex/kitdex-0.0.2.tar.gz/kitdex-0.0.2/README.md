# KitDex

KitDex is a simple program to record where tools and other "kit" is stored in a workshop. It then generates a printable index for your workshop.

It is not designed for inventory management.

## Development status

KitDex is designed for my own needs organising a couple of workshops. It is not sophisticated at all.

## Installation

KitDex requires PDFLaTeX to be installed and on your computer's PATH.

KitDex is a python program requiring python 3.6 and above. Install KitDex with:

`pip install kitdex`

## Usage

#### First use

Run:

`kidex -n directory.yml`

This should open the interactive editor. Start by populating a list of locations that kit can be stored at.

Once you have populated the location list you can add kit to the directory.

#### To edit the same directory

Run:

`kidex directory.yml`
