from app import db, viber
from app.models import User
from viberbot.api.messages.text_message import TextMessage
from app.utils.texts import (
    categories,
    categories_list,
    categories_present,
    commands,
    location,
)
from app.utils.scrape import get_jobs


def message_handler(viber_request, message):
    user = User.query.filter_by(receiver=viber_request.sender.id).first()

    if message == "Cat":
        if user.categories:
            viber.send_messages(
                viber_request.sender.id,
                [
                    TextMessage(
                        text=f"Vaše trenutno izabrane kategorije su: {user.categories.replace('_', '.')}\n"
                    ),
                    categories_present,
                    categories_list,
                ],
            )
        else:
            viber.send_messages(viber_request.sender.id, [categories, categories_list])
    elif message.startswith("Cat a"):
        to_add = message.split()[-1]
        if to_add in user.categories:
            return
        if not user.categories:
            user.categories = to_add
        else:
            user.categories += "_" + to_add
    elif message.startswith("Cat d"):
        to_delete = message.split()[-1]
        if "_" + to_delete in user.categories:
            user.categories = user.categories.replace("_" + to_delete, "")
        elif to_delete + "_" in user.categories:
            user.categories = user.categories.replace(to_delete + "_", "")
        elif to_delete in user.categories:
            user.categories = ""
    elif message.startswith("Cat"):
        cats = message.split()[1].replace(".", "_")
        user.categories = cats
    elif message == "Jobs":
        get_current_jobs(user)
    elif message == "Loc":
        viber.send_messages(viber_request.sender.id, location)
    elif message.startswith("Loc"):
        loc = message.split()[1]
        user.location = loc
    elif message == "Help":
        viber.send_messages(viber_request.sender.id, commands)

    db.session.commit()


def get_current_jobs(user):
    jobs = get_jobs(user.categories, user.location)
    msgs = []
    for position, company, link in jobs:
        message = f"{position}\n{link}\n{company}"
        msgs.append(TextMessage(text=message))
    viber.send_messages(user.receiver, msgs)
