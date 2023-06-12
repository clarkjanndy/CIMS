from django.urls import path
from . import views
from .views import line_chart, line_chart_json


urlpatterns = [
   # users paths
   path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
   path('register/',views.register, name='register'),
    path('faculty_reg',views.faculty_reg, name='faculty_reg'),
   path('nstp_reg',views.nstp_reg, name='nstp_reg'),
#    path('rotc_reg',views.rotc_reg, name='rotc_reg'),
   path('staff_reg',views.staff_reg, name='staff_reg'),
   path('register/addRecord/',views.addRecord, name='addRecord'),
   path('faculty_addRecord/',views.faculty_addRecord, name='faculty_addRecord'),
   path('nstp_addRecord/',views.nstp_addRecord, name='nstp_addRecord'),
   path('staff_addRecord/',views.staff_addRecord, name='staff_addRecord'),
#    path('rotc_addRecord/',views.rotc_addRecord, name='rotc_addRecord'),
#    path('register/upload/', views.image_upload_view),
   path('login',views.user_login, name='user_login'),
   path('submitlogin/',views.usersubmitlogin, name='usersubmitlogin'),
   
   path('home/',views.user_home_page, name='user_home_page'),
   path('med_inquiry/',views.med_inquiry, name='med_inquiry'),
   path('home/upload_prof_pic/',views.upload_prof_pic, name='upload_prof_pic'),
   path('home/edit_user_profile',views.edit_user_profile, name='edit_user_profile'),
   path('home/submit_post/',views.submit_post, name='submit_post'),
   path('',views.user_login, name='index'),
   path('logout/',views.user_logout, name='user_logout'),
   path('qualified_rotc',views.qualified_rotc, name='qualified_rotc'),
   path('qualified_cwts',views.qualified_cwts, name='qualified_cwts'),
  
    # admin paths

    path('admin/register/',views.admin_register, name='admin_register'),
    path('admin/register/adminSubmitReg/',views.adminSubmitReg, name='adminSubmitReg'),
    path('comment/<int:pk>',views.comment,name='comment'),
    path('admin/',views.admin_home_page, name='admin_home_page'),
    path('admin/home/',views.admin_home_page, name='admin_home_page'),  
    path('admin/faculty_list',views.faculty_list, name='faculty_list'),
    
    path('admin/add_category',views.add_category, name='add_category'),
    
    path('admin/rotc_qualified',views.qualified_rotc_list, name='admin_users_list'),
    path('admin/users_list',views.admin_users_list, name='admin_users_list'),
    path('admin/users_list/view_by_level',views.view_by_level, name='view_by_level'),
    path('admin/bulk-delete',views.bulk_delete, name='view_by_level'),
    
    path('admin/with_condition',views.with_condition, name='with_condition'),
    path('admin/home/delete_post/<int:pk>',views.delete_post,name='delete_post'),
    path('admin/home/view_post/<int:pk>',views.view_post,name='view_post'),
    path('features/submit_post/',views.submit_post, name='submit_post'),
    path('admin/login/',views.admin_login, name='admin_login'),
    path('admin/login/submitlogin/',views.adminsubmitlogin, name='adminsubmitlogin'),
    path('admin/logout/',views.admin_logout, name='admin_logout'),
    path('admin/delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('admin/for_confirmation',views.admin_for_confirmation, name='admin_for_confirmation'),
    path('admin/confirm_user/<int:pk>', views.confirm_user, name="confirm_user"),
    path('admin/edit_user/<int:pk>', views.edit_user, name="edit_user"),
    path('admin/edit_user/save_edit_user/<int:pk>', views.save_edit_user, name="save_edit_user"),
    path('admin/check_user/<int:id>', views.check_user, name="check_user"),
    path('admin/inventory',views.admin_inventory, name='admin_inventory'),
    path('admin/inventory/remove_order/<int:pk>',views.remove_order, name='remove_order'),
    path('admin/inventory/check_out_order',views.check_out_order, name='check_out_order'),
    path('admin/inventory/add_order',views.add_order, name='add_order'),
    path('admin/inventory/list',views.list_by, name='list_by'),
    path('admin/inventory/add_stock/<int:pk>',views.add_stock, name='add_stock'),
    path('admin/inventory/delete_stock/<int:pk>',views.delete_stock, name='delete_stock'),
     path('admin/inventory/add_stock/save_added_stock/<int:pk>',views.save_added_stock, name='save_added_stock'),
    path('admin/inventory/expired',views.expired, name='expired'),
    path('admin/inventory/save',views.save_item, name='save_item'),
    path('features',views.features,name='features'),
    path('message',views.message,name='message'),
    path('features/announcements',views.announcements,name="announcements"),
    path('send',views.send,name='send'),
    path('visit_history',views.visit_history,name='visit_history'),
    path('medical_notes',views.medical_notes,name='medical_notes'),
    path('search_history',views.search_history,name='search_history'),
    path('save_current_checkup_rec',views.save_current_checkup_rec,name='save_current_checkup_rec'),
    path('reports',views.reports,name='reports'),
    path('settings',views.settings,name='settings'),
    path('myhistory',views.myhistory,name='myhistory'),
    path('physicaly_fit',views.physicaly_fit,name='physicaly_fit'),
    path('pdftest',views.pdftest,name='pdftest'),
    path('save_code',views.save_code,name='save_code'),
    
    path('privacy-policy',views.privacy_policy,name='privacy_policy'),
    path('notifications',views.notifications,name='notifications'),
    path('view-notif/<int:id>',views.view_notif,name='view_notif'),
    
    
    #reports
    path('reports/inventory',views.reports_inventory,name='reports_inventory'),
    path('reports/user-visit-history/<int:id>',views.reports_user_visit_history,name='user_visit_history'),
]

