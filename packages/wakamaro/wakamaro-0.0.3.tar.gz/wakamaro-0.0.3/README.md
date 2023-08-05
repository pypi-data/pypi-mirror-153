# wakamaro

## Abstract
wakamaro is a package for visualizing the number of waka poetry composed by poets in Nijuichidaishu (21 waka poetry anthologies)

Using a Nijuichidaishu dataset, Visualize the number of waka poetry per waka poet.

The Nijuichidaishu dataset is downloadable from:
http://codh.rois.ac.jp/pmjt/


## Overview of Data
- the Center for Open Data in the Humanities
- “The Dataset of Pre-Modern Japanese Text (the National Institute of Japanese Literature)
- http://codh.rois.ac.jp/index.html.en

Link to download data
- http://codh.rois.ac.jp/pmjt/package/text.zip


## How to run wakamaro
$ pip install wakamaro


## How to run wakamaro
$ wakamaro <number of Nijuichidaishu> <number of appearances>

The first argument: number of Nijuichidaishu (1 to 21)
The second argument: minimum number of appearances of the waka poets to be displayed

Example of Running: waka poets that appeared more than 5 times in kokin wakashu
$ wakamaro 1 5

<img src="https://github.com/AihaIkegami/wakamaro/blob/main/01_%E5%8F%A4%E4%BB%8A%E5%92%8C%E6%AD%8C%E9%9B%86_bar.jpg" alt="result">

The vertical axis shows number of appearances in waka poetry.
The horizontal axis show appearance of waka poets in waka poetry.
