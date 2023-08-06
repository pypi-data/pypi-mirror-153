import logging
import upswingutil as ul
from firebase_admin import firestore, get_app, storage


class Firestore:
    org_collection = 'Organizations'
    sub_collection_properties = 'properties'
    credentials = 'credentials'

    def __init__(self, app=None, project_name = ul.G_CLOUD_PROJECT):
        self.firestore_db = firestore.client(app=get_app(app)) if app else firestore.client()
        self.firestore_storage = storage.bucket(name=f'{project_name}.appspot.com', app=get_app(app)) if app else storage.bucket(name=f'{project_name}.appspot.com')

    def get_collection(self, name):
        return self.firestore_db.collection(name)

    def get_collection_docs(self, name):
        return self.firestore_db.collection(name).stream()

    def get_ref_collection(self, name):
        return self.firestore_db.collection(name)

    def get_ref_document(self, name, doc):
        return self.firestore_db.collection(name).document(doc).get()

    def write_doc(self, collection: str, doc: str, data: dict):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.set(data, merge=True)
        logging.debug(f"Document written successfully")

    def update_doc(self, collection: str, doc: str, data: dict):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.update(data)
        logging.debug(f"Document Updated successfully")

    def increment_doc_value(self, collection: str, doc: str, data: str, incr: int):
        __ref__ = self.firestore_db.collection(collection).document(doc)
        __ref__.update({
            data: firestore.firestore.Increment(incr)
        })

    def upload_document_firestorage(self, path: str, contentType: str,imgData: bytes, public: bool = False):
        blob_ref = self.firestore_storage.blob(path)
        blob_ref.upload_from_string(imgData, content_type=contentType)
        if public:
            blob_ref.make_public()
        return blob_ref.public_url

    def delete_document_firestorage(self, path: str):
        blob_ref = self.firestore_storage.blob(path)
        if (blob_ref.exists()):
            blob_ref.delete()
        return True
