from flask import Flask, render_template, request
from sympy import symbols, sympify, Matrix

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_vars = int(request.form.get("num_vars"))
        num_funcs = int(request.form.get("num_funcs"))

        return render_template("compute.html",
                               num_vars=num_vars,
                               num_funcs=num_funcs)

    return render_template("index.html")


@app.route("/compute", methods=["POST"])
def compute():
    num_vars = int(request.form.get("num_vars"))
    num_funcs = int(request.form.get("num_funcs"))

    var_names = []
    functions = []

    # Gather variable names
    for i in range(num_vars):
        var_names.append(request.form.get(f"var_{i}"))

    # Gather function expressions
    for j in range(num_funcs):
        functions.append(request.form.get(f"func_{j}"))

    # SymPy Computation
    variables = symbols(var_names)
    exprs = [sympify(f) for f in functions]

    J = Matrix(exprs).jacobian(variables)
    determinant = str(J.det()) if num_vars == num_funcs else "Not square — no determinant"

    return render_template("compute.html",
                           num_vars=num_vars,
                           num_funcs=num_funcs,
                           var_names=var_names,
                           functions=functions,
                           jacobian=str(J),
                           determinant=determinant)


if __name__ == "__main__":
    app.run(debug=True)
