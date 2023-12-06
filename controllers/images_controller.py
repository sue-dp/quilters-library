from flask import jsonify
import uuid

from db import db
from config import data_store, s3_storage_type
from models.images import Images, image_schema, images_schema
from lib.authenticate import authenticate, authenticate_return_auth
from lib.s3 import s3_upload
from util.reflection import populate_object
