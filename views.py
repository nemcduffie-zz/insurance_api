from run import app


@app.route('/hello')
def hello() -> str:
    return 'Hello world!'
