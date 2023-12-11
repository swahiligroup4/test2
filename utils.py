import re  
import base64
import logging
from struct import pack
from pyrogram.errors import UserNotParticipant
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from marshmallow.exceptions import ValidationError
import os
import requests
import json
from info import DB2, COLLECTION_NAME

COLLECTION_NAME_2="gdrive"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
imdb=Instance.from_db(DB2)
@imdb.register
class User(Document):
    id = fields.StrField(attribute='_id')
    bot =fields.StrField(required=True)
    usage = fields.StrField(required=True)
    class Meta:
        collection_name = COLLECTION_NAME_2
        
async def add_link(id,sts):
    try:
        data = User(
            id = id,
            bot = sts,
            usage = "False"
        )
    except ValidationError:
        logger.exception('Error occurred while saving group in database')
    else:
        try:
            await data.commit()
        except DuplicateKeyError:
            logger.warning("already saved in database")
        else:
            logger.info("group is saved in database")

async def get_gdrive_link(query):
    filter = {"bot": query}
    total_results = await User.count_documents(filter)
    cursor = User.find(filter)
    cursor.sort('$natural',-1)
    files = await cursor.to_list(length=int(total_results))
    return files
