"""
    Unittesting for project Notifyer.
"""
from unittest.mock import patch
import requests
from pyfakefs.fake_filesystem_unittest import TestCase
import notify

files_db = {
    notify.ENCRYPTED_TOKEN : "gAAAAABiB6tZU1VB1CNO4z0Fd_yGPnUQp_YzpmDaSq"+
                             "Rkyz4p12OZAuQh1t3gIM2OqvrSvYAcYCs9YB0Y-fHR"+
                             "8g1QuxGJUWDvWZCeR0osUFc3-2ARbYNv6QtbV3WCywIdYtaphxSHF6ns",

    notify.SECRET_FILE : "Jc9Xeh8lHt_T_mpzvd9TMOSv8mMbTfOY3RYuXvU7JvA="
}

class TestNotify(TestCase):
    """
        Unittest for notify.py
    """

    def _setup_fakefs(self, files):
        self.setUpPyfakefs()
        for file_path, content in files.items():
            self.fs.create_file(file_path, contents = content )

    def _patch_system(self):
        patcher = patch('notify.system')
        mock_system  = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_system

    def _patch_exit(self):
        patcher = patch("notify.sys.exit")
        mock_exit = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_exit

    def _patch_pushbullet(self):
        patcher = patch("notify.PushBullet")
        mock_push_bullet = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_push_bullet

    def _patch_input(self):
        patcher = patch('notify.input')
        mock_input = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_input

    def _patch_print(self):
        patcher = patch('notify.print')
        mock_print = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_print

    def _patch_open(self):
        patcher= patch('notify.open')
        mock_open = patcher.start()
        self.addClassCleanup(patcher.stop)
        return mock_open


    def test_task_notifer(self):
        """
            It test the task_notifer()
                It execute the command and check's the correct token is
            loaded for ENCRYPTED_TOKEN file and sends the correct notification
            to the user.
        """
        self._setup_fakefs(files_db)
        mock_system = self._patch_system()
        mock_system.return_value = 0
        mock_pushbullet = self._patch_pushbullet()

        notify.task_notifyer("Hi")
        temp = mock_pushbullet()

        mock_system.assert_called_with("Hi")
        mock_pushbullet.assert_any_call(b'o.Rwz8cIrje22GgVy1GDxDP3SgLHtKA31e')
        temp.push_note.assert_called_once_with('Completed ','100%')


    def test_task_notifer_without_internet_connection(self):
        """
                This function test task_notifyer() when the internet connection
            is down.It checks the proper exceptional case for that.
        """
        self._setup_fakefs(files_db)
        mock_system = self._patch_system()
        mock_system.return_value = 0
        mock_pushbullet = self._patch_pushbullet()
        mock_print = self._patch_print()
        mock_exit = self._patch_exit()

        mock_pushbullet.side_effect = requests.exceptions.ConnectionError
        notify.task_notifyer("Hi")

        mock_exit.assert_called()
        mock_print.assert_any_call((" ---------! Check Your Internet connection !--------- "))


    def test_task_notifyer_with_error_status(self):
        """
            This function test the task_notifyer function
            when the command executed has error and intimatest to
            the user that the error has occured.
        """

        self._setup_fakefs(files_db)
        mock_system = self._patch_system()
        mock_system.return_value = 3145
        mock_pushbullet = self._patch_pushbullet()

        notify.task_notifyer("Hi")
        temp = mock_pushbullet()

        mock_system.assert_called_with("Hi")
        mock_pushbullet.assert_any_call(b'o.Rwz8cIrje22GgVy1GDxDP3SgLHtKA31e')
        temp.push_note.assert_any_call('process failed ', 'cmd : Hi\n')


    def test_install(self):
        """
            This function test the installation part
                - It checks wether the user has api-key
                - It checks wether it store the encrypted api-key
                seceret files
        """
        self.setUpPyfakefs()
        self.fs.create_dir(notify.ENCRYPTED_TOKEN.replace("access_token",''))
        mock_input = self._patch_input()
        mock_input.side_effect = ["y","o.Rwz8cIrje22GgVy1GDxDP3SgLHtKA31e"]
        mock_print = self._patch_print()
        self._patch_pushbullet()

        notify.install()

        self.assertTrue( self.fs.exists(notify.ENCRYPTED_TOKEN) )
        self.assertTrue( self.fs.exists(notify.SECRET_FILE) )
        mock_print.assert_any_call(
            (" ----------------- # API-key is Sucessfully Updated # --------------"))


    def test_install_with_worng_api_key(self):
        """
            It checks install() when worng api-key has been given.
        """
        self.setUpPyfakefs()
        self.fs.create_dir(notify.ENCRYPTED_TOKEN.replace("access_token",''))

        mock_pushbullet = self._patch_pushbullet()
        mock_pushbullet.side_effect = notify.errors.InvalidKeyError

        mock_input = self._patch_input()
        mock_input.side_effect = ["y","o.Rwz8cIrje22GgVy1GDxDP3SgLHtK"]# removing "A31e" from apikey

        mock_exit = self._patch_exit()
        mock_print = self._patch_print()

        notify.install()

        mock_exit.assert_called()
        mock_print.assert_any_call((" ------------------! Wrong API key !----------------- "))


    def test_install_cancellation(self):
        """
            This function test the install part when user does not have
            api-key.
        """
        mock_exit = self._patch_exit()
        mock_input = self._patch_input()
        mock_input.return_value = 'N'
        mock_print = self._patch_print()

        notify.install()

        mock_exit.assert_called()
        mock_print.assert_any_call(("Get Api key form https://www.pushbullet.com"))


    def test_install_without_internet_connection(self):
        """
            This function test the install part when there is no
            internet connection.
        """
        mock_exit = self._patch_exit()
        mock_input = self._patch_input()
        mock_print = self._patch_print()
        mock_push = self._patch_pushbullet()

        mock_push.side_effect = requests.exceptions.ConnectionError
        mock_input.return_value = 'Y'

        notify.install()

        mock_exit.assert_called()
        mock_print.assert_any_call((" ---------! Check Your Internet connection !--------- "))
