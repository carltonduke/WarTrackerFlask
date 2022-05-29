import views
from helpers import LazyView
from flask import Flask, render_template

app = Flask(__name__)

app.add_url_rule('/', view_func=LazyView('views.index'))
app.add_url_rule('/warlog/', methods = ['POST','GET'], view_func=LazyView('views.warlogInput'))
app.add_url_rule('/clan', view_func=LazyView('views.clan'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)