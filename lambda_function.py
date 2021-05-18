# python imports
import json
import logging
import os
import uuid
from urllib.parse import unquote

# third party imports
import boto3
import requests

logger = logging.getLogger()
VALID_EXT = ["mp4", "MOV", "flv", "ogv", "mov"]


def lambda_handler(event, context):
    event = event['Records']
    response = list()
    for event_obj in event:
        bucket_name = event_obj['bucket_name']
        # ex: object_key= videos/{user_id}/03-03-2020/abc.mov
        file_obj = event_obj['object_key']
        # extract the extension ex. mov
        obj_ext = file_obj.split(".")[-1]
        if obj_ext in VALID_EXT:
            obj_name = unquote(file_obj[:len(file_obj) - (len(obj_ext) + 1)].replace("+", " "))

            # creating a thumbnail file location for s3
            # ex. thumbnail/videos/{user_id}/03-03-2020/abc_thumbnail.jpeg
            aws_file_path = "thumbnails/" + obj_name + "_thumbnail.jpeg"
            # temporary downloaded video path on aws lambda
            tmp_video_path = "/tmp/" + str(uuid.uuid1()) + ".{}".format(obj_ext)
            # thumbnail path on aws lambda
            thumbnail_file = "/tmp/" + str(uuid.uuid1()) + ".jpeg"
            s3 = boto3.client('s3')
            # download the video from s3 to aws lambda
            s3.download_file(bucket_name, obj_name + "." + obj_ext, tmp_video_path)

            os.system(
                "yes | /opt/python/ffmpeg -i " + tmp_video_path + " -ss 00:00:01.000 -vframes 1 " + thumbnail_file)
            try:
                # upload file on the specific path
                # which will be ex. thumbnail/videos/{user_id}/03-03-2020/abc_thumbnail.jpeg
                s3.upload_file(thumbnail_file, bucket_name, aws_file_path)
            except Exception as e:
                print("error while uploading thumbnail to bucket")
                print(str(e))

            # you can use below code if you want your lambda function to notify your server
            # tht the job is done and this is the response
            # but for this you have to pass the 'env' in the request params
            # and have to define the environment variable 'webhook' as your API endpoint
            base_url = os.environ.get(event_obj['env'])
            url = base_url + os.environ['web_hook']
            header = {'Content-Type': "Application/json"}
            data = {'video_url': obj_name+"."+obj_ext, 'thumbnail_url': aws_file_path.replace(" ", "+"),
                    "object_id": event_obj['object_id'], "object_type": event_obj['object_type']}
            response.append(data)

            # to delete the temporary files created
            os.remove(tmp_video_path)
            os.remove(thumbnail_file)
        # hit your server url
        requests.post(url, json.dumps(response), headers=header)
        print("call back sent")
    return {
        'statusCode': 200,
        'body': "Ok."
    }
