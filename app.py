from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/manual_search.html')
def manual_search():
    return render_template('manual_search.html')


if __name__ == '__main__':
    app.run()
