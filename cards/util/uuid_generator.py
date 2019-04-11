import uuid


class UuidGenerator:

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())
