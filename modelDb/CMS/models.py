from django.db import models
from dao.uitlsPlus import *

# Create your models here.
def zTreeList():
    cpulist = cpuList()


def cpuList():

    sql = 'select * from d_cpu_model'
    # obj = Utils()
    # obj.searchListP()
