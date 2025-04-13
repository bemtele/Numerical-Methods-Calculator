from flask import Flask, render_template, request
import sympy as sp
import numpy as np

app = Flask(__name__)

def find_valid_bounds(func, x_l, x_u, tolerance):
    valid_bounds = []
    for lower in range(int(x_l), int(x_u)):
        for upper in range(lower + 1, int(x_u) + 1):
            if func(lower) * func(upper) < 0:
                iterations = int(np.ceil(np.log2((upper - lower) / (tolerance / 100))))
                valid_bounds.append((lower, upper, func(lower), func(upper), iterations))
    return valid_bounds

def bisection_method(func, initial_x_l, initial_x_u, tolerance_percent):
    x_l, x_u = initial_x_l, initial_x_u
    iteration = 1
    error = float('inf')
    prev_midpoint = None
    results = []

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
            'error': error if prev_midpoint else None,
            'f_midpoint': f_midpoint
        })

        prev_midpoint = midpoint
        iteration += 1

    return results, midpoint

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user inputs
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            x_l = float(request.form['x_l'])
            x_u = float(request.form['x_u'])

            # Process function
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')

            # Find valid bounds
            valid_bounds = find_valid_bounds(func, x_l, x_u, tolerance)
            if not valid_bounds:
                return render_template('index.html', 
                                    error="No valid bounds found in the given range.")

            # Get selected bounds (using first valid pair for simplicity)
            selected_lower, selected_upper = valid_bounds[0][:2]

            # Run bisection method
            results, root = bisection_method(func, selected_lower, selected_upper, tolerance)

            return render_template('index.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr,
                                 valid_bounds=valid_bounds)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
