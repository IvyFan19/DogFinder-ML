from application import app
from flask import request, jsonify
import uuid

from application.api.datastore import Datastore
from application.api.storage import Storage
from application.api.vision import Vision

datastore = Datastore()
storage = Storage()
vision = Vision()


@app.route('/api/posts/create', methods=['POST'])
def create_post():
    # create id
    post_id = str(uuid.uuid4())
    # get post data
    data = request.json
    # save data to datastore
    ret = datastore.create(
        post_id=post_id, 
        location=data['location'], 
        contact=data['contact'], 
        post_type=data['post_type'])
    return jsonify(ret)


@app.route('/api/posts/get/<post_id>', methods=['GET'])
def get_post(post_id):
    return jsonify(datastore.read_one(post_id))

@app.route('/api/posts/search/', defaults={'term': ''}, methods=['GET'])
@app.route('/api/posts/search/<term>', methods=['GET'])
def search_post(term):
    return jsonify(datastore.read_many(term))

@app.route('/api/posts/update', methods=['POST'])
def update_post():
    data = request.json
    ret = datastore.update(
        post_id=data['post_id'],
        image_id=data['image_id'],
        location=data['location'],
        contact=data['contact'],
        breed=data['breed'],
        post_type=data['post_type'])
    return jsonify(ret)


@app.route('/api/posts/delete', methods=['POST'])
def delete_post():
    data = request.json
    return jsonify(datastore.delete(post_id=data['post_id']))

@app.route('/api/images/upload/<post_id>', methods=['POST'])
def upload_image(post_id):
    image_id = str(uuid.uuid4())
    uploaded_file = request.files['file']
    if uploaded_file:
        image_url = storage.save(image_id, uploaded_file)
        tags = vision.get_tags('gs://project3-294022.appspot.com/'+image_id)
        breed = vision.get_breed(tags)
        datastore.update(post_id=post_id, image_id=image_id, image_url=image_url, breed=breed, tags=tags)
        ret = {'status': 'success', 'image_id': image_id}
        return jsonify(ret)