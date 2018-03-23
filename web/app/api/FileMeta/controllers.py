from flask import Blueprint, jsonify, request
from .models import *
from .validators import *
from werkzeug.utils import secure_filename
from dicttoxml import dicttoxml
import os
import json
import random
import string


File = Blueprint('File', __name__)

ALLOWED_EXTENSIONS = set(['json'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@File.route('/xml', methods=['GET'])
def download_xml():
    file_request = request.get_json()
    is_valid = get_validator(file_request)
    if not is_valid:
        response = jsonify({'error': get_validator.errors})
        return response
    link = file_request['link']
    file_meta = FileMeta.query.filter_by(link=link).first()
    if file_meta == None:
        response = jsonify({'error': 'file not found'})
        return response, 404
    if file_meta.protected == True and 'password' not in file_request:
        response = jsonify({'error': 'password required'})
        return response, 400
    if file_meta.protected == True and file_meta.password != file_request['password']:
        response = jsonify({'error': 'wrong password'})
        return response
    file_json = json.loads(open('JSON/{}'.format(link), 'r').read())
    xml = dicttoxml(file_json)
    return xml


@File.route('/get', methods=['GET'])
def get_file():
    file_request = request.get_json()
    is_valid = get_validator(file_request)
    if not is_valid:
        response = jsonify({'error': get_validator.errors})
        return response
    link = file_request['link']
    file_meta = FileMeta.query.filter_by(link=link).first()
    if file_meta == None:
        response = jsonify({'error': 'file not found'})
        return response, 404
    if file_meta.protected == True and 'password' not in file_request:
        response = jsonify({'error': 'password required'})
        return response, 400
    if file_meta.protected == True and file_meta.password != file_request['password']:
        response = jsonify({'error': 'wrong password'})
        return response
    file_content = json.loads(open('JSON/{}'.format(link), 'r').read())
    result_meta = file_meta_schema.dump(file_meta).data
    return jsonify({'meta': result_meta, 'content': file_content})


@File.route('/save', methods=['POST'])
def upload_file():
    file_json = request.files['file']
    if 'file' not in request.files:
        response = jsonify({'error': 'No file part'})
        return response, 400
    if file_json.filename == '':
        response = jsonify({'error': 'No selected file'})
        return response, 400
    if file_json and allowed_file(file_json.filename):
        link = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        file_json.filename = link
        filename = secure_filename(file_json.filename)
        file_json.save(os.path.join('JSON', filename))
        weight = os.stat('JSON/{}'.format(link)).st_size
        file_meta = FileMeta(
            protected=False,
            password=None,
            weight=weight,
            link=link
        )
        db.session.add(file_meta)
        db.session.commit()
        response = file_meta_schema.dump(file_meta)
        return jsonify(response.data)
    else:
        return jsonify({'error': 'bad extension'})


@File.route('/delete', methods=['DELETE'])
def delete_file():
    file_request = request.get_json()
    is_valid = get_validator(file_request)
    if not is_valid:
        response = jsonify({'error': get_validator.errors})
        return response
    link = file_request['link']
    file_meta = FileMeta.query.filter_by(link=link).first()
    if file_meta == None:
        response = jsonify({'error': 'file not found'})
        return response, 404
    if file_meta.protected == True and 'password' not in file_request:
        response = jsonify({'error': 'password required'})
        return response, 400
    if file_meta.protected == True and file_meta.password != file_request['password']:
        response = jsonify({'error': 'wrong password'})
        return response
    os.remove(os.path.join('JSON', link))
    db.session.delete(file_meta)
    db.session.commit()
    response = jsonify({'message': 'successfully deleted'})
    return response, 200


#God bless a man who will read it
@File.route('/update', methods=['PUT'])
def update_file():
    file_request = request.get_json()
    is_valid = get_validator(file_request)
    if not is_valid:
        response = jsonify({'error': get_validator.errors})
        return response
    link = file_request['link']
    file_meta = FileMeta.query.filter_by(link=link).first()
    if file_meta == None:
        response = jsonify({'error': 'file not found'})
        return response, 404
    if file_meta.protected == True and 'password' not in file_request:
        response = jsonify({'error': 'password required'})
        return response, 400
    if file_meta.protected == True and file_meta.password != file_request['password']:
        response = jsonify({'error': 'wrong password'})
        return response
    if 'protected' in file_request:
        if file_request['protected'] == True:
            if file_meta.protected == True:
                if 'old_password' not in file_request:
                    response = jsonify({'error': 'no old_password in request'})
                    return response, 400
                if 'old_password' != file_meta.password:
                    response = jsonify({'error': 'wrong password'})
                    return response, 400
                if 'new_password' not in file_request:
                    response = jsonify({'error': 'no new_password in request'})
                    return response, 400
                if file_request['new_password'] == None:
                    response = jsonify({'error': 'no new_password in request'})
                    return response, 400
                file_meta.password = file_request['new_password']
            else:
                if 'new_password' not in file_request:
                    response = jsonify({'error': 'no new_password in request'})
                    return response, 400
                if file_request['new_password'] == None:
                    response = jsonify({'error': 'no new_password in request'})
                    return response, 400
                file_meta.protected = True
                file_meta.password = file_request['new_password']
                db.session.commit()
        else:
            if file_meta.protected == True:
                if 'old_password' not in file_request:
                    response = jsonify({'error': 'no old_password in request'})
                    return response, 400
                if 'old_password' != file_meta.password:
                    response = jsonify({'error': 'wrong password'})
                    return response, 400
                file_meta.protected = False
                file_meta.password = None
                db.session.commit()
            else:
                response = jsonify({'error': 'protected is already False'})
                return response, 400
    if 'content' in file_request:
        if file_request['content'] == None:
            response = jsonify({'error': 'no new_password in request'})
            return response, 400
        else:
            file_content = file_request['content']
            file_json = open(os.path.join('JSON', link), 'w').write(file_content)
            response = jsonify({'message': 'file updated'})
            return response
