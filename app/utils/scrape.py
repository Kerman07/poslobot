import scrapy


class JobSpider(scrapy.Spider):
    name = "jobs"

    def parse(self, response):
        jobs = response.css(".BF0HTNC-hg-l")
        for job in jobs:
            position = job.css("a::text").get()
            if position:
                whole_link = job.css("a::attr(href)").get().split(";")
                link = "https://www.mojposao.ba/" + whole_link[0] + ";" + whole_link[-1]
                hgc = job.css(".BF0HTNC-hg-c")
                company = hgc[-1].css("a::text").get()
                self.job_list.append([position, company, link])