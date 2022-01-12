# **Process Notifyer**
## **Description**
The project Process notifer is just a python script for notify a specific task which you performing on a linux machine.In some case like buliding your project might take a lot time inorder to notify you after the completion of the bulid process via mobile phone by simple pop-up notification.

## **Installation**
1. To start off with we need to download the [push butllet](https://play.google.com/store/apps/details?id=com.pushbullet.android) app for our andriod phone.
2. Next to that create a account on it and also go to [push-bullet website](https://www.pushbullet.com/).
3. create an API token from **Settings->Account->Create Access Token.**
4. clone the repository using git clone.
```
$ git clone https://github.com/SPR-Ideas/Make_FTP.git
```
5. Navigate to the directory and type make install command
```
$ make install
```
this will automatically insall all the dependencies.It also ask for API key past the Api key which you have created in pushbullet website.it looks similary like this
```
Do you have Api key Y/n ?y
Enter the new Api key : #paste your Api-key
```
once it is all done, add the path to the environment variable so that you can acess from any directory.

## **Uninstall**
To uninstall the script navigate to the  Notify directory and type the command
```
$ make uninstall
```
it will automatically removes the apikeys stored in .notify directory.

## **Usage**
```
./notify.py -C "command to be executed" -N "text should be showed on pop msg (Optional)."
```
### *for example*
```
./notify.py -C "make bulid" -N "Your bulid is completed."
```
it automatically send a pop-up notification to your mobile once the command has be commpleted.

![alt text](.images/git.jpeg)