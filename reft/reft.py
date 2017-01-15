import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from rel_extract import rel_extract;    


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , reft.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'C:\\Users\\ephra\\git\\reft\\reft\\reft.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('REFT_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        print('no sqlite_db attr')
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


#TODO not ideal, get the initial CLI to work
with app.app_context():
    print("This should work")
    init_db()

@app.cli.command('initdb')
def initdb_command():
    print('Initializing the database.')
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


        
@app.route('/')
def show_entities():
    db          = get_db()
    cur         = db.execute('select subject, object from relation_entities order by id desc')
    entities    = cur.fetchall()
    print('entities from db: ' + str(len(entities)))
    return render_template('show_entities.html', entities=entities)


@app.route('/add', methods=['POST'])
def add_entry():
    db          = get_db()
    entities    = rel_extract.findrelations(request.form['text'])
    for ent in entities:
        db.execute('insert into relation_entities (subject, object, relation_type_id)  select ?, ?, id from relation_type where subject=? and object=?', 
                   [ent.subj, ent.obj, ent.subj_type, ent.obj_type])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entities'))