import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = '/Users/NikolaiLucenko/Documents/GitHub/detection-demo/images/'
    STATIC_FOLDER = '/Users/NikolaiLucenko/Documents/GitHub/detection-demo/static/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_FILE_SIZE = 16 * 1024 * 1024
    AUTHOR = {'username': 'Nick_Elixir'}
    MENU = [
        {
            'link': "/index",
            'label': 'Load Image'
        },
        {
            'link': "/gallery",
            'label': 'Gallery'
        },
        {
            'link': "/capture",
            'label': "Take a photo"
        }
    ]