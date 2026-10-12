"""
Utility script to generate bcrypt hashed passwords for config.yaml
Run this script to generate secure hashes for new students or teachers.
Usage:
    python generate_keys.py
"""

try:
    import streamlit_authenticator as stauth
    
    passwords_to_hash = ["student123", "teacher123"]
    hashed_passwords = stauth.Hasher(passwords_to_hash).generate()
    
    print("Generated Hashes:")
    for pwd, hsh in zip(passwords_to_hash, hashed_passwords):
        print(f"Password '{pwd}': {hsh}")

except ImportError:
    print("streamlit-authenticator not installed yet.")
    print("Install it with: pip install streamlit-authenticator")
