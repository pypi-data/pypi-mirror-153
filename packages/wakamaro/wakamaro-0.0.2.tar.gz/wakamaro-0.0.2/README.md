# wakamaro

A package for visualizing the number of waka poetry composed by poets in Nijuichidaishu"

Using a Nijuichidaishu dataset, Visualize the number of waka poetry per waka poet.

The Nijuichidaishu dataset is downloadable from:
http://codh.rois.ac.jp/pmjt/


## Overview of Data
- the Center for Open Data in the Humanities
- “The Dataset of Pre-Modern Japanese Text (the National Institute of Japanese Literature)
- http://codh.rois.ac.jp/index.html.en

Data Licensing
- CC BY-SA

Link to download data
- http://codh.rois.ac.jp/pmjt/package/text.zip


## How to run wakamaro
The first argument: Number of Nijuichidaishu
The second argument: Minimum number of appearances of the waka poets to be displayed

Example of Running: waka poets that appeared more than 5 times in kokin wakashu
$ wakamaro 1 5