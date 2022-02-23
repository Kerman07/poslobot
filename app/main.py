from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from app.selen import get_jobs

app = Flask(__name__)
viber = Api(
    BotConfiguration(
        name="PythonSampleBot",
        avatar="http://site.com/avatar.jpg",
        auth_token="4ec6da36b227dc6f-cfe43ef1fe4c9487-2930ff0d897e15ca",
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

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        jobs = get_jobs()
        msgs = []
        for posao, poslodavac, link in jobs:
            message = f"{posao}\n{link}\n{poslodavac}"
            msgs.append(TextMessage(text=message))
        viber.send_messages(viber_request.sender.id, msgs)
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(
            viber_request.get_user.id, [TextMessage(text="thanks for subscribing!")]
        )
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warn(
            "client failed receiving message. failure: {0}".format(viber_request)
        )

    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, debug=True)
