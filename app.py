from flask import Flask, render_template, request
import sympy as sp
import numpy as np
from tabulate import tabulate

app = Flask(__name__)

# Common utility function
def format_value(value):
    """Format the number to remove unnecessary trailing zeros."""
    return f"{value:.6f}".rstrip('0').rstrip('.') if isinstance(value, (int, float)) else str(value)

# Bisection Method Implementation
def bisection_method(func, x_l, x_u, tolerance_percent):
    results = []
    iteration = 1
    error = float('inf')
    prev_midpoint = None

    while error > tolerance_percent:
        midpoint = (x_l + x_u) / 2
        f_midpoint = func(midpoint)

        if func(x_l) * f_midpoint < 0:
            x_u = midpoint
        else:
            x_l = midpoint

        if prev_midpoint is not None:
            error = abs((midpoint - prev_midpoint) / midpoint) * 100

        results.append({
            'iteration': iteration,
            'x_l': x_l,
            'x_u': x_u,
            'midpoint': midpoint,
            'error': error if prev_midpoint is not None else None,
            'f_midpoint': f_midpoint
        })

        prev_midpoint = midpoint
        iteration += 1

    return results, midpoint

# False Position Method Implementation
def false_position_method(func, x_l, x_u, tolerance_percent):
    results = []
    iteration = 1
    error = float('inf')
    prev_xr = None

    while error > tolerance_percent:
        f_xl = func(x_l)
        f_xu = func(x_u)
        
        # False-Position formula
        xr = (x_u * f_xl - x_l * f_xu) / (f_xl - f_xu)
        f_xr = func(xr)

        if f_xl * f_xr < 0:
            x_u = xr
        else:
            x_l = xr

        if prev_xr is not None:
            error = abs((xr - prev_xr) / xr) * 100

        results.append({
            'iteration': iteration,
            'x_l': x_l,
            'x_u': x_u,
            'xr': xr,
            'error': error if prev_xr is not None else None,
            'f_xr': f_xr
        })

        prev_xr = xr
        iteration += 1

    return results, xr

# Newton-Raphson Method Implementation
def newton_raphson_method(func, func_prime, initial_guess, tolerance_percent):
    results = []
    x_n = initial_guess
    iteration = 1
    error = float('inf')
    prev_x_n = None

    while error > tolerance_percent:
        f_x_n = func(x_n)
        f_prime_x_n = func_prime(x_n)

        if f_prime_x_n == 0:
            break  # Avoid division by zero

        x_n_plus_1 = x_n - f_x_n / f_prime_x_n

        if prev_x_n is not None:
            error = abs((x_n_plus_1 - prev_x_n) / x_n_plus_1) * 100

        results.append({
            'iteration': iteration,
            'x_n': x_n,
            'f_x_n': f_x_n,
            'f_prime_x_n': f_prime_x_n,
            'error': error if prev_x_n is not None else None
        })

        prev_x_n = x_n_plus_1
        x_n = x_n_plus_1
        iteration += 1

    return results, x_n

# Secant Method Implementation
def secant_method(func, x0, x1, tolerance_percent):
    results = []
    iteration = 1
    error = float('inf')
    prev_x1 = None

    while error > tolerance_percent:
        f_x0 = func(x0)
        f_x1 = func(x1)

        if f_x0 == f_x1:
            break  # Avoid division by zero

        x2 = x1 - (f_x1 * (x1 - x0)) / (f_x1 - f_x0)
        f_x2 = func(x2)

        if prev_x1 is not None:
            error = abs((x2 - prev_x1) / x2) * 100

        results.append({
            'iteration': iteration,
            'x0': x0,
            'x1': x1,
            'x2': x2,
            'error': error if prev_x1 is not None else None,
            'f_x2': f_x2
        })

        x0, x1 = x1, x2
        prev_x1 = x2
        iteration += 1

    return results, x2

# Route for Bisection Method
@app.route('/bisection', methods=['GET', 'POST'])
def bisection_route():
    if request.method == 'POST':
        try:
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            x_l = float(request.form['x_l'])
            x_u = float(request.form['x_u'])
            
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')
            
            results, root = bisection_method(func, x_l, x_u, tolerance)
            return render_template('bisection.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr)
        except Exception as e:
            return render_template('bisection.html', error=str(e))
    return render_template('bisection.html')

# Route for False Position Method
@app.route('/false_position', methods=['GET', 'POST'])
def false_position_route():
    if request.method == 'POST':
        try:
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            x_l = float(request.form['x_l'])
            x_u = float(request.form['x_u'])
            
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')
            
            results, root = false_position_method(func, x_l, x_u, tolerance)
            return render_template('false_position.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr)
        except Exception as e:
            return render_template('false_position.html', error=str(e))
    return render_template('false_position.html')

# Route for Newton-Raphson Method
@app.route('/newton', methods=['GET', 'POST'])
def newton_route():
    if request.method == 'POST':
        try:
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            initial_guess = float(request.form['initial_guess'])
            
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')
            func_prime = sp.lambdify(x, sp.diff(sp.sympify(func_expr), x), 'numpy')
            
            results, root = newton_raphson_method(func, func_prime, initial_guess, tolerance)
            return render_template('newton.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr)
        except Exception as e:
            return render_template('newton.html', error=str(e))
    return render_template('newton.html')

# Route for Secant Method
@app.route('/secant', methods=['GET', 'POST'])
def secant_route():
    if request.method == 'POST':
        try:
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            x0 = float(request.form['x0'])
            x1 = float(request.form['x1'])
            
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')
            
            results, root = secant_method(func, x0, x1, tolerance)
            return render_template('secant.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr)
        except Exception as e:
            return render_template('secant.html', error=str(e))
    return render_template('secant.html')

# Homepage Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
