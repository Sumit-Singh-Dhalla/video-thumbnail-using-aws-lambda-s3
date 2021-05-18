# Create Thumbnail of Videos at S3 using AWS Lambda

* **python.zip**: this folder contains the ffmpeg libraries that we need to get the video
  frame of a video. You need to upload this zip file as a lambda layer in your
  Lambda function
  
* **lambda-function.zip**: this folder contains the env dependencies of run your code and 
  a file named lambda_function.py.
  
* **lambda_function.py**: this is the main file which executes in you lambda function.

* **requirements.txt**: it includes the package list of requirements

# if you want to check this code locally: 
    * you can create a env anf install the requirements.txt
    * download the ffmpeg and ffprobe executables and give their path in the
      lambda_function.py file
  
# if you want to test this on AWS Lambda:
    * create a python layer and upload the python.zip file init
    * create your lambda function and add the layer in this funciton
    * then upload this lambda-function.zip file as your lambda code. and everthing is set now

# Input:
  [{"bucket_name": "my-dev-bucket", "object_name": "path/to/my/video/object/in/bucket"}]


                    