import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, interpolate
from scipy.interpolate import splrep, splev


DEFAULT_MAX_DIMS = 6
iterations = 0


def create_random_problem(dims, min_val=0, max_val=1000):
    A = []
    for i in range(dims):
        A.append(random.sample(range(min_val, max_val), dims))
    b = random.sample(range(min_val, max_val), dims)
    objective = random.sample(range(min_val, max_val), dims)
    return A, b, objective


def create_klee_minty_problem(dims):
    A = []
    for i in range(dims):
        row = [0] * dims
        for j in range(i + 1):
            coefficient = 2 ** (i - j + 1)
            if coefficient == 2:
                coefficient = 1
            row[j] = coefficient
        A.append(row)
    
    dims_range = list(range(dims))
    b = list(map(lambda x: 5 ** (x + 1), dims_range))
    objective = list(map(lambda x: -2 ** (dims - x - 1), dims_range))
    return A, b, objective


def create_problem(problem_type, dims):
    if problem_type == 'klee-minty':
        return create_klee_minty_problem(dims)
    return create_random_problem(dims)
    

def callback(res):
    global iterations
    iterations += 1


def run_simplex(dims, problem_type, alg_type, maxiter):
    global iterations
    iterations = 0
    A, b, objective = create_problem(problem_type, dims)
    return optimize.linprog(objective, method=alg_type, A_ub=A, b_ub=b, callback=callback, options={ 'maxiter': maxiter })
    
    
def plot(x_data, y_data, max_dims, alg_type, problem_type):
    x = np.array(x_data)
    y = np.array(y_data)
    x_new = np.linspace(1, max_dims - 1, max_dims * 100)
    a_BSpline = interpolate.make_interp_spline(x, y)
    y_new = a_BSpline(x_new)
    
    plt.xlabel('dimensions', fontdict={ 'weight': 'bold' })
    plt.ylabel('iterations', fontdict={ 'weight': 'bold' })
    plt.title(f'{alg_type} {problem_type}', fontdict={ 'weight': 'bold' })
    plt.xticks(list(range(1, max_dims)))
    plt.plot(x_new, y_new)
    plt.savefig(f'./images/{alg_type}_{problem_type}_{max_dims}.png')
    plt.show()
    
    
def main():
    global iterations
    max_dims = int(sys.argv[1]) + 1
    alg_type = sys.argv[2]
    problem_type = sys.argv[3] # interior-point / simplex
    maxiter = int(sys.argv[4]) # TODO: make optional
    epochs = int(sys.argv[5])
    
    plot_data = []
    dim_range = list(range(1, max_dims))
    for dim in dim_range:
        sum_of_iterations = 0
        for _ in range(epochs):
            res = run_simplex(dim, problem_type, alg_type, maxiter)
            sum_of_iterations += iterations
            if not res.success:
                print('simplex failed', res.message)
                sys.exit(-1)
        plot_data.append(sum_of_iterations / epochs)
    plot(dim_range, plot_data, max_dims, alg_type, problem_type)
    

if __name__ == '__main__':
    main()