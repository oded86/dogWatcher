from trello import TrelloApi
import json

class Backoffice_trello:

    def __init__(self, image_path, image_details):
        self.image_path = image_path
        self.image_details = image_details
        self.TRELLO_APP_KEY = "502ad237349dafb0a9bf926baa9c8d60"  # your trello key
        self.TOKEN = "15228f4570a5dc117cfc1b860cccd4fcaa3a9cd36f8de8ba644ce4dccc6079b4"  # your api token
        self.listID = "6147170682c5603c6eee742d"  # the id for your list
        self.cardPos = "top"  #'top', 'bottom', or a number

    def open_trello_ticket(self):
        if "rishon_images" in self.image_path:
            url_to_image ="https://incontrol-sys.com/"+ self.image_path
        else:
            url_to_image ="https://incontrol-sys.com/rishon_images/"+ self.image_path

        trello = TrelloApi(self.TRELLO_APP_KEY, self.TOKEN)
        new_card = trello.cards.new("Dog Was found", idList=self.listID, desc=self.image_details, pos=self.cardPos,
                                    urlSource=url_to_image )
        return new_card

#payload = {"lat": "36.860361000000005", "long": "-79.273586", "url": "rishon_images/pats_us2.jpg"}
#url = "pats_us2.jpg"
#bt = Backoffice_trello(url, json.dumps(payload))
#print(bt.open_trello_ticket())