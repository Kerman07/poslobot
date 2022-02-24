from app import db, viber
from app.models import User
from viberbot.api.messages.text_message import TextMessage
from app.utils.texts import categories
from app.utils.scrape import get_jobs

def message_handler(viber_request, message):
    user = User.query.filter_by(receiver=viber_request.sender.id).first()

    if message == "Cat":
        viber.send_messages(viber_request.sender.id, categories)
    elif message.startswith("Cat"):
        cats = message.split()[1].replace(".", "_")
        user.categories = cats
        db.session.commit()
    elif message == "Jobs":
        get_current_jobs(user)

def get_current_jobs(user):
    jobs = get_jobs(user.categories, user.location)
    msgs = []
    for position, company, link in jobs:
        message = f"{position}\n{link}\n{company}"
        msgs.append(TextMessage(text=message))
    viber.send_messages(user.receiver, msgs)