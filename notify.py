"""
    Notifyer
            Whenever we used to perform a bigger taks in a machine like copying a bigger files ,
        buliding process and installation process we often used to check our machine untill
        the completion of the task.

            Here the script has different approach that one can start a bigger process and he can
        leave the system for a while and can go for a break. once the task assigned is completed it
        automatically send us a notification that the task is completed.
"""
#!/bin/python3
from os import system,path
import sys
import argparse
from pushbullet import PushBullet ,errors
from cryptography.fernet import Fernet
import requests

SECRET_FILE = path.expanduser("~")+"/.notify/client_secret/secret.key"
ENCRYPTED_TOKEN = path.expanduser("~")+"/.notify/client_secret/access_token"


def end(msg):
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
    with open(SECRET_FILE, "rb") as r:
        return r.read()


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


def check_api_key(api_key):
    """
        It checks the wether the api key is valid or not form the pushnote
    server.
    """
    try :
        PushBullet(api_key)
    except errors.InvalidKeyError:
        end(" ------------------! Wrong API key !----------------- ")
    except requests.exceptions.ConnectionError:
        end(" ---------! Check Your Internet connection !--------- ")


def change_api_key():
    """
    It encrypt and save the new API Key and
    deletes the old one.
    """
    choice = input("Do you have Api key Y/n ?")

    if choice in ("y" ,"Y"):
        new_api_key = input("Enter the new Api key : ")
        generate_key()
        check_api_key(new_api_key)
        encrypted_token = encrypt_message(new_api_key)

        with open(ENCRYPTED_TOKEN,"wb") as fp:
            fp.write(encrypted_token)
            fp.close()
        print(" ----------------- # API-key is Sucessfully Updated # --------------")

    else:
        end("Get Api key form https://www.pushbullet.com")


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
    try:
        pb = PushBullet(token)
        pb.push_note(title,msg)
    except requests.exceptions.ConnectionError:
        end(" ---------! Check Your Internet connection !--------- ")


def task_notifyer(cmd,msg="100%"):
    """
        It is the start of the program it execute the tasks and
        once its is completed it sends the notification for user.
    """
    if system(cmd) == 0:
        send_notification("Completed ", msg)
    else:
        send_notification("process failed ","cmd : "+cmd+"\n"+ ''if msg == "100%" else msg )


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
