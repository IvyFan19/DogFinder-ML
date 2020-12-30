from google.cloud import vision


class Vision(object):

    breed_list = [
        'german sheperd',
        'american pit',
        'bull terrier',
        'yorkshire terrier',
        'west highland terrier',
        'american pit bull terrier',
        'beagle',
        'cardigan welsh corgi',
        'appenzeller sennenhund',
        'entlebucher mountain dog',
        'italian greyhound',
        'ibizan hound',
        'german spitz',
        'german spitz mittel',
        'german spitz klein',
        'spitz',
        'russell terrier',
        'alaskan malamute',
        'sakhalin husky',
        'golden retriever',
        'nova scotia duck tolling retriever',
        'terrier',
        'yorkshire terrier',
        'morkie',
        'shibainu',
        'australian shepherd',
        'Australian Terrier',
        'basenji',
        'bichon frise',
        'bloodhound',
        'boston terrier',
        'boxer',
        'chihuahua',
        'dachshund',
        'french bulldog',
        'great dane',
        'pug'
    ]

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def get_tags(self, path):
        tags = []
        image = vision.types.Image()
        image.source.image_uri = path
        response = self.client.label_detection(image=image)
        for label in response.label_annotations:
            tags.append(label.description.lower())
        return tags

    def get_breed(self, tags):
        for label in tags:
            if label in self.breed_list:
                return label
        return 'unknown'