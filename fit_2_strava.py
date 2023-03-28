from stravalib.client import Client
from stravalib.exc import RateLimitExceeded, RateLimitTimeout, ActivityUploadFailed
from config import FIT_OUTPUT_DIR, STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_REFRESH_TOKEN, STRAVA_ACCESS_TOKEN
import time
import os

def upload_file_to_strava(client, file_name, data_type):
    with open(file_name, "rb") as f:
        try:
            r = client.upload_activity(activity_file=f, data_type=data_type)
        except RateLimitExceeded as e:
            timeout = e.timeout
            print()
            print(f"Strava API Rate Limit Exceeded. Retry after {timeout} seconds")
            print()
            time.sleep(timeout)
            r = client.upload_activity(activity_file=f, data_type=data_type)
        print(
            f"Uploading {data_type} file: {file_name} to strava, upload_id: {r.upload_id}."
        )


def main() :
    client_id=STRAVA_CLIENT_ID
    client_secret=STRAVA_CLIENT_SECRET
    refresh_token=STRAVA_REFRESH_TOKEN
    access_token=STRAVA_ACCESS_TOKEN
    
    folder_path = FIT_OUTPUT_DIR

    client = Client()
    if len(access_token) != 40 :
        refresh_response = client.refresh_access_token(
            client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
        )
        
        client.access_token = refresh_response["access_token"]
    else:
        client.access_token = access_token

    print("For {id}, I now have an access token {token}".format(id=client_id, token=client.access_token))
    
    # get file list     
    files = os.listdir(folder_path)

    for file_name in files:
        print("======================\n", file_name)
        if not file_name.endswith(".fit"):
            continue
        
        file_name = os.path.join(folder_path, file_name)
        try:
            upload_file_to_strava(client, file_name, "fit")
        except RateLimitTimeout as e:
            timeout = e.timeout
            print(f"Strava API Rate Limit Timeout. Retry in {timeout} seconds\n")
            time.sleep(timeout)
            # try previous again
            upload_file_to_strava(client, file_name, "fit")

        except ActivityUploadFailed as e:
            print(f"Upload faild error {str(e)}")
        # spider rule
        time.sleep(5)


if __name__ == "__main__":
    main()