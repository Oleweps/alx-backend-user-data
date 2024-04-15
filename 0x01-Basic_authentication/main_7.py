#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    from api.v1.auth.basic_auth import BasicAuth

    ba = BasicAuth()
    res = None
    #res = ba.user_object_from_credentials("email", 333)
    
    if res is not None:
        print("user_object_from_credentials must return None if 'user_pwd' is not a string")
        exit(1)

    print("OK", end="")

    res = ba.user_object_from_credentials("u1@gmail.com", "pwd")
    if res is not None:
        print("user_object_from_credentials must return None if 'user_email' is not linked to any user")
        exit(1)
    print("OK", end="")
