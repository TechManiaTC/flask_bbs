from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    abort,
    flash,
)
from werkzeug.utils import secure_filename

from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
import os
import uuid

from routes import current_user, new_csrf_token
from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    board_id = request.args.get('board_id', 'all')
    if board_id == 'all':
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    if not u:
        return render_template("index.html", ms=ms, bs=bs, bid=board_id)
    else:
        return redirect(url_for('topic.index'))


@main.route("/login")
def login():
    return render_template("login.html")


@main.route('/login/confirm', methods=['POST'])
def login_confirm():
    form = request.form
    u = User.validate_login(form)
    print('login u', u)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('index.login'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        print('login', session)
        # 设置 cookie 有效期为 永久
        session.permanent = False
        return redirect(url_for('topic.index'))


@main.route('/signout')
def signout():
    if 'user_id' in session:
        session.pop('user_id')
        return redirect(url_for('index.index'))
    else:
        abort(401)


@main.route("/register")
def register():
    return render_template("register.html")


@main.route("/register/confirm", methods=['POST'])
def register_confirm():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    flash('注册成功')
    return redirect(url_for('index.login'))


@main.route("/setting")
def setting():
    u = current_user()
    return render_template("setting.html", user=u)


@main.route("/profile/edit", methods=['POST'])
def edit_profile():
    u = current_user()
    form = request.form
    User.update(id=u.id, form=form)
    return redirect(url_for('.setting'))


@main.route("/password/edit", methods=['POST'])
def edit_password():
    u = current_user()
    form = request.form
    old_pass = User.salted_password(form['old_pass'])
    if old_pass == u.password:
        new_pass = User.salted_password(form['new_pass'])
        User.update(u.id, dict(
            password=new_pass
        ))
    return redirect(url_for('.setting'))


@main.route('/profile')
def profile():
    u = current_user()
    topics = Topic.all(user_id=u.id)
    replys = Reply.all(user_id=u.id)
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u, topics=topics, replys=replys)


@main.route('/user/<id>')
def user_detail(id):
    u = User.one(id=id)
    topics = Topic.all(user_id=u.id)
    replys = Reply.all(user_id=u.id)
    if u is None:
        os.abort(404)
    else:
        return render_template('profile.html', user=u, topics=topics, replys=replys)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    # file 是一个上传的文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        # filename = secure_filename(file.filename)
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        print('avatar path', os.path.join('user_image', filename))
        file.save(os.path.join('user_image', filename))
        u = current_user()
        User.update(u.id, dict(
            user_image='/uploads/{}'.format(filename)
        ))

    return redirect(url_for(".profile"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)
