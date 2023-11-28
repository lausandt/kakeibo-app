from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schema

# C:\Program Files\Git\usr\bin> .\openssl rand -hex 32
SECRET_KEY = "e54a036a73faf7cf3b6cd12ff1674f4e072e2669549855af00dee4e88b0ecf72"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return schema.TokenData(username=email)
    except JWTError:
        raise credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
