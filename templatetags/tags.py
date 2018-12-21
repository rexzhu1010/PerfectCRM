#__author:  Administrator
#date:  2017/1/5

from django import template
from django.utils.safestring import mark_safe
from king_admin.utils import prn_obj
from django.utils.timezone import datetime,timedelta
register = template.Library()
from django.core.exceptions import FieldDoesNotExist
from  crm import models
from django.db.models import Sum
@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    # print("11111111111")
    # prn_obj(obj)
    # print("11111111111")
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        #obj为一行数据全部字段结果，column为需要显示的字段
        try:
            field_obj = obj._meta.get_field(column)

            if field_obj.choices:#choices type
                column_data = getattr(obj,"get_%s_display" % column)()
            else:
                column_data = getattr(obj,column)
            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
            if index == 0:  # 在第一列增加 a 标签，跳到change
               column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,obj_id=obj.id,data=column_data)

        #处理数据库里没有的 自定义字段
        except FieldDoesNotExist as e:
                if hasattr(admin_class,column):
                    column_fun = getattr(admin_class,column)
                    admin_class.instance = obj
                    admin_class.request = request
                    column_data =  column_fun()
        row_ele += "<td>%s</td>" % column_data




    return mark_safe(row_ele)

@register.simple_tag
def build_paginations(query_sets,filter_condtions,previous_orderby,search_q):
    # print("build_paginations1111111111111111111111111111111111111111111")
    set_previous_orderby=""
    if previous_orderby != "":
        set_previous_orderby="&o=%s"%(previous_orderby)
    page_btn=""

    s_q=""
    if search_q !="":
        s_q="&_q=%s"%(search_q)
    for page_num in query_sets.paginator.page_range:
        filters=""
        for k,v in filter_condtions.items():
            filters +="&%s=%s"%(k,v)

    page_ref = 0
    for page_num in query_sets.paginator.page_range:

        if  page_num  < 2  or page_num > query_sets.paginator.num_pages - 1 \
                or abs(query_sets.number - page_num) <= 1 :  #代表最前面2页和最后面两页   or # 这里用了 abs  ，abs(-1)=1 ,判断当前面的前后两页
            ele_class = ""
            if query_sets.number == page_num:
                ele_class = "active"
            page_btn += '''<li class=%s><a href="?page=%s%s%s%s">%s</a></li>'''%(ele_class,page_num,filters,set_previous_orderby,s_q,page_num)

        else :
              # print("page_ref:%s,page_num:%s" % (page_ref, page_num))
              if page_ref + 1 == page_num:
                  # print("page_ref:%s,page_num:%s"%(page_ref,page_num))
                  page_ref = page_num
                  continue
              page_btn += '''<li><a>...</a></li>'''
              page_ref = page_num
        #print(page_btn)
    return mark_safe(page_btn)


