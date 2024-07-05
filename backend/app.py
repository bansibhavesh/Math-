from flask import Flask, request, render_template
from sympy import symbols, Eq, solve, parse_expr, SympifyError
from sympy.plotting import plot
import matplotlib.pyplot as plt
import os
import re  # Import the re module for regex operations

# Set the backend to 'Agg' for non-GUI rendering
plt.switch_backend('Agg')

app = Flask(__name__)

def parse_equation(equation_str):
    # Replace '^' with '**' and handle spaces around operators
    equation_str = equation_str.replace('^', '**').replace(' ', '')
    return equation_str

def identify_equation_type(equation_str):
    if any(func in equation_str for func in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc']):
        return 'trigonometric'
    elif any(func in equation_str for func in ['exp']):
        return 'exponential'
    elif 'log' in equation_str:
        return 'logarithmic'
    elif any(char in equation_str for char in ['<', '>', '<=', '>=']):
        return 'inequality'
    elif equation_str.count('=') > 1:
        return 'system'
    elif re.search(r'\b(x|y|z)\b', equation_str):
        highest_power = max([int(match.group(2)) if match.group(2) else 1 for match in re.finditer(r'([xyz])(\d*)', equation_str)])
        if highest_power == 1:
            return 'linear'
        elif highest_power == 2:
            return 'quadratic'
        elif highest_power == 3:
            return 'cubic'
    return 'linear'

def solve_equation(equation_str, plot_graph=False):
    x = symbols('x')
    try:
        equation_str = parse_equation(equation_str)
        parsed_eq = parse_expr(equation_str)
        if '==' in equation_str:
            left_side, right_side = equation_str.split('==')
            eq = Eq(parse_expr(left_side), parse_expr(right_side))
        else:
            eq = Eq(parsed_eq, 0)

        # Solve the equation
        solution = solve(eq, x)

        # Plot graph if required
        if plot_graph:
            if not os.path.exists('static'):
                os.makedirs('static')
            p = plot(eq.lhs, (x, -10, 10), show=False)
            p.save(os.path.join('static', 'graph.png'))

        return solution

    except SympifyError as e:
        return f"Error parsing or solving equation: {e}"

    except Exception as e:
        return f"Error solving equation: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    graph = None
    if request.method == 'POST':
        equation_str = request.form.get('equation')
        plot_graph = 'plot_graph' in request.form
        result = solve_equation(equation_str, plot_graph)
        if plot_graph:
            graph = True
    return render_template('index.html', result=result, graph=graph)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
