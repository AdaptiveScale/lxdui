import requests

__FIREBASE_USER_VERIFY_SERVICE = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
__FIREBASE_API_KEY = "AIzaSyAVIWywqLtxfRLxZfjAauCK6tH-udR_jeo"

def firebaseLogin(email, passwd):
    url = "%s?key=%s" % (__FIREBASE_USER_VERIFY_SERVICE, __FIREBASE_API_KEY)
    data = {"email": email,
            "password": passwd,
            "returnSecureToken": True}

    result = requests.post(url, json=data)
    json_result = result

    return json_result