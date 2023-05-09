"""
TEMPORARY WORKING CODE
"""
import numpy as np
import sympy as sp
import math
from scipy.optimize import minimize

# Sample numpy array of points
points = np.random.rand(1000,2)

bool_list = []
for i in range(0,np.shape(points)[0]):
    if points[i,1] - points[i,0] > 0:
        bool_list.append(True)
    else:
        bool_list.append(False)

x, y = sp.symbols("x y")

def line_equation(m, b):
    return y - m * x - b

def count_points_on_sides(m, b, points, bool_list):
    line_eq = line_equation(m, b)
    count = 0
    for i, point in enumerate(points):
        x_val, y_val = point
        point_on_line = line_eq.subs({x: x_val, y: y_val})

        if point_on_line > 0 and bool_list[i]:
            count -= 1
        elif point_on_line < 0 and not bool_list[i]:
            count -= 1
    return count

def objective_function(params, points, bool_list):
    m, b = params
    count = count_points_on_sides(m, b, points, bool_list)
    print("m: "+str(m),"b: "+str(b))
    return count

def optimize_line(points, bool_list):
    initial_guess = [0.0, 0.0]
    
    # Define the initial simplex with the desired step size
    step_size = 0.5
    initial_simplex = np.array([initial_guess, [initial_guess[0] + step_size, initial_guess[1]], [initial_guess[0], initial_guess[1] + step_size]])
    
    result = minimize(lambda p: objective_function(p, points, bool_list), initial_guess, method='Nelder-Mead', options={'maxiter': 5000, 'initial_simplex': initial_simplex})
    m_opt, b_opt = result.x
    return m_opt, b_opt


misclassification_threshold = 0.1  # Set your desired threshold
max_lines = 5  # Set the maximum number of lines allowed
current_points = points
current_bool_list = bool_list
lines = []

while len(lines) < max_lines:
    m, b = optimize_line(current_points, current_bool_list)
    count = count_points_on_sides(m, b, current_points, current_bool_list)
    misclassification_rate = 1 - abs(count) / len(current_points)

    if misclassification_rate <= misclassification_threshold:
        lines.append((m, b))
        break
    
    if len(lines) > 0 and math.isclose(m,lines[-1][0]) and math.isclose(b,lines[-1][1]):
        break

    lines.append((m, b))
    line_eq = line_equation(m,b)

    # Identify points on the wrong side of the line meant for points that fail
    wrong_points = []
    wrong_bool_list = []
    for i, (point, bool_value) in enumerate(zip(current_points, current_bool_list)):
        
        x_val, y_val = point
        point_on_line = line_eq.subs({x: x_val, y: y_val})
        
        if point_on_line < 0:
            wrong_points.append(point)
            wrong_bool_list.append(bool_value)

    current_points = np.array(wrong_points)
    current_bool_list = wrong_bool_list
    print("made it through once!")

print("Dividing lines:")
for m, b in lines:
    print(line_equation(m, b))

