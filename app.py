from flask import Flask, render_template, request
import sympy as sp
import numpy as np
from tabulate import tabulate

app = Flask(__name__)

# Common utility functions
def format_value(value):
    return f"{value:.6f}".rstrip('0').rstrip('.') if isinstance(value, (int, float)) else str(value)

# Bisection Method
@app.route('/bisection', methods=['GET', 'POST'])
def bisection():
    if request.method == 'POST':
        try:
            # Get inputs
            func_expr = request.form['function']
            tolerance = float(request.form['tolerance'])
            x_l = float(request.form['x_l'])
            x_u = float(request.form['x_u'])
            
            # Process function
            x = sp.Symbol('x')
            func = sp.lambdify(x, sp.sympify(func_expr), 'numpy')
            
            # Run bisection method
            results, root = bisection_method(func, x_l, x_u, tolerance)
            return render_template('bisection.html', 
                                 results=results,
                                 root=root,
                                 function=func_expr)
        except Exception as e:
            return render_template('bisection.html', error=str(e))
    return render_template('bisection.html')

# False Position Method
@app.route('/false_position', methods=['GET', 'POST'])
def false_position():
    if request.method == 'POST':
        try:
            # Similar structure as bisection
            # ... (implementation omitted for brevity)
            pass
        except Exception as e:
            return render_template('false_position.html', error=str(e))
    return render_template('false_position.html')

# Newton-Raphson Method
@app.route('/newton', methods=['GET', 'POST'])
def newton():
    if request.method == 'POST':
        try:
            # Similar structure as bisection
            # ... (implementation omitted for brevity)
            pass
        except Exception as e:
            return render_template('newton.html', error=str(e))
    return render_template('newton.html')

# Secant Method
@app.route('/secant', methods=['GET', 'POST'])
def secant():
    if request.method == 'POST':
        try:
            # Similar structure as bisection
            # ... (implementation omitted for brevity)
            pass
        except Exception as e:
            return render_template('secant.html', error=str(e))
    return render_template('secant.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
