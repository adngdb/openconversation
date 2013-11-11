import datetime
import flask
import httplib2
import simplejson as json
import urllib
import uuid
from functools import wraps

import openconversation as oc
import settings

app = flask.Flask(__name__)
app.config.from_object('settings')
http = httplib2.Http()


def authenticated(f):
    """Check if user is logged in"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not get_user_email():
            return flask.redirect(flask.url_for('index'))
        return f(*args, **kwargs)
    return decorated


def isadministrator(f):
    """Check if user is an admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = oc.User(get_user_email())
        if not user.isadmin:
            return flask.redirect(flask.url_for('index'))
        return f(*args, **kwargs)
    return decorated


def get_user_email():
    return flask.session.get('%s_email' % settings.PREFIX)


def json_encode(data):
    for key, item in data.items():
        if isinstance(item, (datetime.date, datetime.datetime)):
            data[key] = item.isoformat()
    return json.dumps(data)


#------------------------------------------------------------------------------
# Views entry points
#------------------------------------------------------------------------------
@app.route('/')
def index():
    billets = oc.Billets().get()
    return flask.render_template('index.html', billets=billets)


@app.route('/write')
def write():
    return flask.render_template('write.html')


@app.route('/admin/')
@authenticated
@isadministrator
def admin():
    return flask.render_template('admin.html')


#------------------------------------------------------------------------------
# Application entry points
#------------------------------------------------------------------------------
@app.route('/billet/<billet_id>', methods=['GET'])
def get_billet(billet_id):
    billet = oc.Billet(billet_id)
    origin = None
    answers = []

    if flask.request.headers.get('content-type') == 'application/json':
        data = billet.get()
        data['billet_id'] = '%s%s' % (
            flask.request.host_url[:-1],  # URL without the trailing slash
            flask.url_for('get_billet', billet_id=data['billet_id'])
        )
        return json_encode(data)

    if billet.answer_to:
        # Get the billet this answers to
        origin = oc.Billet(billet.answer_to)

    if billet.answers:
        for answer_id in billet.answers:
            answers.append(oc.Billet(answer_id))

    return flask.render_template(
        'billet.html',
        billet=billet,
        origin=origin,
        answers=answers
    )


@app.route('/billet/<billet_id>', methods=['POST'])
def add_answer_to_billet(billet_id):
    billet = oc.Billet(billet_id)

    answer_id = flask.request.form.get('answer_id')

    if not billet.answers:
        billet.answers = [answer_id]
    else:
        billet.answers.append(answer_id)

    billet.save()
    return flask.make_response(('', 200, []))


@app.route('/billet', methods=['POST'])
@authenticated
def create_billet():
    billet = oc.Billet()

    billet.billet_id = str(uuid.uuid4())
    billet.content = flask.request.form.get('billet_content')
    billet.title = flask.request.form.get('billet_title')
    billet.tags = flask.request.form.get('billet_tags')
    billet.author = get_user_email()
    billet.date_created = datetime.datetime.utcnow()
    billet.answer_to = flask.request.form.get('billet_answer_to')
    billet.answers = []

    billet.save()

    if billet.answer_to:
        origin_billet = oc.Billet(billet.answer_to)
        origin_billet.add_answer(billet.billet_id)

    return flask.redirect(
        flask.url_for('get_billet', billet_id=billet.billet_id)
    )


#------------------------------------------------------------------------------
# Login entry points
#------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    bid_fields = {
        'assertion': flask.request.form['assertion'],
        'audience': flask.request.host_url
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    }
    http.disable_ssl_certificate_validation = True
    resp, content = http.request(
        'https://login.persona.org/verify',
        'POST',
        body=urllib.urlencode(bid_fields),
        headers=headers
    )
    bid_data = json.loads(content)

    if bid_data['status'] == 'okay' and bid_data['email']:
        flask.session['%s_email' % settings.PREFIX] = bid_data['email']
    else:
        print bid_data

    return flask.url_for('index')


@app.route('/logout')
def logout():
    if '%s_email' % settings.PREFIX in flask.session:
        flask.session.pop('%s_email' % settings.PREFIX, None)
    return flask.redirect(flask.url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
