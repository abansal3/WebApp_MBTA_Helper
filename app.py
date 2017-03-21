"""
Simple "Hello, World" application using Flask
"""

from flask import *
from mbta_helper import find_stop_near

app = Flask(__name__)

app.config['DEBUG'] = True


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place = request.form['location']
        place, distance = find_stop_near(place)

        if place and distance:
            return render_template('index.html', place=place, distance=distance)
        else:
            return render_template('index.html', error=True)
    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run()
