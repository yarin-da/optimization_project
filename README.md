# Optimization Project

## Setup

The script wasn't tested for Python2, therefore we recommend that you use Python3.

To run this script you need to first install these packages:

* Numpy 
    
    `python3 -m pip install numpy`

* Scipy 

    `python3 -m pip install scipy`

* Matplotlib 

    `python3 -m pip install matplotlib`

***

After you have all the dependencies, run the script.

For example:
```bash
    python3 opt.py dims=10 alg=interior-point problem=klee-minty maxiter=1024 epochs=1 image_folder=.
```

Options:
```
alg: interior-point, simplex

problem: klee-minty, random

maxiter: positive integer

epochs: positive integer

image_folder: folder path
```

You may enter a partial number of arguments (arguments that aren't passed to the script will get a default value).

You may also enter the arguments in any arbitrary order you like.

***

## Contributors

* [Ronli Vignanski](https://github.com/RonliVignanski)
* [Yarin Dado](https://github.com/yarin-da)