from learning import app, engine
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('userid') and request.form.get('password'):
        userid = request.form.get('userid')
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session['userid'] = 1 # TODO :: fetch & store user object
            session.permanent = True  # use Cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            flash('Incorrect password.', 'danger')
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
    return render_template('index.html', topics=topics)


@app.route('/topic/new', methods=['GET', 'POST'])
@login_required
def newTopic():
    if request.method == 'POST':
        if request.form.get('topic'):
            db = DBSession(engine)
            fields = {
                'topic': request.form.get('topic'),
                'description': request.form.get('description')
            }
            db.create_or_update('Topic', fields)
            db.save()
            return redirect(url_for('index'))
    return render_template('topic_editor.html')


@app.route('/vote/<int:topic_id>/<user_vote>', methods=['POST'])
@login_required
def vote(topic_id, user_vote):
    db = DBSession(engine)
    vote = db.getMulti('Vote', {'topic':topic_id, 'voter':session.get('userid')})
    if len(vote):
        vote = dict((col, getattr(vote[0], col)) for col in vote[0].__table__.columns.keys())
    else:
        vote = {'topic':topic_id, 'voter':session.get('userid')}
    if user_vote == 'voteup':
        vote['voteup'] = 1
        vote['votedown'] = 0
    elif user_vote == 'votedown':
        vote['voteup'] = 0
        vote['votedown'] = 1
    db.create_or_update('Vote', vote)
    db.save()
    return ''
