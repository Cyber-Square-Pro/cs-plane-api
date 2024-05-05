import jwt
from django.conf import settings

def generate_token(user_id, email):

    # Create payload
    payload = {
        'id': user_id,
        'email': email
    }
    
    # Encode token
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm = 'HS256')
    
    return token
