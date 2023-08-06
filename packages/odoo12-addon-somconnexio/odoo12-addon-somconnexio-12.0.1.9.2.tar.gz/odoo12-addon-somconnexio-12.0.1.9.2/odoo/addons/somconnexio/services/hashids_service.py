from hashids import Hashids
import os

HASH_LENGTH = 5


class HashGetter:
    def __init__(self, id_to_hash):
        self.id = id_to_hash
        self.hashids = Hashids(
            min_length=HASH_LENGTH, salt=os.getenv('HASH_SALT', "")
        )

    def get(self):
        hashed_id = self.hashids.encode(self.id).upper()
        return hashed_id
