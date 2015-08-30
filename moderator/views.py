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


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('userid') and request.form.get('password'):
        userid = request.form.get('userid')
        password = request.form.get('password')
        db = DBSession(engine)
        user_details = db.get('User', {'userid' : userid})
        if user_details:
            if password == user_details['password']:
                session['logged_in'] = True
                session['userid'] = user_details['id']
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
        topic['voteup'] = 0
        topic['votedown'] = 0
        votes = db.getMulti('Vote', {'topic' : topic['id']})
        for vote in votes:
            topic['voteup'] += vote['voteup']
            topic['votedown'] += vote['votedown']
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
                'createdby': session.get('userid')
            }
            db.create_or_update('Topic', fields)
            db.save()
            return redirect(url_for('index'))
    return render_template('topic_editor.html')


@app.route('/vote/<int:topic_id>/<user_vote>', methods=['POST'])
@login_required
def vote(topic_id, user_vote):
    db = DBSession(engine)
    vote = db.getMulti('Vote', {'topic': topic_id, 'voter': session.get('userid')})
    if len(vote):
        vote = vote[0]
    else:
        vote = {'topic': topic_id, 'voter': session.get('userid')}
    if user_vote == 'voteup':
        vote['voteup'] = 1
        vote['votedown'] = 0
    elif user_vote == 'votedown':
        vote['voteup'] = 0
        vote['votedown'] = 1
    db.create_or_update('Vote', vote)
    db.save()
    return redirect(url_for('index'))
