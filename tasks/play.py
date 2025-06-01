import datetime
from datetime import timedelta



now = datetime.datetime.now()

sp_time = datetime.datetime(2005, 2, 22, 21)

if now and now > sp_time:
    print("damn")
    
    
diff = timedelta()

print(diff)


import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
print(code_verifier)