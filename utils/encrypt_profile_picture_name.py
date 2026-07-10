from uuid import uuid4
from datetime import datetime
import os

def encrypt(filename):
    extension = os.path.splitext(filename)[1]
    
    # filename_uuid_timestamps.extension
    encrypted = f"{filename[:filename.rindex(".")]}_{uuid4()}_{int(datetime.now().timestamp())}{extension}"
    
    return encrypted