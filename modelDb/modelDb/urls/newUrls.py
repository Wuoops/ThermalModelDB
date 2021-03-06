from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from materials.views import materials,createMaterial,createMaterialTags,updateMaterialTags,updateMaterial,deleteMaterial,uploadFiles,uploadCover
from modelRes.views import upload,resupload,resBranch,resource,branchFilePage,branchHistory,deletefile,branchremark,resBranchFileupload,newBranch,updateFile,branchIterate,giveupiterate,iterateFileupload,iterateCommit,historyFilePage
from setPages.views import branchSet,createBranch,updateBranch,deleteModal
from Login.views import login_view,logoutfunction
from homePage.views import homePage
from recycleBin.views import recycleBin,rollback


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^materials/', materials),
    url(r'^createMaterial/', createMaterial),
    url(r'^upload/', upload),
    url(r'^resupload/', resupload),
    url(r'^resBranch/', resBranch),
    url(r'^resource/', resource),
    url(r'^accounts/login*', login_view),
    url(r'^login/', login_view),
    url(r'^home*', homePage),
    url(r'^createtags*', createMaterialTags),
    url(r'^updateMaterialTags*', updateMaterialTags),
    url(r'^updateMaterial*', updateMaterial),
    url(r'^deleteMaterial/', deleteMaterial),
    url(r'^recyclebin*', recycleBin),
    url(r'^rollback*', rollback),
    url(r'^branchSet*', branchSet),
    url(r'^createBranch*', createBranch),
    url(r'^updateBranch*', updateBranch),
    url(r'^logout/', logoutfunction),
    url(r'^uploadFiles/', uploadFiles),
    url(r'^uploadCover/', uploadCover),
    url(r'^branchFilePage/', branchFilePage),
    url(r'^branchHistory/', branchHistory),
    url(r'^deletefile/', deletefile),
    url(r'^branchremark/', branchremark),
    url(r'^resBranchFileupload/', resBranchFileupload),
    url(r'^newBranch/', newBranch),
    url(r'^updateFile/', updateFile),
    url(r'^branchIterate/', branchIterate),
    url(r'^giveupiterate/', giveupiterate),
    url(r'^iterateFileupload/', iterateFileupload),
    url(r'^iterateCommit/', iterateCommit),
    url(r'^historyFilePage/', historyFilePage),
    url(r'^deleteModal/', deleteModal),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
