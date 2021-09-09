from GPSPhoto import gpsphoto


class ImageDetails:
    def __init__(self, image_path):
        self.image_path = image_path

    def get_image_details(self):
        # Get the data from image file and return a dictionary
        data = gpsphoto.getGPSData(self.image_path)
        return data
