from flask import Flask, render_template, request
from sympy import symbols, sympify, Matrix, latex as sympy_latex

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_vars = int(request.form.get("num_vars"))
        num_funcs = int(request.form.get("num_funcs"))

        # Provide a list of variable options (Latin a-z and common Greek names)
        latin = [chr(c) for c in range(ord('a'), ord('z')+1)]
        greek = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']

        variable_options = latin + greek + ['custom']

        return render_template("compute.html",
                               num_vars=num_vars,
                               num_funcs=num_funcs,
                               variable_options=variable_options)

    return render_template("index.html")


@app.route("/compute", methods=["POST"])
def compute():
    num_vars = int(request.form.get("num_vars"))
    num_funcs = int(request.form.get("num_funcs"))

    var_names = []
    functions = []

    # Gather variable names (handle select + custom inputs)
    for i in range(num_vars):
        choice = request.form.get(f"var_choice_{i}")
        if choice == 'custom':
            custom = request.form.get(f"var_custom_{i}") or f'x{i}'
            var_names.append(custom)
        else:
            # choice might be None if old form — fall back to var_i
            var_names.append(choice or request.form.get(f"var_{i}"))

    # Gather function expressions
    for j in range(num_funcs):
        functions.append(request.form.get(f"func_{j}"))


    # SymPy Computation
    variables = symbols(var_names)
    exprs = [sympify(f) for f in functions]

    J = Matrix(exprs).jacobian(variables)

    # Prepare outputs: string, latex, and HTML-friendly rows
    jacobian_str = str(J)
    jacobian_latex = sympy_latex(J)
    matrix_entries = [[str(J[i, j]) for j in range(J.cols)] for i in range(J.rows)]

    if num_vars == num_funcs:
        det = J.det()
        determinant_str = str(det)
        determinant_latex = sympy_latex(det)
    else:
        determinant_str = "Not square — no determinant"
        determinant_latex = "Not square — no determinant"

    # Provide variable options again for the template (for navigation back/forth)
    latin = [chr(c) for c in range(ord('a'), ord('z')+1)]
    greek = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']

    variable_options = latin + greek + ['custom']

    return render_template("compute.html",
                           num_vars=num_vars,
                           num_funcs=num_funcs,
                           var_names=var_names,
                           functions=functions,
                           jacobian=jacobian_str,
                           jacobian_latex=jacobian_latex,
                           matrix_entries=matrix_entries,
                           determinant=determinant_str,
                           determinant_latex=determinant_latex,
                           variable_options=variable_options)


if __name__ == "__main__":
    app.run(debug=True)
