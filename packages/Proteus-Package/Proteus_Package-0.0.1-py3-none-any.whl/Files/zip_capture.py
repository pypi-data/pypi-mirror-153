from flask import request, make_response
import imgkit
from pathlib import Path

import os
import shutil

from proteus_services.utils.common import decompress_file, search_recursive


class ZIPCapture:
    """
    A resource for capturing zip/presentation preview image using imgkit library
    """

    def __init__(self):
        self.file_storage_path = os.environ.get('de_storage_path', '/flask_downloads')

    def get(self):
        try:
            zip_file_part = request.files.get('file_0', None)

            if not zip_file_part:
                raise Exception('Zip file not found in request payload')

            Path(self.file_storage_path).mkdir(parents=True, exist_ok=True)

            file_path = os.path.join(self.file_storage_path, zip_file_part.filename)
            zip_file_part.save(file_path)

            head, _ = os.path.split(file_path)

            destination = os.path.join(head, 'tmp')
            decompress_file(file_path, destination)

            try:
                os.remove(file_path)
            except Exception as ex:
                print("ZipExtractor: Exception while removing file", ex)

            found, index_path = search_recursive(destination, ['index.html'])

            if found:
                try:
                    image = imgkit.from_file(index_path, False)
                except Exception as ex:
                    print("ZipCapture: Exception while capturing zip", ex)

                    options = {"xvfb": ""}
                    image = imgkit.from_file(index_path, False, options=options)

                response = make_response(image)
                response.headers.set('Content-Type', 'image/jpeg')
                response.headers.set('Content-Length', str(len(image)))
                response.headers.set('Content-Disposition', 'attachment', filename='capture.jpg')

                try:
                    shutil.rmtree(destination)
                except Exception as ex:
                    print('Error while deleting folder {}'.format(destination))
                    print(ex)

                return response
            else:
                return bytes(0)
        except Exception as ex:
            print('Exception while capturing HTML preview')
            print(ex)
            return bytes(0)