@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_condtions):

    filter_condtions_ele=""
    for k,v in filter_condtions.items():
        # print(filter_condtions)
        # print(k,v,"condtionsssssssssss")
        filter_condtions_ele+="&%s=%s"%(k,v)

    if loop_counter <  3  or loop_counter > query_sets.paginator.num_pages -2:   #代表这是前两页 或 最后两页，要显示
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,filter_condtions_ele,loop_counter)

        # print("我是%s"%loop_counter,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

        return mark_safe(ele)



    if abs(query_sets.number - loop_counter) <= 1: #这里用了 abs  ，abs(-1)=1
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,filter_condtions_ele,loop_counter)
        print("我是%s,当前页是%s" % (loop_counter,query_sets.number), "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

        return mark_safe(ele)

    return '...'



@register.simple_tag
def build_table_header_column(column, orderby_key,filter_condtions,admin_class):
    #< th > < ahref = "?o={% set_orderbykey column orderby_key %}" > {{column}}  < / a > < / th >
    #< spanclass ="glyphicon glyphicon-menu-down" aria-hidden="true" > < / span >




    filters = ""
    for k, v in filter_condtions.items():
        # if filter_condtions[k]:
            filters += "&%s=%s" % (k, v)

    # print("filtersfiltersfiltersfiltersfiltersfiltersfiltersfilters",filters)
    ele = '''<th> <a href ="?o={orderby_key}{filters}"> {column}</a>{up_down}</th>'''
    up="<span class ='glyphicon glyphicon-triangle-bottom' aria-hidden='true'></span>"
    down = "<span class ='glyphicon glyphicon-triangle-top' aria-hidden='true'></span>"
    if orderby_key.strip("-") == column:
        orderby_key = orderby_key
        if orderby_key.startswith("-"):
            up_down = up
        else:
            up_down = down
    else:
        orderby_key = column
        up_down=""
    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name
    except FieldDoesNotExist as e:
        column_verbose_name = getattr(admin_class,column).display_name
        # return column_verbose_name
        ele = mark_safe('''<th><a href="#">%s</a></th>'''%column_verbose_name)
    ele = ele.format(orderby_key=orderby_key,filters=filters,column=column_verbose_name,up_down=up_down)
    return mark_safe(ele)


@register.simple_tag
def set_orderbykey(column,orderby_key):
    # print("我是orderby_key:",orderby_key)
    if orderby_key.strip("-") == column:
        if orderby_key.startswith("-"):
            print("我是排序----------------------------------")
            return column
        else:
            return "-%s"%column
    else:
        return column


@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_condtions,selectdate):
    select_ele = '''<select class="form-control" name='{filter_name}' ><option value=''>----</option>'''

    #field_obj为字段属性类，condtion 为需要过滤的 表字段，下面通过_meta方法 获得该字段的属性
    field_obj = admin_class.model._meta.get_field(condtion)

    # dir(admin_class.model._meta)
    # print("field_obj ---------------:")
    # prn_obj(field_obj)
    # print("end obj ---------------")
    # print("meta  :  ",dir(admin_class.model._meta))
    #判断该字段属性choices不为空
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            # print("choice",choice_item,filter_condtions.get(condtion),type(filter_condtions.get(condtion)))
            # print("filter_condtions:",filter_condtions)
            if filter_condtions.get(condtion) == str(choice_item[0]):
                #filter_condtions 为当前GET 请求处理过的 过滤参数，类型为字典
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''
    # print("type(field_obj)",type(field_obj))
    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''

    if type(field_obj).__name__ in ['DateTimeField','DateField']:
        date_els = []
        today_ele =  datetime.now().date()
        date_els.append(["今天",today_ele ])
        date_els.append(["昨天", today_ele - timedelta( days=1) ])
        date_els.append(["近7天", today_ele - timedelta( days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele- timedelta(days=90)])
        date_els.append(["本年", today_ele .replace(month=1,day=1)])
        date_els.append(["365天", today_ele- timedelta(days=365)])

        for d in date_els:
            print(type(str(selectdate)),type(str(d[1])))
            selected = ""
            if selectdate :
                print("111111111111111111111111111111111111")
                if selectdate == str(d[1]):
                   print(d[1],222222222222222222222222)
                   selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>'''%(d[1],selected,d[0])

        filter_field_name = "%s__gte"%condtion
    else:
        filter_field_name = condtion
    select_ele = select_ele.format(filter_name=filter_field_name)

    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def get_model_name(admin_class):

    return  admin_class.model._meta.verbose_name



@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    #返回select 中待选数据, 这里field 没有写死，适合所有

    all_obj_list = getattr(admin_class.model,field.name).rel.model.objects.all()  #表结构中取出 的  所有select数据
    print("我是  get_m2m_obj_list")

    if not form_obj.instance.id:
        print("我是  get_m2m_obj_list")
        return all_obj_list

    selected_obj_list = getattr(form_obj.instance, field.name).all()  # 单条数据  已选select数据

    standy_obj_list = []
    for  obj  in all_obj_list:
        if obj  not in selected_obj_list:
            standy_obj_list.append(obj)

    return standy_obj_list

@register.simple_tag
def get_m2m_selected_list(form_obj,field):
    #返回已选择的M2m 数据
    if not form_obj.instance.id:
        return None
    selected_obj=getattr(form_obj.instance,field.name).all()
    print("selected:",selected_obj)
    return  selected_obj


@register.simple_tag
def display_obj_related(objs):


    html_ele=""

    for obj in objs:
        html_ele += "<ul><li>%s :%s</li>" % (obj._meta.verbose_name,obj)
        html_ele += recursive_related_objs_lookup(obj)
        html_ele +="</ul>"





    return mark_safe(html_ele)




def recursive_related_objs_lookup(obj):

    html_ele=""
    temp_ele=""
    for otm_obj in obj._meta.related_objects:   #循环对像中 有关联的表
        # if "ManyToOneRel" not in otm_obj.__repr__():
        #     continue
        if hasattr(otm_obj,"get_accessor_name"):
           temp_set_name = otm_obj.get_accessor_name()

           if getattr(obj, temp_set_name).all() :
               temp_ele += "<ul>"

               for i in getattr(obj,temp_set_name).all():
                   temp_ele += "<li>%s : %s</li>  "%(i._meta.verbose_name,i)
                   # print(html_ele)
                   if len(i._meta.related_objects) > 0 :
                            temp_ele += recursive_related_objs_lookup(i)

               temp_ele += "</ul>"
           else:
               print("temp_set_name 是空的:", temp_set_name)
               continue

               # break

        # break

    if (len(obj._meta.local_many_to_many) > 0):
        temp_ele += "<ul>"
        for mtm_obj in obj._meta.local_many_to_many:

            v = getattr(obj, mtm_obj.name).all()  # = getattr(customer,tags).all()

            for i in v:
                temp_ele += "<li>%s : %s</li>" % (mtm_obj.name, i)
                # if len(i._meta.local_many_to_many) > 0:
                #     html_ele = recursive_related_objs_lookup(i, html_ele)
        temp_ele += "</ul>"

    html_ele+=temp_ele




    return html_ele




def recursive_related_objs_lookup2(objs):
    #model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele += li_ele

        #for local many to many
        #print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来了
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name) #getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():# customer.tags.select_related()
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  #最终跟最外层的ul相拼接


        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()): # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                #上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj,'select_related'): # slect_related() == all()
                    target_objs = accessor_obj.select_related() #.filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) >0:
                    #print("\033[31;1mdeeper layer lookup -------\033[0m")
                    #nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele


@register.simple_tag
def render_enroll_contract(enroll_obj):
    return enroll_obj.enrollment_class.contract.template.format(course=enroll_obj.enrollment_class.course,customer=enroll_obj.customer.name)



@register.simple_tag
def get_action_name(admin_class,action):
    func = getattr(admin_class,action)
    if  hasattr( func,"display_name"):
        return func.display_name
    else:
        return action

@register.simple_tag
def get_score(request,enroll_obj):

    study_records = models.StudyRecord.objects.filter(student=enroll_obj)

    study_records2 = enroll_obj.studyrecord_set.filter(course_record__from_class_id = enroll_obj.enrollment_class.id)
    # study_records = enroll_obj.enrollment_class.courserecord
    return study_records.aggregate(Sum('score'))['score__sum']
