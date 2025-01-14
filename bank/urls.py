from django.urls import path

from bank import views

urlpatterns = [
        path('',views.user_login),
        path('register',views.user_registration),
        path('adminhome',views.admin_dashboard),
        path('userhome',views.user_dashboard),
        path('logout',views.user_logout),
        path('adddonor',views.register_donor),
        path('viewdonor/<str:status>/', views.view_donor),
        path('viewdonor/', views.view_donor, {'status': None}),
        path('detailedview/<int:id>', views.detailed_view_donor),
        path('updatedonor/<int:id>',views.update_donor),
        path('deletedonor/<int:id>',views.delete_donor),
        path('inventorylist',views.get_inventory),
        path('collect/<int:id>',views.collect_inventory),
]

