from app import app, render_template, url_for, abort, redirect, request, session

from app import flow, google, requests, cachecontrol, id_token, GOOGLE_CLIENT_ID

from app import load_user, login_menager, login_user, logout_user, login_required, User, current_user


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["google_name"] = id_info.get("name")
    user1 = User(id_info.get("sub"), id_info.get("name"))
    login_user(user1)
    return redirect('/')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/")

@app.route('/profile')
@login_required
def profile():
    return f'Hello, {current_user.id}!'