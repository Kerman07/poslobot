import scrapy
from app import viber
from viberbot.api.messages.text_message import TextMessage


class JobSpider(scrapy.Spider):
    name = "jobs"

    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
    }

    def parse(self, response):
        jobs = response.css(".DVIXVVB-hg-k")
        msgs = []
        for job in jobs:
            info_div = job.css(".DVIXVVB-hg-l")
            job_id = info_div.css("a::attr(href)").get().split(";")[-1]
            link = "https://www.mojposao.ba/#!job;" + job_id
            position = info_div.css("a::text").get()
            company = info_div.css(".DVIXVVB-hg-c *::text").getall()[-1]
            message = f"{position}\n{link}\n{company}"
            msgs.append(TextMessage(text=message))
        if msgs:
            viber.send_messages(self.receiver, msgs)
        else:
            viber.send_messages(
                self.receiver,
                TextMessage(
                    text="Danas nije bilo objavljenih poslova sa vašim kriterijumima."
                ),
            )
