from app import app

with app.test_client() as c:
    data = {
        'num_vars': '2',
        'num_funcs': '2',
        'var_choice_0': 'x',
        'var_choice_1': 'y',
        'func_0': 'x**2 + y',
        'func_1': 'sin(x) + y'
    }
    resp = c.post('/compute', data=data)
    html = resp.get_data(as_text=True)
    # print only portions around Jacobian/Determinant
    start = html.find('Jacobian Matrix (plain):')
    print(html[start:start+1000])
