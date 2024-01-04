from app import app, render_template, url_for


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')