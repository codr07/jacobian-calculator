from app import app

with app.test_client() as c:
    resp = c.post('/', data={'num_vars': '2', 'num_funcs': '2'})
    html = resp.get_data(as_text=True)
    print(html)
