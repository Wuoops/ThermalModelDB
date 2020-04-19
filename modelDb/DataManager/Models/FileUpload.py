from dao.uitlsPlus import *
from django.db import models
from django.core.files.storage import FileSystemStorage

class FileUpload(models.Model):
    fileUl = models.FileField(upload_to='files')
