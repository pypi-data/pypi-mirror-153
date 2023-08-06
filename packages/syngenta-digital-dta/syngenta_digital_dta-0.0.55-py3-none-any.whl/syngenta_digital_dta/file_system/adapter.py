import os
import shutil

import jsonpickle
import requests

from syngenta_digital_dta.common.base_adapter import BaseAdapter
from syngenta_digital_dta.s3.adapter import S3Adapter


class FileSystemAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sns_attributes = kwargs.get('sns_attributes')
        self.sns_arn = kwargs.get('sns_arn')

    def create(self, **kwargs):
        body = self.__set_body(**kwargs)
        destination_path = kwargs['destination_path']

        self.__create_destination_directory(destination_path)

        with open(destination_path, 'wb') as file:
            file.write(body)

        if kwargs.get('publish', True):
            data = {'file_path': destination_path}
            super().publish('create', data)

    def read(self, **kwargs) -> bytes:
        with open(kwargs['file_path'], 'rb') as file:
            body = file.read()

        if kwargs.get('json', False):
            return jsonpickle.decode(body)
        return body

    def update(self, **kwargs):
        destination_path = kwargs['destination_path']

        if not os.path.isfile(destination_path):
            raise FileNotFoundError(f'No such file: {destination_path}')

        self.create(**kwargs)

    def delete(self, **kwargs):
        path = kwargs['path']

        if os.path.isdir(path) and kwargs.get('recursive', False):
            shutil.rmtree(path)
        elif os.path.isdir(path):
            raise DeleteDirectoryException(f'Set recursive to True to delete contents in folder at {path}')
        else:
            os.remove(path)

    def get_age(self, **kwargs) -> float:
        return os.stat(kwargs['path']).st_ctime

    def __set_body(self, **kwargs) -> bytes:
        if kwargs.get('file_object'):
            return kwargs['file_object']
        if kwargs.get('file_path'):
            return self.read(file_path=kwargs['file_path'])
        if kwargs.get('http_link'):
            return self.__download_file(**kwargs)
        if kwargs.get('s3_path'):
            return self.__download_from_s3(**kwargs)
        raise FileObjectExpception('No file_object, file_path, http_link, or s3_path provided')

    def __create_destination_directory(self, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    def __download_file(self, **kwargs) -> bytes:
        link = kwargs['http_link']
        headers = kwargs.get('headers')

        response = requests.request('GET', link, headers=headers)
        return response.content

    def __init_s3_adapter(self, **kwargs):
        return S3Adapter(
            region=kwargs.get('region'),
            endpoint=kwargs.get('s3_enpoint'),
            bucket=kwargs.get('bucket'),
        )

    def __download_from_s3(self, **kwargs) -> bytes:
        s3_adapter = self.__init_s3_adapter(**kwargs)
        kwargs['decode'] = False
        results = s3_adapter.get(**kwargs)
        return results['Body'].read()


class DeleteDirectoryException(Exception):
    pass


class FileObjectExpception(Exception):
    pass
