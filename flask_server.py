from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

@app.route("/")
def home():
    config_width = 10
    config_speed = 5
    return render_template('equalizer.html', config_width=config_width, config_speed=config_speed)


def main():
    Bootstrap(app)
    app.run(host="0.0.0.0", port=8080)

main()
