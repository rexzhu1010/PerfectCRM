
#models 在crm 中 所要要写 crm ，不能写king_admin

from king_admin import permission_hook
perm_dic = {
    'crm_table_index':['table_index','GET',[],{},],
    'crm_table_list':['table_objs','GET',["consultant"],{},permission_hook.view_my_own_coustomer],
    'crm_table_objs_change_view':['table_objs_change','GET',[],{}],
    'crm_table_objs_change':['table_objs_change','POST',[],{}],
    'crm_table_objs_add_view':['table_objs_add','GET',[],{}],
    'crm_table_obj_add':['table_objs_add','POST',[],{}],
    'crm_table_obj_delete_view':['obj_delete','GET',[],{}],
    'crm_table_obj_delete':['obj_delete','POST',[],{}],

}

# url(r'(\w+)/(\w+)/(\d+)/change/password/$', views.password_reset, name="password_reset"),
# url(r'(\w+)/(\w+)/(\d+)/change/$', views.table_objs_change, name="table_objs_change"),
# url(r'(\w+)/(\w+)/add/$', views.table_objs_add, name="table_objs_add"),
# url(r'(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name="obj_delete"),
# url(r'(\w+)/(\w+)/$', views.display_table_objs, name="table_objs"),
# url(r'\w+/$', views.index, name="table_index")
