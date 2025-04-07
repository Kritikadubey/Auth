import random
import pickle

async def generate_otp():
    return str(random.randint(1000, 9999))

def listToBlob(faceId):
    return pickle.dumps(faceId)

def blobToList(faceId):
    return pickle.loads(faceId)
