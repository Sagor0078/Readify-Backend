import jwt
import uuid
import logging
from src.config import Config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer


# Initialize password hashing context
passwd_context = CryptContext(schemes=["bcrypt"])

# Token expiry configuration
ACCESS_TOKEN_EXPIRY = 3600  # 1 hour

def generate_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return passwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    """Verify a stored password against one provided by user."""
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    """Create a JWT access token."""
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    # Encode the token
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    """Decode a JWT access token."""
    try:
        # Attempt to decode the token
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
        return None
    except Exception as e:
        logging.exception("An error occurred while decoding the token.")
        return None


serializer = URLSafeTimedSerializer(
    secret_key= Config.JWT_SECRET,
    salt = "email-verification"
)

def create_url_safe_token(data: dict):
    
    token = serializer.dumps(data)

    return token

def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))

