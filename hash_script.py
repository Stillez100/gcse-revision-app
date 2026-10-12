import streamlit_authenticator as stauth
import json

passwords = ["21062011", "26111968", "03011971", "06122006"]
hashes = stauth.Hasher(passwords).generate()

data = {
    "lizalou7@icloud.com": hashes[0],
    "emmandhoward@aol.com": hashes[1],
    "emmandhoward@aol.co.uk": hashes[2],
    "mstiles11@icloud.com": hashes[3]
}
with open("hashes.json", "w") as f:
    json.dump(data, f)
