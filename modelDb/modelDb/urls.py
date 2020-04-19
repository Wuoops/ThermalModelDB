from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import path,re_path

# from Login.views import index,login
from Login.views import LoginView
from DataManager.views.model import model,cpu,dimm,file_down,getImg
from DataManager.views.ModelViews.cpuUploadView import cpuUpload
from DataManager.views.ModelViews.dimmUploadView import dimmUpload
from DataManager.views.disk import disk
from modelDb.settings import MEDIA_ROOT
from DataManager.views.ModelViews.uploadDimmTest import dimmul
from DataManager.views.ModelViews.diskUploadView import hddUpload
from DataManager.views.ModelViews.otherUploadView import otherUpload
from DataManager.views.uploadView import uploadPage
from DataManager.views.modelDelete import *
from DataManager.views.recycleBinView import *
from CMS.views import homePage
from DataManager.views.ModelViews.resourceView import resource
from DataManager.views.ModelViews.resBranch import resBranch
from DataManager.views.ModelViews.resupload import resupload

from django.views.static import serve
urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^login/', LoginView.login),
    url(r'^model/', model),
    # url(r'^upload/', upload),
    # url(r'^edit/', upload),
    url(r'^CPU/', cpu),
    url(r'^DIMM/', dimm),
    url(r'^DISK/', disk),
    url(r'^cpuUpload/', cpuUpload),
    url(r'^CPUUpload/', cpuUpload),
    url(r'^dimmUpload/', dimmUpload),
    url(r'^DIMMUpload/', dimmUpload),
    # url(r'^dimmUpload/', dimmul),

    url(r'^hddUpload/', hddUpload),
    url(r'^HDDUpload/', hddUpload),
    url(r'^otherUpload/', otherUpload),
    url(r'^homePage/', homePage),
    # url(r'^/static/sdr.zip', file_down),
    url(r'^download/', file_down),
    # url(r'^img/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),

    url(r'^files/', serve,{"files":MEDIA_ROOT}),
    url(r'^modeldelete/', modeldelete),
    url(r'^recyclebin/', recyclebin),

    url(r'^uploadPage/', uploadPage),
    url(r'^resupload/', resupload),
    # url(r'^video/', include("modelDb.urls")),
    url(r'^resource/', resource),
    url(r'^resBranch/', resBranch),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
