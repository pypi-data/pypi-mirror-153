from zipfile import ZipFile
import os
import cchardet as chardet

import logging.handlers
logger = logging.getLogger(__name__)


def get_file_encoding(folder, filename):
    'get file encoding'       
    file_path = folder + '/' + filename
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        logger.info("result %s", result['encoding'])
        return result['encoding']


def convert_file_encoding_to_utf8(input_decode, folder, filename): 
    'convert file from input_decode to utf8'   

    file_path = folder + '/' + filename
    fbytes = ''

    logger.info("convert_file_encoding_to_utf8")
    
    if input_decode == 'UHC' or input_decode == None:
        with open(file_path, 'rb') as f:
            fbytes = f.read()
        f.close()
        new_file = folder + '/new_' + filename
        with open(new_file, 'w+b') as f:
            f.write(fbytes.decode('utf-8','ignore').encode('utf-8'))
        f.close()
        os.rename(new_file,file_path)
    else:
        with open(file_path, 'rb') as f:
            fbytes = f.read()
        f.close()
        new_file = folder + '/new_' + filename
        with open(new_file, 'w+b') as f:
            f.write(fbytes.decode(input_decode).encode('utf-8'))
        f.close()
        os.rename(new_file,file_path)
    logger.info("file conversion complete")


def unzip_file(folder, filename):
    'unzip file from folder and filename'
    zip_path = '{}/{}'.format(folder, filename)
    with ZipFile(zip_path, 'r') as zip:
        zip.extractall(path=folder)
        zip.close()
    remove_file(folder, filename)


def remove_file(folder, filename):   
    'remove file from folder and filename'     
    os.remove('{}/{}'.format(folder, filename))


def get_file_size(folder, filename):
    'get file size from folder and filename'
    file_size = os.path.getsize(folder + '/' + filename)
    return file_size  


def get_file_size(filepath):
    'get file size from filepath'
    file_size = os.path.getsize(filepath)
    return file_size  


def humanbytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B/KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B/MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B/GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B/TB)