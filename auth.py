import functools
from flask import (Blueprint, flash, g, render_template, request, url_for, session, redirect)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute('SELECT id FROM usuarios WHERE username = %s', (username,))
        
        if not username:
            error = 'username es requerido'
        if not password:
            error = 'password es requerido'
        elif c.fetchone() is not None:
            error = f'usuario {username} ya está registrado'
            
        if error is None:
            c.execute(
                'INSERT INTO usuarios(username, password) VALUES(%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = c.fetchone()
        
        if user is None:
            error = "Usuario y/o contrasena invalida"
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contrasena invalida'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']  # Asegúrate de almacenar el id en 'user_id'
            return redirect(url_for('todo.index'))  # Redirige a la página de todos
            
        flash(error)
        
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')  # Usa 'user_id', no 'id'
    
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))  # Corregido el SQL aquí
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))  # Redirige a la página de login después de cerrar sesión
