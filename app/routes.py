from app import app


@app.route('/')
@app.route('/shop')
def shop():
    return 'All products'
