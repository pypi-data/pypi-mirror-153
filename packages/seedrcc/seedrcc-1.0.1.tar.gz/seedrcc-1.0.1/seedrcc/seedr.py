import requests
import functools
from base64 import b64decode

import validators

from seedrcc.login import Login
from seedrcc.login import createToken


class Seedr():
    """
    This class contains the method to access the seedr account

    Args:
        token (str): Token of the seedr account
        callbackFunc (function, optional): Callback function to call
            after the token is refreshed

    Example:
        >>> seedr = Seedr(token='token')

    Example:
        The callback function will be called after the token is refreshed.

            >>> def callbackFunc(token):
            >>>     print(f'Token refreshed: {token}')

            >>> seedr = Seedr(token='token', callbackFunc=callbackFunc)

        If the callback function has more than one argument, pass the function
        as a lambda function.

            >>> def callbackFunc(token, userId):
            >>>     print(f'Token refreshed of {userId}: {token}')

            >>> seedr = Seedr(token='token', callbackFunc=lambda token: callbackFunc(token, '1234'))
    """
    def __init__(self, token, callbackFunc=None):
        self.token = token
        token = eval(b64decode(token))
        self._callback_func = callbackFunc

        self._base_url = 'https://www.seedr.cc/oauth_test/resource.php'
        self._access_token = token['access_token']
        self._refresh_token = token['refresh_token'] if 'refresh_token' in token else None
        self._device_code = token['device_code'] if 'device_code' in token else None

    def testToken(self):
        """
        Test the validity of the token

        Example:
            >>> response = account.testToken()
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'test'
        }

        response = requests.get(self._base_url, params=params)
        return response.json()

    def __autoRefresh(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            try:
                response = response.json()

            except requests.exceptions.JSONDecodeError:
                return {
                    'result': False,
                    'code': 400,
                    'error': response.text
                }

            if 'error' in response and response['error'] == 'expired_token':
                refreshResponse = self.refreshToken()

                if 'error' in refreshResponse:
                    return refreshResponse

                response = func(self, *args, **kwargs).json()

            return response

        return wrapper

    def refreshToken(self):
        '''
        Refresh the expired token

        Note:
            This method is called automatically after the token is refreshed by
            the module. However, you can call it manually if you want to
            refresh the token.

        Example:
            >>> response = account.refreshToken()
            >>> print(account.token)
        '''

        if self._refresh_token:
            url = 'https://www.seedr.cc/oauth_test/token.php'

            data = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": "seedr_chrome"
            }

            response = requests.post(url, data=data).json()

        else:
            response = Login().authorize(deviceCode=self._device_code)

        if 'access_token' in response:
            self._access_token = response['access_token']

            self.token = createToken(
                response, self._refresh_token, self._device_code
                )

            if self._callback_func:
                self._callback_func(self.token)

        return response

    @__autoRefresh
    def getSettings(self):
        """
        Get the user settings

        Example:
            >>> response = account.getSettings()
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'get_settings'
        }

        response = requests.get(self._base_url, params=params)
        return response

    @__autoRefresh
    def getMemoryBandwidth(self):
        """
        Get the memory and bandwidth usage

        Example:
            >>> response = account.getMemoryBandwidth()
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'get_memory_bandwidth'
        }

        response = requests.get(self._base_url, params=params)
        return response

    @__autoRefresh
    def addTorrent(self, magnetLink=None, torrentFile=None, wishlistId=None, folderId='-1'):
        """
        Add a torrent to the seedr account for downloading

        Args:
            magnetLink (str, optional): The magnet link of the torrent
            torrentFile (str, optional): Remote or local path of the
                torrent file
            folderId (str, optional): The folder id to add the torrent to.
                Defaults to '-1'.

        Example:
            Adding torrent to the root folder using magnet link

            >>> response = account.addTorrent(magnetLink='magnet:?xt=')
            >>> print(response)

        Example:
            Adding torrent from local torrent file

            >>> response = account.addTorrent(torrentFile='/path/to/torrent')
            >>> print(response)

        Example:
            Adding torrent from remote torrent file

            >>> response = account.addTorrent(torrentFile='https://api.telegram.org/file/bot<token>/<file_path>')
            >>> print(response)

        Example:
            Adding torrent using wishlistId

            >>> response = account.addTorrent(wishlistId='12345')
            >>> print(response)

        Example:
            Adding torrent to a certain folder

            >>> response = account.addTorrent(magnetLink='magnet', folderId='12345')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'add_torrent'
        }

        data = {
            'torrent_magnet': magnetLink,
            'wishlist_id': wishlistId,
            'folder_id': folderId
        }

        files = {}

        if torrentFile:
            if validators.url(torrentFile):
                file = requests.get(torrentFile).content

                files = {
                    'torrent_file': file
                }

            else:
                files = {
                    'torrent_file': open(torrentFile, 'rb').read(),
                }

        response = requests.post(self._base_url, data=data, params=params, files=files)
        return response

    @__autoRefresh
    def scanPage(self, url):
        """
        Scan a page and return a list of torrents. For example,
        you can pass the torrent link of 1337x.to and it will fetch
        the magnet link from that page.

        Args:
            url (str): The url of the page to scan

        Example:
            >>> response = account.scanPage(url='https://1337x.to/torrent/1010994')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'scan_page'
        }

        data = {
            'url': url
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def createArchive(self, folderId):
        """
        Create an archive link of a folder

        Args:
            folderId (str): The folder id to create the archive of

        Example:
            >>> response = account.createArchive(folderId='12345')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'create_empty_archive'
        }

        data = {
            'archive_arr': f'[{{"type":"folder","id":{folderId}}}]'
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def fetchFile(self, fileId):
        """
        Create a link of a file

        Args:
            fileId (string): The file id to fetch

        Example:
            >>> response = account.fetchFile(fileId='12345')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'fetch_file'
        }

        data = {
            'folder_file_id': fileId
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def listContents(self, folderId=0, contentType='folder'):
        """
        List the contents of a folder

        Args:
            folderId (str, optional): The folder id to list the contents of.
                Defaults to root folder.
            contentType (str, optional): The type of content to list.
                Defaults to 'folder'.

        Example:
            list the contents of the root folder

            >>> response = account.listContents()
            >>> print(response)

        Example:
            list the contents of the folder with id '12345'

            >>> response = account.listContents(folderId='12345')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'list_contents'
        }

        data = {
            'content_type': contentType,
            'content_id': folderId
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def renameFile(self, fileId, renameTo):
        """
        Rename a file

        Args:
            fileId (str): The file id to rename
            renameTo (str): The new name of the file

        Example:
            >>> response = account.renameFile(fileId='12345', renameTo='newName')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'rename'
        }

        data = {
            'rename_to': renameTo,
            'file_id': fileId
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def renameFolder(self, folderId, renameTo):
        """
        Rename a folder

        Args:
            folderId (str): The folder id to rename
            renameTo (str): The new name of the folder

        Example:
            >>> response = account.renameFolder(folderId='12345', renameTo='newName')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'rename'
        }

        data = {
            'rename_to': renameTo,
            'folder_id': folderId
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def deleteFile(self, fileId):
        """
        Delete a file

        Args:
            fileId (str): The file id to delete

        Example:
            >>> response = account.deleteFile(fileId='12345')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'delete'
        }

        data = {
            'delete_arr': f'[{{"type":"file","id":{fileId}}}]'
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def deleteFolder(self, folderId):
        """
        Delete a folder

        Args:
            folderId (str): The folder id to delete

        Example:
            >>> response = account.deleteFolder(folderId='12345')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'delete'
        }

        data = {
            'delete_arr': f'[{{"type":"folder","id":{folderId}}}]'
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def deleteWishlist(self, wishlistId):
        """
        Delete an item from the wishlist

        Args:
            wishlistId (str): The wishlistId of item to delete

        Example:
            >>> response = account.deleteWishlist(wishlistId='12345')
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'remove_wishlist'
        }

        data = {
            'id': wishlistId
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def deleteTorrent(self, torrentId):
        """
        Delete an active downloading torrent

        Args:
            torrentId (str): The torrent id to delete

        Example:
            >>> response = account.deleteTorrent(torrentId='12345')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'delete'
        }

        data = {
            'delete_arr': f'[{{"type":"torrent","id":{torrentId}}}]'
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def addFolder(self, name):
        """
        Add a folder

        Args:
            name (str): Folder name to add

        Example:
            >>> response = account.addFolder(name='New Folder')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'add_folder'
        }

        data = {
            'name': name
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def searchFiles(self, query):
        """
        Search for files

        Args:
            query (str): The query to search for

        Example:
            >>> response = account.searchFiles(query='harry potter')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'search_files'
        }

        data = {
            'search_query': query
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def changeName(self, name, password):
        """
        Change the name of the account

        Args:
            name (str): The new name of the account
            password (str): The password of the account

        Example:
            >>> response = account.changeName(name='New Name', password='password')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'user_account_modify'
        }

        data = {
            'setting': 'fullname',
            'password': password,
            'fullname': name
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def changePassword(self, oldPassword, newPassword):
        """
        Change the password of the account

        Args:
            oldPassword (str): The old password of the account
            newPassword (str): The new password of the account

        Example:
            >>> response = account.changePassword(oldPassword='oldPassword', newPassword='newPassword')
            >>> print(response)
        """

        params = {
            'access_token': self._access_token,
            'func': 'user_account_modify'
        }

        data = {
            'setting': 'password',
            'password': oldPassword,
            'new_password': newPassword,
            'new_password_repeat': newPassword
        }

        response = requests.post(self._base_url, params=params, data=data)
        return response

    @__autoRefresh
    def getDevices(self):
        """
        Get the devices connected to the seedr account

        Example:
            >>> response = account.getDevices()
            >>> print(response)
        """
        params = {
            'access_token': self._access_token,
            'func': 'get_devices'
        }

        response = requests.get(self._base_url, params=params)
        return response
