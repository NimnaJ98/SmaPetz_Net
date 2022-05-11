import uuid

#get a random code for the slug
def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-','').lower()
    return code