from ast import parse
from time import sleep
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from collections import Counter
import json



class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        urls = ['https://www.crous-amiens.fr/restaurant/restaurant-dunilasalle-amiens/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        counter=0
        numberDay=0
        # stock question and answer in a list
        plats = []
        platsWithDay = []
        date=Selector(response).xpath("//*[@id='menu-repas']")
        main_dishes=Selector(response).xpath("//*[@class='liste-plats']")
        print("date",date)
        for quote in date:
            plats.append({
                'date':quote.xpath('.//h3/text()').extract(),
            })
        for quote in main_dishes:
            contenu=quote.xpath('.//li/text()').extract()
            # if contenu had a no value, we skip it
            if contenu:
                counter+=1
                plats.append({
                    'main_dishes':contenu,
                })
        for i in plats:
            for a in i:
                if a == 'date':
                    numberDay=len(i[a])
        if numberDay == counter:
            for i in plats:
                for a in i:
                    if a == 'date':
                        #loop with number of main_dishes index date in plats
                        for index in range(0,numberDay):
                            platsWithDay.append({
                                'date':i[a][index],
                                'main_dishes':', '.join(plats[1+index]['main_dishes']),
                                'number_of_dishes':len(plats[1+index]['main_dishes']),
                            })
        else:
            print("error, no matching with days and dishes")
            sleep(5)
            #recall the function to try again
            self.parse(response)

        dump = "["+",".join([json.dumps(obj) for obj in platsWithDay ])+"]" 
        # send list of platsWithDay to file json
        #add dict to json file with open('file.json', 'w') as f:
        
        with open('/home/alexadmin/dev/botTelegram/CrousBot/plats.json', 'w') as outfile:
            outfile.write(dump)
        #with open('/var/www/application/messengerSend/datas.json', 'w') as outfile:
        #    for a in platsWithDay:
        #        json.dump(dump, outfile)
           

        page = response.url.split("/")[-2]
    
       


