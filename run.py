# run.py

import os

from app import create_app

#create the app and pass in the configuration name

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
