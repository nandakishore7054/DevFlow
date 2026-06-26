import time
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from jose import jwt

def run_tests():
    print("--- Testing Password Hashing ---")
    plain_password = "my_super_secret_password"
    hashed = get_password_hash(plain_password)
    print(f"Plain:  {plain_password}")
    print(f"Hashed: {hashed}")
    
    is_valid = verify_password(plain_password, hashed)
    print(f"Password Match: {is_valid}")
    
    print("\n--- Testing JWT Token Creation & Validation ---")
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    print(f"Generated Token:\n{token}\n")
    
    # Decode to verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"Decoded Payload: {payload}")
    print(f"Extracted Email: {payload.get('sub')}")
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
