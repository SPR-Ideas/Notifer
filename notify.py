from pushbullet import PushBullet
from cryptography.fernet import Fernet
from os import system

SECRET_FILE = "/home/levi/programing/Notifyer/secret.key"
ENCRYPTED_TOKEN = "/home/levi/programing/Notifyer/access_token"


def generate_key():
    """
    Generates a key and save it into a file.
    """
    key = Fernet.generate_key()
    with open(SECRET_FILE, "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Load the previously generated key.
    """
    return open(SECRET_FILE, "rb").read()


def encrypt_message(message):
    """
    Encrypts a message.
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message.
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message


def change_api_key():
    """
    It encrypt and save the new API Key and
    deletes the old one.
    """
    new_api_key = input("Enter the new Api key : ")
    generate_key()
    encrypted_token = encrypt_message(new_api_key)

    with open(ENCRYPTED_TOKEN,"wb") as fp:
        fp.write(encrypted_token)
        fp.close()


def get_token():
    """
    Gives the  Api-token.
    """
    with open(ENCRYPTED_TOKEN,"rb") as fp:
        token = fp.read()
        token = decrypt_message(token)
    return token


def send_notification(title,msg):
    """
    Sends the notification to our mobile.
    """
    token = get_token()
    pb = PushBullet(token)
    status = pb.push_note(title,msg)
    return status


def task_notifyer(cmd,msg="100%"):
    system(cmd)
    send_notification("Completed ", msg)


