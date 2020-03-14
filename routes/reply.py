from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.mail import Mail
from routes import *

from models.reply import Reply
from utils.common import log

main = Blueprint('reply', __name__)


def users_from_content(content):
    # 不能解决 @在文本中间 比如 123@name abc，这样就不能获得name了
    parts = content.split(' ')
    users = []
    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            users.append(u)
    return users


def send_mails(sender, receivers, content, tid):
    for r in receivers:
        form = dict(
            title='{} AT 了你'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id,
            topic_id=tid,
        )
        m = Mail.new(form)
        log(m)


@main.route("/add", methods=["POST"])
def add():
    log('reply add')
    form = request.form
    u = current_user()

    # 发邮件
    log('before send mail', form)
    content = form['content']
    log('reply', content)
    users = users_from_content(content)
    log('reply', users)
    tid = form['topic_id']
    send_mails(u, users, content, tid)
    log('after send mail')
    m = Reply.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))
