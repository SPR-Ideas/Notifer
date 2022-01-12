#!/bin/python3
from os import system,path
import sys
import argparse
from pushbullet import PushBullet
from cryptography.fernet import Fernet

SECRET_FILE = path.expanduser("~")+"/.notify/client_secret/secret.key"
ENCRYPTED_TOKEN = path.expanduser("~")+"/.notify/client_secret/access_token"


def exit(msg):
    """
    Prints the error and exits the program.
    """
    print(msg)
    sys.exit(1)

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
    choice = input("Do you have Api key Y/n ?")

    if choice == "y" or choice =="Y":
        new_api_key = input("Enter the new Api key : ")
        generate_key()
        encrypted_token = encrypt_message(new_api_key)

        with open(ENCRYPTED_TOKEN,"wb") as fp:
            fp.write(encrypted_token)
            fp.close()
    else:
        exit("Get Api key form https://www.pushbullet.com")


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


def install():
    """
        It ask for the Api key for intallation and once it got it
        it creats an client_secret files if not end the program by
        exit status 1.
    """
    change_api_key()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-C",type=str,required=False)
    parser.add_argument("-N" ,type=str,required=False)
    parser.add_argument("--set",type=str,required=False)
    parser.add_argument("-I",type=str,required=False)

    args = parser.parse_args()

    if args.N and args.C :
        task_notifyer(args.C, args.N)

    elif args.set :
        if args.set == "api-key":
            change_api_key()

    elif args.C :
        task_notifyer(args.C)

    elif args.I :
        install()
