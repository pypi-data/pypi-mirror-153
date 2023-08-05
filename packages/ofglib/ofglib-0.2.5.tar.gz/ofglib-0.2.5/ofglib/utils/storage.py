import boto3
import boto3.session
import io

import os
import pickle

def save_model(PATH, model, model_id:int, target_id:int):
    initial_dir = PATH
    check = os.path.join(initial_dir, r'models')
    if not os.path.exists(check):
        os.makedirs(check)
    os.chdir(check)

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, f'{model_id}')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    file_name = f'{current_directory}\{model_id}\{model_id}_{target_id}.model'
    print(file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(model, f)
    os.chdir(initial_dir)


def get_models(PATH, model_id:int):

    initial_dir = PATH
    model_dir = os.path.join(initial_dir, r'models')
    model_dir = os.path.join(model_dir, f'{model_id}')
    os.chdir(model_dir)
    model_names = os.listdir()

    models = []
    for file in model_names:
        file = open(file, 'rb')
        model = pickle.load(file)
        models.append(model)
        file.close()

    os.chdir(initial_dir)

    return models


class S3_Connector():
    def __init__(self,
                 ACCESS_KEY: str = '',
                 SECRET_KEY: str = '',
                 BUCKET_NAME: str = ''):

        session = boto3.session.Session(
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        self.s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )

        self.bucket = BUCKET_NAME

    def get_csv(self, file_name):

        # download file in memory
        file_stream = io.BytesIO()
        self.s3.download_fileobj(self.bucket, file_name, file_stream)
        file_stream.seek(0)

        return file_stream

    def get_model(self, model_name):

        # download file in memory
        file_stream = io.BytesIO()
        self.s3.download_fileobj(
            self.bucket,
            f"{model_name}.model",
            file_stream
        )
        file_stream.seek(0)

        return pickle.load(file_stream)

    def save_obj(self, model_name, file_stream, ext):

        try:
            file_stream.seek(0)
            self.s3.upload_fileobj(
                file_stream, self.bucket, f"{model_name}{ext}"
            )
            file_stream.close()
        except Exception:
            pass
        return 0
