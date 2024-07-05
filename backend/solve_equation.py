from sympy import symbols, Eq, solve, parse_expr, simplify, SympifyError
from sympy.plotting import plot
import matplotlib.pyplot as plt
import re
import time

def parse_equation(equation_str):
    equation_str = equation_str.replace('^', '**')
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
        print("\nStep 1: Parse the equation")
        equation_str = parse_equation(equation_str)
        parsed_eq = parse_expr(equation_str)
        print(f"Parsed Equation: {parsed_eq}")

        if '==' in equation_str:
            left_side, right_side = equation_str.split('==')
            eq = Eq(parse_expr(left_side), parse_expr(right_side))
        else:
            eq = Eq(parsed_eq, 0)

        print("\nStep 2: Set the equation to zero if necessary")
        eq = Eq(eq.lhs - eq.rhs, 0)
        print(f"Equation set to zero: {eq}")

        print("Cook'n up...")
        time.sleep(2)  # Simulate loading

        print("\nStep 3: Solve the equation")

        # Check if the equation simplifies to a known identity
        simplified_eq = simplify(eq)
        if simplified_eq == True:
            print("The equation is a trigonometric identity.")
            print("It holds true for all values of x.")
            return None  # Return None to indicate no finite solution

        # Solve the equation
        solution = solve(eq, x)
        print(f"Solution: {solution}")

        print("Cooked.")

        if plot_graph:
            print("\nPlotting the equation (optional)")
            plot(eq.lhs, (x, -10, 10))

        return solution

    except SympifyError as e:
        print(f"Error parsing or solving equation: {e}")
        print("Please check your input equation for syntax errors or unsupported operators.")
        return None

    except Exception as e:
        print(f"Error solving equation: {e}")
        return None

def solve_system_of_equations(eq_strs, plot_graph=False):
    variables = symbols(' '.join(f'x{i}' for i in range(1, len(eq_strs) + 1)))
    try:
        eqs = [parse_expr(parse_equation(eq_str)) for eq_str in eq_strs]
        eqs = [Eq(eq, 0) for eq in eqs]

        print("Cook'n up...")
        time.sleep(2)  # Simulate loading

        solution = solve(eqs, variables)
        print("Cooked.")
        return solution

    except SympifyError as e:
        print(f"Error parsing system of equations: {e}")
        print("Please check your input equations for syntax errors or unsupported operators.")
        return None

    except Exception as e:
        print(f"Error solving system of equations: {e}")
        return None

def solve_inequality(inequality_str, plot_graph=False):
    x = symbols('x')
    try:
        print("\nStep 1: Parse the inequality")
        inequality_str = parse_equation(inequality_str)
        parsed_ineq = parse_expr(inequality_str)
        print(f"Parsed Inequality: {parsed_ineq}")

        print("Cook'n up...")
        time.sleep(2)  # Simulate loading

        print("\nStep 2: Solve the inequality")
        solution = solve(parsed_ineq, x)
        print(f"Solution: {solution}")

        print("Cooked.")

        return solution

    except SympifyError as e:
        print(f"Error parsing inequality: {e}")
        print("Please check your input inequality for syntax errors or unsupported operators.")
        return None

    except Exception as e:
        print(f"Error solving inequality: {e}")
        return None

def detailed_quadratic_solution(equation_str, plot_graph=False):
    x = symbols('x')
    try:
        equation_str = parse_equation(equation_str)
        if '==' in equation_str:
            left_side, right_side = equation_str.split('==')
            eq = Eq(parse_expr(left_side), parse_expr(right_side))
        else:
            eq = Eq(parse_expr(equation_str), 0)
        
        eq = Eq(eq.lhs - eq.rhs, 0)
        simplified_eq = simplify(eq)
        
        a, b, c = [simplified_eq.lhs.as_poly().coeff_monomial(x**i) for i in range(2, -1, -1)]

        print("\nStep-by-step solution for quadratic equation:")
        print(f"Given quadratic equation: {simplified_eq}")
        print(f"Coefficients: a = {a}, b = {b}, c = {c}")
        print("Using the quadratic formula: x = (-b ± √(b²-4ac)) / 2a")
        
        discriminant = b**2 - 4*a*c
        print(f"Discriminant (b² - 4ac): {discriminant}")

        if discriminant < 0:
            print("The equation has no real solutions.")
            return None

        print("Cook'n up...")
        time.sleep(2)  # Simulate loading

        sol1 = (-b + discriminant**0.5) / (2*a)
        sol2 = (-b - discriminant**0.5) / (2*a)
        
        print("Cooked.")
        print(f"Solutions: x1 = {sol1}, x2 = {sol2}")

        if plot_graph:
            print("\nPlotting the equation (optional)")
            plot(eq.lhs, (x, -10, 10), title="Quadratic Equation Plot")
            plt.show()

        return [sol1, sol2]

    except SympifyError as e:
        print(f"Error parsing or solving quadratic equation: {e}")
        print("Please check your input equation for syntax errors or unsupported operators.")
        return None

    except Exception as e:
        print(f"Error solving quadratic equation: {e}")
        return None

if __name__ == "__main__":
    print("Welcome to the A-level and IGCSE Mathematics equation solver!")
    print("Enter 'quit' to exit.")

    while True:
        equation_str = input("\nEnter an equation to solve (or type 'quit' to exit): ").strip()
        if equation_str.lower() == 'quit':
            break

        plot_graph = input("Would you like to see the graph of the equation? (yes/no): ").strip().lower() == 'yes'

        equation_type = identify_equation_type(equation_str)
        print(f"Identified Equation Type: {equation_type}")

        if equation_type == 'system':
            num_eqs = int(input("Enter the number of equations in the system: "))
            eq_strs = [input(f"Enter equation {i+1}: ") for i in range(num_eqs)]
            result = solve_system_of_equations(eq_strs, plot_graph)

        elif equation_type == 'quadratic':
            detailed_quadratic_solution(equation_str, plot_graph)
            result = solve_equation(equation_str, plot_graph)

        elif equation_type == 'inequality':
            result = solve_inequality(equation_str, plot_graph)

        else:
            result = solve_equation(equation_str, plot_graph)

        if result is not None:
            print(f"\nThe solution is: {result}")
        else:
            print("\nUnable to solve the equation. Please check your input and try again.")
