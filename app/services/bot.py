import crochet
from app import db, viber, crawl_runner
from app.models import User
from viberbot.api.messages.text_message import TextMessage
from threading import Thread
from app.utils.texts import (
    categories,
    categories_list,
    categories_present,
    commands,
    location,
    subscribed,
)
from app.utils.scrape import JobSpider
from app.utils.dictionary import mapping


def message_handler(viber_request, message):
    user = User.query.filter_by(receiver=viber_request.sender.id).first()

    if message == "Start":
        user = User(receiver=viber_request.sender.id)
        db.session.add(user)
        viber.send_messages(viber_request.sender.id, [subscribed])

    elif message == "Cat":
        if user.categories:
            viber.send_messages(
                viber_request.sender.id,
                [categories_present, categories_list],
            )
        else:
            viber.send_messages(viber_request.sender.id, [categories, categories_list])

    elif message.startswith("Cat a"):
        to_add = message.split()[-1]
        if to_add in user.categories.split("_"):
            return
        if not user.categories:
            user.categories = to_add
        else:
            user.categories += "_" + to_add

    elif message.startswith("Cat d"):
        to_delete = message.split()[-1]
        user.categories = "_".join(
            cat for cat in user.categories.split("_") if cat != to_delete
        )

    elif message.startswith("Cat"):
        cats = message.split()[1].replace(".", "_")
        user.categories = cats
        cat_mapping = "\n".join(f"- {mapping[en]}" for en in cats.split("_"))
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(text=f"Vaše izabrane kategorije su:\n{cat_mapping}"),
        )

    elif message == "Jobs":
        t = Thread(
            target=get_current_jobs,
            args=([user.categories, user.location, user.receiver],),
        )
        t.start()

    elif message == "Loc":
        viber.send_messages(viber_request.sender.id, location)

    elif message.startswith("Loc"):
        loc = message.split()[1]
        user.location = loc
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(text="Uspješno ste promijenili lokaciju."),
        )

    elif message == "End":
        user.daily = False
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(
                text="Nećete primati dnevne obavijesti.\nDa bi ponovo počeli primati obavijesti pošaljite Begin."
            ),
        )

    elif message == "Begin":
        user.daily = True
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(text="Ponovo ćete primati dnevne obavijesti."),
        )

    elif message == "Status":
        if user.categories:
            cat_mapping = "\n".join(
                f"- {mapping[en]}" for en in user.categories.split("_")
            )
            viber.send_messages(
                viber_request.sender.id,
                TextMessage(text=f"Vaše izabrane kategorije su:\n{cat_mapping}\n"),
            )
        else:
            viber.send_messages(
                viber_request.sender.id,
                TextMessage(text=f"Niste izabrali kategorije.\n"),
            )
        if user.location:
            viber.send_messages(
                viber_request.sender.id,
                TextMessage(text=f"Vaša lokacija je: {user.location}"),
            )
        else:
            viber.send_messages(
                viber_request.sender.id, TextMessage(text=f"Niste izabrali lokaciju.\n")
            )
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(
                text=f"Primanje dnevnih obavijesti: " + ("Da" if user.daily else "Ne")
            ),
        )

    elif message == "Help":
        viber.send_messages(viber_request.sender.id, commands)

    db.session.commit()


def get_current_jobs(user_obj):
    categories, location, receiver = user_obj
    scrape_with_crochet(categories, location, receiver)


@crochet.run_in_reactor
def scrape_with_crochet(categories, location, receiver):
    crawl_runner.crawl(
        JobSpider,
        start_urls=[
            f"https://www.mojposao.ba/#!searchjobs;keyword=;page=1;title=all;range=today;location=all;i={categories};lk={location}"
        ],
        receiver=receiver,
    )
