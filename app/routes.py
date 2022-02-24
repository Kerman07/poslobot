import os
from flask import request, Response
from app import app
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import (
    ViberFailedRequest,
    ViberMessageRequest,
    ViberConversationStartedRequest,
    ViberSubscribedRequest,
    ViberUnsubscribedRequest,
)

from app.utils.scrape import get_jobs
from app import db
from app.models import User
from app.utils.texts import conversation_started, subscribed, categories


viber = Api(
    BotConfiguration(
        name="Poslobot",
        avatar="http://site.com/avatar.jpg",
        auth_token=os.environ.get("VIBER_AUTH"),
    )
)


@app.route("/", methods=["POST"])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(
        request.get_data(), request.headers.get("X-Viber-Content-Signature")
    ):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberSubscribedRequest):
        # check_user = User.query.filter_by(receiver=viber_request.sender.id).first()
        # if check_user:
        #     return Response(status=500)
        user = User(receiver=viber_request.sender.id)
        db.session.add(user)
        db.session.commit()
        viber.send_messages(viber_request.user.id, [subscribed])

    elif isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message.text
        if message == "Cat":
            viber.send_messages(viber_request.sender.id, categories)

    elif isinstance(viber_request, ViberUnsubscribedRequest):
        user = User.query.filter_by(receiver=viber_request.user_id).first()
        db.session.delete(user)
        db.session.commit()

    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(
            viber_request.user.id,
            [conversation_started],
        )

    elif isinstance(viber_request, ViberFailedRequest):
        logging.warn(
            "client failed receiving message. failure: {0}".format(viber_request)
        )

    return Response(status=200)


@app.route("/viber", methods=["GET"])
def send_jobs():
    users = User.query.all()
    for user in users:
        jobs = get_jobs(user.categories, user.location)
        msgs = []
        for position, company, link in jobs:
            message = f"{position}\n{link}\n{company}"
            msgs.append(TextMessage(text=message))
        viber.send_messages(user.receiver, msgs)
    return Response(status=200)
