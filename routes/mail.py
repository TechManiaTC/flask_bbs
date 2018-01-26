from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.mail import Mail

main = Blueprint('mail', __name__)


@main.route("/add/", methods=["POST"])
def add():
    form = request.form
    print('mail form', form)
    receiver = User.one(username=form['receiver_user'])
    print('receiver_user', receiver)
    receiver_id = receiver.id
    u = current_user()
    Mail.new(form, sender_id=u.id, sender_user=u.username, receiver_id=receiver_id)
    return redirect(url_for(".index"))


@main.route("/new")
def new():
    u = current_user()
    token = new_csrf_token()
    return render_template("mail/new.html", token=token, user=u)


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    if u is not None:
        send_mail = Mail.all(sender_id=u.id)
        received_mail = Mail.all(receiver_id=u.id)
        t = render_template(
            "mail/index.html",
            sends=send_mail,
            receives=received_mail,
            user=u,
            # topic=topic,
        )
    else:
        abort(401)
    return t


@main.route("/view/<string:id>")
def view(id):
    u = current_user()
    mail = Mail.one(id=id)
    if current_user().id in [mail.receiver_id, mail.sender_id]:
    # if current_user().id == mail.receiver_id and current_user().id == mail.sender_id:
        return render_template("mail/detail.html", mail=mail, user=u)
    else:
        return redirect(url_for(".index"))
