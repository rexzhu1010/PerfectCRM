def table_objs_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enable_admins[app_name][table_name]
    model_form_class =  forms.create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj=model_form_class(request.POST,instance=obj) # 把新POST，和旧的OBJ 都交给 modelform 对比 才是更新
        if form_obj.is_valid():
            form_obj.save()
    else:
        form_obj= model_form_class(instance=obj)
    return  render(request,"king_admin/table_obj_change.html",{"form_obj":form_obj,"admin_class":admin_class})

def table_objs_add(request,app_name,table_name):
    admin_class = king_admin.enable_admins[app_name][table_name]
    model_form_class =  forms.create_model_form(request,admin_class)

    if request.method == "POST":
        form_obj=model_form_class(request.POST) # 把新POST，和旧的OBJ 都交给 modelform 对比 才是更新
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace("/add/","/"))
    return  render(request,"king_admin/table_obj_add.html",{"form_obj":form_obj,"admin_class":admin_class})
