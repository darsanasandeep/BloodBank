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
        path('requestlist',views.view_blood_request),
        path('request',views.register_request),
        path('viewrequest/<str:status>/', views.user_request_list),
        path('viewrequest/', views.user_request_list, {'status': None}),
        path('verification/<int:id>/<str:status>',views.approve_reject_request),
        path('verification/<int:id>/',views.approve_reject_request,{'status': None}),
        path('updaterequest/<int:id>',views.update_request),
        path('deleterequest/<int:id>', views.delete_request),
        path('detailedreqt/<int:id>',views.detailed_request),
        path('supply/<int:id>',views.supply_inventory),
        path('viewprofile',views.view_profile),
        path('updateprofile',views.update_profile),
        path('changepass',views.change_password),
        path('inactivate',views.inactivate_user)

]

