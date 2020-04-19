#cpu类
from DataManager.Models.ModelClass import *

class Cpu(ModelClass):
    instractionSet=''
    bord=''
    platform=''
    code=''
    series=''
    family=''
    genoration=''
    cpu_name=''
    core=''
    threads=''
    frequency=''
    turbo=''
    process=''
    TDP=''
    suatus=''
    launchDate=''
    socket=''
    cache=''
    mem_max=''
    mem_type=''
    mem_ecc=''
    gpu_inside=''
    gpu_name=''
    #插入CPU表
    def instertCpuTable(self):
        pass
    #更新CPU表
    def updateCpuTable(self):
        pass
