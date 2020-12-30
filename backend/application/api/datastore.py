from google.cloud import datastore


class Datastore(object):

    KEY = 'DOG'

    def __init__(self):
        self.client = datastore.Client()

    def create(self, post_id, location='', contact='', post_type=''):
        try:
            task_key = self.client.key(self.KEY, post_id)
            task = datastore.Entity(key=task_key)
            task['post_id'] = post_id
            task['location'] = location.lower()
            task['contact'] = contact.lower()
            task['post_type'] = post_type.lower()
            self.client.put(task)
            return {'status': 'success', 'post_id': post_id}
        except:
            return {'status': 'failure', 'reason': 'unknown error occurred'}

    def update(self, post_id, image_id=False, image_url=False, location=False, contact=False, breed=False, post_type=False, tags=False):
        try:
            task_key = self.client.key(self.KEY, post_id)
            task = self.client.get(key=task_key)
            if image_id:
                task['image_id'] = image_id
            if image_url:
                task['image_url'] = image_url
            if location:
                task['location'] = location.lower()
            if contact:
                task['contact'] = contact.lower()
            if breed:
                task['breed'] = breed.lower()
            if post_type:
                task['post_type'] = post_type.lower()
            if tags:
                task['tags'] = tags
            self.client.put(task)
            return {'status' : 'success', 'post_id' : post_id}
        except:
            return {'status' : 'failure', 'reason': 'no entity found'}

    def read_one(self, post_id):
        query = self.client.query(kind=self.KEY)
        query.add_filter('post_id', '=', post_id)
        result = list(query.fetch())
        return {
            'status': 'success',
            'result': result
        }

    def read_many(self, term=''):
        query_loc = self.client.query(kind=self.KEY)
        query_bre = self.client.query(kind=self.KEY)
        query_typ = self.client.query(kind=self.KEY)

        if term != '':
            query_loc.add_filter('location', '=', term.lower())
            query_bre.add_filter('breed', '=', term.lower())
            query_typ.add_filter('post_type', '=', term.lower())
        else:
            return {
                'status': 'success',
                'result': list(query_loc.fetch())
            }
        loc_res = list(query_loc.fetch())
        loc_bre = list(query_bre.fetch())
        loc_typ = list(query_typ.fetch())
        return {
            'status': 'success',
            'result': loc_res + loc_bre + loc_typ
        }
        

    def delete(self, post_id=''):
        task_key = self.client.key(self.KEY, post_id)
        self.client.delete(key=task_key)