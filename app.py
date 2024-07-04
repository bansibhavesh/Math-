from flask import Flask, request, render_template
from sympy import symbols, Eq, solve, parse_expr, SympifyError
from sympy.plotting import plot
import os
import re

# Set matplotlib backend to 'Agg' for non-GUI environment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

def parse_equation(equation_str):
    # Replace '^' with '**' for exponentiation
    equation_str = equation_str.replace('^', '**')
    return equation_str

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

        solution = solve(eq, x)

        if plot_graph:
            # Plot and save the graph
            p = plot(eq.lhs, (x, -10, 10), show=False)
            img_path = os.path.join('static', 'graph.png')
            p.save(img_path)
            graph_url = '/' + img_path  # Assuming static files are served from root

        else:
            graph_url = None

        return solution, graph_url

    except SympifyError as e:
        return f"Error parsing or solving equation: {e}", None

    except Exception as e:
        return f"Error solving equation: {e}", None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    graph_url = None
    if request.method == 'POST':
        equation_str = request.form.get('equation')
        plot_graph = 'plot_graph' in request.form
        result, graph_url = solve_equation(equation_str, plot_graph)
    return render_template('index.html', result=result, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
