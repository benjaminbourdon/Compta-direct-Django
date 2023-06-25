from django.urls import path
from . import views

urlpatterns = [
    path("import", views.ImportFileView.as_view(), name="import_file"),
    path("list", views.UserListView.as_view(), name="list_user"),
]
