from django.urls import path
from . import views

#app_name = "wiki"
#app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    # title_ is the varaible, title__ is the request name.
    path("wiki/<str:title_>", views.pull, name="title__"), # the spec sheet wanted /wiki/
    path("query", views.search, name="query"),
    path("new_page", views.create, name="create_page"),
    path("edit_page", views.editor, name="change_page"),
    path("random", views.random_article, name="random_page"),
    path("update", views.update, name="submit_update")
]
