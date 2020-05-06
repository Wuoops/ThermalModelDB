from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from materials.views import materials,createMaterial,createMaterialTags,updateMaterialTags,updateMaterial,deleteMaterial
from modelRes.views import upload,resupload,resBranch,resource
from Login.views import login_view
from homePage.views import homePage
from recycleBin.views import recycleBin,rollback


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^materials', materials),
    url(r'^createMaterial/', createMaterial),
    url(r'^upload/', upload),
    url(r'^resupload/', resupload),
    url(r'^resBranch/', resBranch),
    url(r'^resource/', resource),
    url(r'^accounts/login/', login_view),
    url(r'^login/', login_view),
    url(r'^home*', homePage),
    url(r'^createtags*', createMaterialTags),
    url(r'^updateMaterialTags*', updateMaterialTags),
    url(r'^updateMaterial*', updateMaterial),
    url(r'^deleteMaterial*', deleteMaterial),
    url(r'^recyclebin*', recycleBin),
    url(r'^rollback*', rollback),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
