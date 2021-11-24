from trello import TrelloApi
import json
from datetime import datetime
from image_details import ImageDetails
import requests


class BackofficeTrello:

    def __init__(self, image_path, image_details, suspected):
        self.image_path = image_path
        self.image_details = image_details
        data =""
        for tag in self.image_details.keys():
            data+= tag + ":" + str(self.image_details[tag]) + "\n"
        self.data =data
        self.TRELLO_APP_KEY = "502ad237349dafb0a9bf926baa9c8d60"  # your trello key
        self.TOKEN = "15228f4570a5dc117cfc1b860cccd4fcaa3a9cd36f8de8ba644ce4dccc6079b4"  # your api token
        self.listID = "6147170682c5603c6eee742d"  # the id for your list
        if suspected:
            self.listID = "618a7e09cbc1ff02e6ab3dd5"

        self.cardPos = "top"  #'top', 'bottom', or a number


    def open_trello_ticket(self):
        if "rishon_images" in self.image_path:
            url_to_image = "https://incontrol-sys.com/" + self.image_path
        else:
            url_to_image = "https://incontrol-sys.com/rishon_images/" + self.image_path

        trello = TrelloApi(self.TRELLO_APP_KEY, self.TOKEN)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        new_card = trello.cards.new("Dog Was found in " + dt_string, idList=self.listID, desc=self.data,
                                    pos=self.cardPos,
                                    urlSource=url_to_image)
        return new_card

    def add_attachment_to_ticket(self, attachment_file, card_id):
        params = (('key', self.TRELLO_APP_KEY), ('token', self.TOKEN),)
        files = {'file': (attachment_file, open(attachment_file, 'rb')), }
        response = requests.post('https://api.trello.com/1/cards/%s/attachments' % card_id, params=params, files=files)
        return response.text


#id = ImageDetails("AQADJLcxGzBWUFJ-.jpg")
#payload = id.get_full_image_details()
#bt = BackofficeTrello("dogsRishon.jpg", payload)
#card = bt.open_trello_ticket()
#file = 'outpy_1.mp4'
#bt.add_attachment_to_ticket(file, card['id'])
