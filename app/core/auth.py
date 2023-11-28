from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# C:\Program Files\Git\usr\bin> .\openssl rand -hex 32
SECRET_KEY = "e54a036a73faf7cf3b6cd12ff1674f4e072e2669549855af00dee4e88b0ecf72"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
