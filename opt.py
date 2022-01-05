import os
import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, interpolate


# global variable that stores the number of iterations of scipy.optimize 
iterations = 0


# creates a problem with random parameters in range [min_val, max_val]
def create_random_problem(dims, min_val=0, max_val=1000):
    A = []
    for _ in range(dims):
        A.append(random.sample(range(min_val, max_val), dims))
    b = random.sample(range(min_val, max_val), dims)
    objective = random.sample(range(min_val, max_val), dims)
    return A, b, objective


# creates a problem with Klee-Minty parameters
def create_klee_minty_problem(dims, scaling=False):
    scalar = 2**dims if scaling else 1
    A = []
    for i in range(dims):
        row = [0] * dims
        for j in range(i + 1):
            coefficient = 2 ** (i - j + 1)
            if coefficient == 2:
                coefficient = 1
            row[j] = coefficient * scalar
        A.append(row)
    
    dims_range = list(range(dims))
    b = list(map(lambda x: scalar * 5 ** (x + 1), dims_range))
    objective = list(map(lambda x: scalar * -2 ** (dims - x - 1), dims_range))

    return A, b, objective


def create_problem(problem_type, dims, scaling):
    if problem_type == 'klee-minty':
        return create_klee_minty_problem(dims, scaling)
    return create_random_problem(dims)
    

# function that we pass to scipy.optimize in order to count the number of iterations
def callback(res):
    global iterations
    iterations += 1


# runs a chosen algorithm with a chosen problem and predefined maximum number of iterations
def run_algorithm(dims, problem_type, alg_type, maxiter, scaling):
    global iterations
    iterations = 0
    # A, b are the constraints and objective contains the coefficients for the objective function
    A, b, objective = create_problem(problem_type, dims, scaling)
    return optimize.linprog(objective, method=alg_type, A_ub=A, b_ub=b, callback=callback, options={ 'maxiter': maxiter })


# utility function that plots all the data in a graph
def plot(x_data, y_data, max_dims, alg_type, problem_type, scaling, image_folder):
    x = np.array(x_data)
    y = np.array(y_data)
    # make a smoother graph
    x_new = np.linspace(1, max_dims, max_dims * 100)
    a_BSpline = interpolate.make_interp_spline(x, y)
    y_new = a_BSpline(x_new)
    
    plt.xlabel('dimensions', fontdict={ 'weight': 'bold' })
    plt.ylabel('iterations', fontdict={ 'weight': 'bold' })
    plt.title(f'{alg_type} {problem_type} {"scaled" if scaling else ""}', fontdict={ 'weight': 'bold' })
    plt.xticks(list(range(1, max_dims + 1)))
    plt.plot(x_new, y_new, color='red')
    
    file_path = os.path.join(image_folder, f'{alg_type}_{problem_type}_{max_dims}_{"scaled" if scaling else ""}.png')
    plt.savefig(file_path)
    plt.show()
    

# this function allows the user to enter partial number of arguments 
# with an arbitrary order
def get_arguments():
    # default argument values
    params = {
        'dims': 10,
        'alg': 'simplex',
        'problem': 'klee-minty',
        'maxiter': 2**11,
        'epochs': 1,
        'scaling': False,
        'image_folder': '.',
    }
    # set arguments according to user input
    for arg in sys.argv[1:]:
        arg_type, arg_val = arg.split('=', 1)
        params[arg_type] = arg_val
    
    return params


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False

    
def main():
    global iterations
    
    params = get_arguments()
    max_dims = int(params['dims'])
    alg_type = params['alg']
    problem_type = params['problem']
    maxiter = int(params['maxiter'])
    epochs = int(params['epochs'])
    image_folder = params['image_folder']
    scaling = str_to_bool(params['scaling'])
    
    plot_data = []
    # run through every dimension from 1 to max_dims
    dim_range = list(range(1, max_dims + 1))
    for dim in dim_range:
        # run for a number of epochs for each dimension (in order to get an average number of iterations)
        sum_of_iterations = 0
        for _ in range(epochs):
            res = run_algorithm(dim, problem_type, alg_type, maxiter, scaling)
            sum_of_iterations += iterations
            # print(res)
            # print(iterations)
            # incase scipy fails - display the error and finish
            if not res.success:
                print('simplex failed', res.message)
                sys.exit(-1)
        plot_data.append(sum_of_iterations / epochs)
    plot(dim_range, plot_data, max_dims, alg_type, problem_type, scaling, image_folder)
    

if __name__ == '__main__':
    main()