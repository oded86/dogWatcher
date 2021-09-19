from GPSPhoto import gpsphoto


class ImageDetails:
    def __init__(self, image_path):
        self.image_path = image_path

    def get_image_details(self):
        # Get the data from image file and return a dictionary
        try:
            data = gpsphoto.getGPSData(self.image_path)
        except:
            photo = gpsphoto.GPSPhoto()
            photo = gpsphoto.GPSPhoto(self.image_path)
            info = photo.GPSInfo(34.8061518, 31.9633645)
            photo.modGPSData(info, self.image_path)
            data = photo.getGPSData(self.image_path)

        return data
