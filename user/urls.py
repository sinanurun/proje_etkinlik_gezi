from django.urls import path

from . import views
#app_name = 'user'
urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('user_advantures/', views.user_advantures, name='user_advantures'),
    path('user_advantures_add/', views.user_advantures_add, name='user_advantures_add'),
    path('delete_advanture/<int:id>', views.user_delete_advanture,name='user_delete_advanture' ),
    path('update_advanture/<int:id>', views.user_update_advanture,name='user_update_advanture' ),
    # path('orders_product/', views.user_order_product, name='user_order_product'),
    # path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    # path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),

]