import os
from flask import request, Response
from app import app, db, viber
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import (
    ViberFailedRequest,
    ViberMessageRequest,
    ViberConversationStartedRequest,
    ViberUnsubscribedRequest,
)

from app.models import User
from app.utils.texts import conversation_started, subscribed
from app.services.bot import message_handler, get_current_jobs


@app.route("/", methods=["POST"])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(
        request.get_data(), request.headers.get("X-Viber-Content-Signature")
    ):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message.text
        message_handler(viber_request, message)

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
    users = User.query.filter_by(daily=True)
    for user in users:
        get_current_jobs(user)
    return Response(status=200)
