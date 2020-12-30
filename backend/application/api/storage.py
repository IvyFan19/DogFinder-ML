from google.cloud import storage


class Storage(object):

    bucket = "project3-294022.appspot.com"

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket)

    def save(self, entity_id, file):
        blob = self.bucket.blob(entity_id)
        blob.upload_from_string(
            file.read(),
            #content_type=file.content_type
            content_type="image/jpeg"
        )
        blob.make_public()
        return 'https://storage.googleapis.com/project3-294022.appspot.com/'+entity_id

    def get(self, id):
        blob = self.bucket.blob(id)
        blob.download_as_bytes(id)

    def delete(self, id):
        blob = self.bucket.blob(id)
        blob.delete()