
# FindAPool 

FindAPool is a module for detecting swimming pools in an image. 

## Installation

FindAPool requires a local distributions of python >= 3.6 and pip >= 9.0 in order to run. Either [anaconda](https://www.anaconda.com/download/) or [miniconda](https://conda.io/miniconda.html) distributions are recommended.

The use of a virtual environment, such as [conda](https://conda.io/docs/), is optional, but also recommended. If using anaconda or miniconda python distribution, this can be easily initiated set up using the commands:

`conda create -n FindAPool python=3.6`

`source activate FindAPool`

Once a suitable distribution of python is installed, download the FindAPool repository and run  

` pip install .`

## Running in the terminal

To run FindAPool from the command line :  

`FindAPool run`

By default the program will look for images in the 'data/' folder with the following h, s, v thresholds :

140 (h1) <= h <= 205 (h2)
s >= 20
v >= 65

The defaults can be modified ainsi : 

`FindAPool run --folder 'img_folder/' --h1 h1_value --h2 h2_value --s s_value --v v_value`
