from moderator import app, engine
from flask import render_template, session, redirect, url_for, request, flash
from DBSession import DBSession
import functools


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner


def isadmin():
    return session.get('user')['isadmin']


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('userid') and request.form.get('password'):
        userid = request.form.get('userid')
        password = request.form.get('password')
        db = DBSession(engine)
        user_details = db.get('User', {'userid': userid})
        if user_details:
            if password == user_details['password']:
                session['logged_in'] = True
                session['user'] = user_details
                session.permanent = False  # use Cookie to store session. (or not!?)
                flash('You are now logged in.', 'success')
                return redirect(next_url or url_for('index'))
            else:
                flash('Incorrect password.', 'danger')
    else:
        flash('Incorrect UserId or Password.', 'danger')
    return render_template('login.html', next_url=next_url)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/')
def index():
    db = DBSession(engine)
    topics = db.getMulti('Topic')
    for topic in topics:
        topic['likes'] = 0
        votes = db.getMulti('Vote', {'topic': topic['id']})
        for vote in votes:
            topic['likes'] += vote['like']
    return render_template('index.html', topics=topics)


@app.route('/topic/new', methods=['GET', 'POST'])
@login_required
def newTopic():
    if request.method == 'POST':
        if request.form.get('topic'):
            db = DBSession(engine)
            fields = {
                'topic': request.form.get('topic'),
                'description': request.form.get('description'),
                'createdby': session.get('user')['id']
            }
            db.create_or_update('Topic', fields)
            db.save()
            return redirect(url_for('index'))
    return render_template('topic_editor.html')


@app.route('/like/<int:topic_id>', methods=['POST'])
@login_required
def like(topic_id):
    db = DBSession(engine)
    vote = db.getMulti('Vote', {'topic': topic_id, 'voter': session.get('user')['id']})
    if len(vote):
        vote = vote[0]
    else:
        vote = {'topic': topic_id, 'voter': session.get('user')['id']}
    if vote.get('like', 0) == 1:
        vote['like'] = 0
    else:
        vote['like'] = 1
    db.create_or_update('Vote', vote)
    db.save()
    return redirect(url_for('index'))


@app.route('/user', methods=['GET'])
@login_required
def list_users():
    if isadmin():
        db = DBSession(engine)
        users = db.getMulti('User')
        return render_template('users.html', users=users)
    return redirect(url_for('index'))


@app.route('/user/new', methods=['GET', 'POST'])
@login_required
def create_user():
    if isadmin():
        if request.method == 'POST':
            pass
        return render_template('user_editor.html', user={})
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def modify_user(user_id):
    db = DBSession(engine)
    user = db.get('User', {'id': user_id})
    if request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        if isadmin():
            pass
    return render_template('user_editor.html', user=user)
