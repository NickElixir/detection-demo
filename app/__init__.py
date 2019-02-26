from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from config import Config
    
app = Flask(__name__)
app.config.from_object(Config)

from app import routes