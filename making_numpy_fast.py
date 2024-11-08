
# %%
import numpy.ma as ma
import numpy as np
import time

# set up the random seed
np.random.seed(42)
# and values to do calculations with later
arr = np.random.rand(1000000)

# %% Timing Code Execution
# Using time.time
start_time = time.time()
# Example operation
mean_val = np.mean(arr)
end_time = time.time()
print(f"Time taken using time.time: {end_time - start_time} seconds")

# Using %timeit times a single line of code
%timeit np.mean(arr)

# Using %%timeit times the whole cell
# %%timeit
# mean_val = np.mean(arr)

# %% Preallocating Memory


def really_inefficient(N):
    result = np.array([])
    for i in range(N):
        result = np.append(result, i)


def inefficient(N):
    result = []
    for i in range(N):
        result.append(i)
    result = np.array(result)


def efficient(N):
    result = np.zeros(N)
    for i in range(N):
        result[i] = i


N = 1_000_000
%timeit really_inefficient(N)
%timeit inefficient(N)
%timeit efficient(N)

# %% Use NumPy's Built-in Functions


def custom_sum(arr):
    # Inefficient
    total = 0
    for val in arr:
        total += val
    return total


# Efficient
total = np.sum(arr)

arr = np.random.rand(1000000)
%timeit custom_sum(arr)
%timeit np.sum(arr)


# %% Efficient Array Indexing
# Example: Compute the mean of values greater than 0.8
arr = np.random.rand(1000000)
filtered_arr = arr[arr > 0.8]
mean_filtered = np.mean(filtered_arr)
print(f"Mean of values greater than 0.8: {mean_filtered}")

# Using Masked Arrays

# Create a masked array
masked_arr = ma.masked_array(arr, mask=arr <= 0.8)
mean_masked = masked_arr.mean()
print(f"Mean of masked array (values > 0.8): {mean_masked}")

# %% Using np.newaxis to Avoid For Loops
# Example: Adding a 1D array to each row of a 2D array


def newaxis_inefficient(arr_2d, arr_1d):
    result_loop = np.zeros_like(arr_2d)
    for i in range(arr_2d.shape[0]):
        result_loop[i, :] = arr_2d[i, :] + arr_1d
    return result_loop


arr_2d = np.random.rand(50, 30)
arr_1d = np.random.rand(30)

# Inefficient way using for loop
%timeit newaxis_inefficient(arr_2d, arr_1d)

# Efficient way using np.newaxis
%timeit arr_2d + arr_1d[np.newaxis, :]

# %% Using np.newaxis to Avoid For Loops
# Example: Creating multiple NFW profiles at once


def nfw_profile(r, rho0, rs):
    return rho0 / ((r/rs) * (1 + r/rs)**2)


def nfw_inefficient(r, rho0, rs):
    result_loop = np.zeros((r.size, rho0.size))
    for i in range(rho0.size):
        result_loop[:, 0] = nfw_profile(r, rho0[i], rs[i])
    return result_loop


# Create a 1D array of radii
r = np.linspace(0.1, 10, 1000)  # in kpc

# Create a 1D array of (unrealistic) NFW parameters
rho0 = np.random.rand(100)  # in Msun / kpc^3
rs = np.random.rand(100)*20 + 10  # in kpc

# Inefficient way using for loop
%timeit nfw_inefficient(r, rho0, rs)

# Efficient way using np.newaxis
%timeit nfw_profile(r[:, np.newaxis], rho0, rs)

# %% Using np.einsum for Efficient Operations
# Note for the simple examples given below inbuilt functions outperform einsum,
# however for more complex operations einsum can be more efficient
# %% Example: Matrix Multiplication

# Create two random matrices
matrix1 = np.random.rand(100, 200)
matrix2 = np.random.rand(200, 100)


def matrix_mult_loop(A, B):
    result = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                result[i, j] += A[i, k] * B[k, j]
    return result


# Inefficient way using nested loops
%timeit matrix_mult_loop(matrix1, matrix2)
# Efficient way using np.dot
%timeit np.dot(matrix1, matrix2)
# Efficient way using np.einsum
%timeit np.einsum('ik,kj->ij', matrix1, matrix2)

# %% Example: Outer Product

# Create two random vectors
vector1 = np.random.rand(1000)
vector2 = np.random.rand(1000)


def outer_product_loop(a, b):
    result = np.zeros((a.size, b.size))
    for i in range(a.size):
        for j in range(b.size):
            result[i, j] = a[i] * b[j]
    return result


# Inefficient way using nested loops
%timeit outer_product_loop(vector1, vector2)
# Efficient way using np.outer
%timeit np.outer(vector1, vector2)
# Efficient way using np.einsum
%timeit np.einsum('i,j->ij', vector1, vector2)
