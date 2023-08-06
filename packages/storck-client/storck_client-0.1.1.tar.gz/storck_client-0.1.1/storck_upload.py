import argparse
from storck_client import StorckClient


if __name__ == '__main__':
    desc = """
    This script uploads a single file in to the storck, along with optional metadata.
    !!Warning for the future!!
    This script creates just a single instance of the storck client connection, and destroys it after upload
    It might be more suitable in the future to use a mechanism that will continously wait for new uploads.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('file', action='store',
                        help='file that wil lbe uploaded')
    parser.add_argument('--storck_filepath', action='store',
                        help='if you want to store the ifle in storck under different path than provided')
    parser.add_argument('--metadata_str', action='store',
                        help='auto upload directory', default=None)

    parser.add_argument('--host', '-a', dest='api_host', action='store',
                        help='STORCK api host')
    parser.add_argument('--user-token', '-u', dest='user_token', action='store',
                        help='STORCK user token')
    parser.add_argument('--workspace-token', '-w', dest='workspace_token', action='store',
                        help='STORCK workspace token')
    args = parser.parse_args()

    client = StorckClient(args.api_host, args.user_token, args.workspace_token)
    response = client.upload_file(args.file, path=args.storck_filepath, metadata_str=args.metadata_str)
    print(response)
