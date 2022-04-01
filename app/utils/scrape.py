import scrapy
from app import viber
from viberbot.api.messages.text_message import TextMessage


class JobSpider(scrapy.Spider):
    name = "jobs"

    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
    }

    def parse(self, response):
        jobs = response.css(".BF0HTNC-hg-l")
        msgs = []
        for job in jobs:
            position = job.css("a::text").get()
            if position:
                whole_link = job.css("a::attr(href)").get().split(";")
                link = "https://www.mojposao.ba/" + whole_link[0] + ";" + whole_link[-1]
                hgc = job.css(".BF0HTNC-hg-c")
                company = hgc[-1].css("a::text").get()
                message = f"{position}\n{link}\n{company}"
                msgs.append(TextMessage(text=message))
        if msgs:
            viber.send_messages(self.receiver, msgs)
        else:
            viber.send_messages(
                "SVDRnk/HlrP/FI/66iUW1w==",
                TextMessage(
                    text="Danas nije bilo objavljenih poslova sa vašim kriterijumima."
                ),
            )
