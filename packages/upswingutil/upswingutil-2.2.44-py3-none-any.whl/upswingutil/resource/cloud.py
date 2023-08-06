import gcsfs
import pickle
import os
from loguru import logger
import upswingutil as ul


def get_model_from_cloud_storage(file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    __filepath__ = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(__filepath__, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f'Unable to get model : {__filepath__}')
        logger.error(e)
        return None


def upload_model_to_cloud_storage(input_data, file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    __filepath__ = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(__filepath__, 'wb') as f:
            f.write(pickle.dumps(input_data))
            return True
    except Exception as e:
        logger.error(f'Unable to write model : {__filepath__}')
        logger.error(e)
        return False


def upload_keras_model_to_cloud_storage_test(input_data, file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    __filepath__ = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(__filepath__, 'wb') as f:
            f.write(input_data)
            return True
    except Exception as e:
        logger.error(f'Unable to write model : {__filepath__}')
        logger.error(e)
        return False


def get_keras_model_from_cloud_storage_test(file_path, file_name="test.h5", token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    __filepath__ = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(__filepath__, mode='rb') as file:  # b is important -> binary
            data = file.read()
        return data
    except Exception as e:
        logger.error(f'Unable to get model : {__filepath__}')
        logger.error(e)
        return None


if __name__ == '__main__':
    f = open("upswingutil/resource/test.h5", "rb")
    print(f.read())
    with open("upswingutil/resource/test.h5", mode='rb') as file:  # b is important -> binary
        data = file.read()
    ul.FIREBASE = 'C:/Upswing/Projects/Code/agent-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json'
    ul.G_CLOUD_PROJECT = 'aura-staging-31cae'
    # data = f.read()
    # upload_model_to_cloud_storage_test(data, '11281', 'test.h5')
    get_keras_model_from_cloud_storage_test('11281')
    # data = 'test'

    # print(upload_model_to_cloud_storage(data, 'OHIPSB', 'test.txt'))
    # output = get_model_from_cloud_storage('OHIPSB', 'test.txt')
    # print(output)
