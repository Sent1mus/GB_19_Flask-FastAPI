from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template('home.html')


@app.route('/clothes/')
def clothes():
    clothes_list = [
        {'title': 'Outerwear', 'description': 'description_01'},
        {'title': 'Home clothes', 'description': 'description_02'},
        {'title': 'Underwear', 'description': 'description_03'}
    ]
    return render_template('clothes.html', clothes_list=clothes_list)


@app.route('/clothes/<items>')
def clothes_items(items):
    return render_template('todo.html', clothes=clothes)


@app.route('/shoes/')
def shoes():
    shoes_list = [
        {'title': 'Sports shoes', 'description': 'description_01', },
        {'title': 'Winter shoes', 'description': 'description_02', },
        {'title': 'Summer shoes', 'description': 'description_03', }
    ]

    return render_template('shoes.html', shoes_list=shoes_list)


@app.route('/shoes/<items>')
def shoes_items(items):
    return render_template('todo.html', shoes=shoes)


if __name__ == '__main__':
    app.run(debug=True)
