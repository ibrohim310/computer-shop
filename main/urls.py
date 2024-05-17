from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.report, name='index'),

#product
    path('create/', views.add_product, name='create'),
    path('list_product/', views.list_product, name='list_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

#category
    path('category/', views.list_category, name='list_category'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
#enter
    path('enter/', views.enter_create, name='enter_create'),
    path('enter/list/', views.enter_list, name='enter_list'),

#out
    path('sell_product/', views.sell_product, name='sell_product'),
    path('list_cell_product/', views.list_cell_product, name='list_cell_product'),

#return
    path('return_product/', views.return_product, name='return_product'),
#login
    path('', views.user_login, name='login'),
]


