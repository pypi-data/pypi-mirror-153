import os
import hashlib
import argparse
from os import listdir
from os.path import isfile, join
from requests import HTTPError

from storck_client import StorckClient

class AutoUploadScript:
    def __init__(self, api_host, user_token, workspace_token, upload_dir='./drop'):
        self.upload_dir = os.getenv('STORCK_AUTO_UPLOAD_DIR', upload_dir)
        self.storck_client = StorckClient(api_host, user_token, workspace_token)

    def load_files_list(self):
        files = [f for f in listdir(self.upload_dir) if isfile(join(self.upload_dir, f))]
        return files

    def filter_files(self, files_list):
        new_files = []
        for file in files_list:
            try:
                storck_file = self.storck_client.get_info(path=file)
                local_file_hash = self._hash_file(file)
                if local_file_hash != storck_file['hash']:
                    new_files.append(file)
            except HTTPError as e:
                if e.response.status_code == 404:
                    new_files.append(file)
                else:
                    raise e
        return new_files

    def upload(self, files):
        print(files)
        for file_path in files:
            self.storck_client.upload_file(self.upload_dir + "/" + file_path, path=file_path)

    def run(self):
        files = self.load_files_list()
        files = self.filter_files(files)
        self.upload(files)

    def _hash_file(self, file_path):
        with open(self.upload_dir + "/" + file_path, 'rb') as file:
            data = file.read()
        hasher = hashlib.md5()
        hasher.update(data)
        return hasher.hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatically upload files from a given directory')
    parser.add_argument('--host', '-a', dest='api_host', action='store',
                        help='STORCK api host')
    parser.add_argument('--user-token', '-u', dest='user_token', action='store',
                        help='STORCK user token')
    parser.add_argument('--workspace-token', '-w', dest='workspace_token', action='store',
                        help='STORCK workspace token')
    parser.add_argument('--dir', '-d', dest='auto_upload_dir', action='store',
                        help='auto upload directory')
    args = parser.parse_args()
    AutoUploadScript(args.api_host, args.user_token, args.workspace_token, args.auto_upload_dir).run()
