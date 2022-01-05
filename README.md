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
    python3 opt.py dims=10 alg=interior-point problem=klee-minty maxiter=1024 epochs=1 scaling=False image_folder=.
```

Options:
```
alg: interior-point, simplex

problem: klee-minty, random

maxiter: positive integer

epochs: positive integer

scaling: boolean [True, False]

image_folder: folder path
```

You may enter a partial number of arguments (arguments that aren't passed to the script will get a default value).

You may also enter the arguments in any arbitrary order you like.

***

## Sample Images

We provided a folder of plot images that we created using our script.

`images/simplex_klee-minty_13.png` was created using: 
```
python3 opt.py dims=13 maxiter=65536 problem=klee-minty alg=simplex image_folder=./images epochs=1
```
`images/simplex_random_13.png` was created using: 
```
python3 opt.py dims=13 maxiter=65536 problem=random alg=simplex image_folder=./images epochs=150
```
`images/interior-point_klee-minty_13.png` was created using: 
```
python3 opt.py dims=13 maxiter=65536 problem=klee-minty alg=interior-point image_folder=./images epochs=1
```
`images/interior-point_random_13.png` was created using: 
```
python3 opt.py dims=13 maxiter=65536 problem=random alg=interior-point image_folder=./images epochs=150
```

***

## Contributors

* [Ronli Vignanski](https://github.com/RonliVignanski)
* [Yarin Dado](https://github.com/yarin-da)