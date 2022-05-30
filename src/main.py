import matplotlib.pyplot as plt
import numpy as np
from sympy import solve_poly_system
from sympy.abc import x


import random


def f(x):
    return 1.25 * x ** 3 - 1.5 * x ** 2 + 1.75 * x + 1


def plot_function(x, a, b):
    y = list(map(f, x))
    plt.plot(x, y)
    plt.title("F(x)")
    plt.show()
    plt.savefig(str(a) + "_" + str(b) + ".png")


def det_maximum(x_array):
   return max([f(x) for x in x_array])


def det_minimum(x_array):
   return min([f(x) for x in x_array])

def extract_random_points(a, b, number_of_points, extreme_f):
    under_f_points = 0
    for i in range(number_of_points):
        x = random.uniform(a, b)
        if extreme_f >= 0.0:
            y = random.uniform(0.0, extreme_f)
            if 0.0 <= y <= f(x):
                under_f_points += 1
        if extreme_f <= 0.0:
            y = random.uniform(extreme_f, 0.0)
            if f(x) <= y <= 0.0:
                under_f_points += 1

    return under_f_points / number_of_points


def plot_simulations_histogram(simulations_integral_values, val):
    plt.hist(simulations_integral_values, bins=100)
    plt.show()
    plt.savefig(str(val)+".png")


solutions = solve_poly_system([1.25 * x ** 3 - 1.5 * x ** 2 + 1.75 * x + 1, 0.0], x)

def main():
    number_of_simulations = 100
    a = -5.0
    b = 5.0
    number_of_points = 100000
    x = np.linspace(a, b, number_of_points)
    plot_function(x, a, b)

    A, B = a, b

    global solutions

    real_solutions = []

    real_solutions.append(A)

    for solution in solutions:
        converted = None
        is_real = False
        try:
            converted = float(solution[0])
            if converted:
                if isinstance(converted, float):
                    is_real = True
        except:
            continue
        if is_real and converted and A <= converted <= B:
            real_solutions.append(converted)

    real_solutions.append(B)

    print("Real solutions list: ", real_solutions)

    if 0.0 not in real_solutions:
        for i in range(len(real_solutions)-1):
            if real_solutions[i] < 0.0 < real_solutions[i+1]:
                real_solutions.insert(i + 1, 0.0)

    print("After adding 0.0", real_solutions)
    integrals_sum = 0.0

    for j in range(len(real_solutions) - 1):
        simulations_integral_values = []

        a = real_solutions[j]
        b = real_solutions[j + 1]
        print("Interval: ", a, b)
        x = np.linspace(a, b, number_of_points)

        maximum_f = det_maximum(x)
        minimum_f = det_minimum(x)

        print("Maximum point of function f on the interval [" + str(
            a) + "," + str(b) + "] is " + str(maximum_f))

        print("Minimum point of function f on the interval [" + str(
            a) + "," + str(
            b) + "] is " + str(minimum_f))

        for i in range(number_of_simulations):
            if i % 50 == 0:
                print("Simulation ", i)
            if 0.0 <= a <= b:
                rectangle_area = abs(maximum_f) * abs(float(b - a))

                points_ratio = extract_random_points(a, b, number_of_points, maximum_f)
                simulations_integral_values.append(points_ratio * rectangle_area)
            elif a <= 0.0 <= b:
                first_half_points_ratio = extract_random_points(a, 0.0, number_of_points,
                                                     minimum_f)
                first_rectangle_area = abs(minimum_f) * abs(float(a))

                second_half_points_ratio = extract_random_points(0.0, b, number_of_points,
                                                     maximum_f)
                second_rectangle_area = abs(maximum_f) * abs(float(b))

                simulations_integral_values.append(second_rectangle_area * second_half_points_ratio -
                                                   first_half_points_ratio * first_rectangle_area  )
            elif a <= b <= 0.0:
                rectangle_area = abs(minimum_f) * abs(float(b - a))
                points_ratio = extract_random_points(a, b, number_of_points,
                                                     minimum_f)
                simulations_integral_values.append((-1) * points_ratio * rectangle_area)

        print("Integral of function f for points ", a, b)
        print("After " + str(number_of_simulations) + " simulations")
        print("and " + str(number_of_points) + " points drawn")
        print("Equals to ", sum(simulations_integral_values)/len(simulations_integral_values))
        integrals_sum += sum(simulations_integral_values)/len(simulations_integral_values)
        plot_simulations_histogram(simulations_integral_values, sum(simulations_integral_values)/len(simulations_integral_values))

    print("Integral of function f for points ", A, B)
    print("After " + str(number_of_simulations) + " simulations")
    print("and " + str(number_of_points * (len(real_solutions) -1) ) + " points drawn")
    print("Equals to ", integrals_sum)


if __name__=='__main__':
    main()