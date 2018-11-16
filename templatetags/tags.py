#__author:  Administrator
#date:  2017/1/5

from django import template
from django.utils.safestring import mark_safe
from king_admin.utils import prn_obj
register = template.Library()

@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(obj,admin_class):
    # print("11111111111")
    # prn_obj(obj)
    # print("11111111111")
    row_ele = ""
    for column in admin_class.list_display:
        #obj为全部字段结果，column为需要显示的字段
        field_obj = obj._meta.get_field(column)
        # print("222222")
        # prn_obj(field_obj)
        # print("222222")
        if field_obj.choices:#choices type
            column_data = getattr(obj,"get_%s_display" % column)()
            # print("55555555555555")
            # print(column,obj.get_status_display)
            # print("55555555555555")
            # # print("%s 3333333333"%column)
            #
            # print(dir(obj._meta))
            # print(column_data)
            #
            # print("%s 33333333333"%column)
        else:
            column_data = getattr(obj,column)
        print(type(column_data))
        if type(column_data).__name__ == 'datetime':
            print(1111111)
            print(type(column_data))
            # prn_obj(column_data)
            print(1111111111)
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)

@register.simple_tag
def build_paginations(query_sets,filter_condtions,previous_orderby):
    print("build_paginations1111111111111111111111111111111111111111111")
    set_previous_orderby=""
    if previous_orderby != "":
        set_previous_orderby="&o=%s"%(previous_orderby)
    page_btn=""
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
            page_btn += '''<li class=%s><a href="?page=%s%s%s">%s</a></li>'''%(ele_class,page_num,filters,set_previous_orderby,page_num)

        else :
              print("page_ref:%s,page_num:%s" % (page_ref, page_num))
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
        print(filter_condtions)
        print(k,v,"condtionsssssssssss")
        filter_condtions_ele+="&%s=%s"%(k,v)

    if loop_counter <  3  or loop_counter > query_sets.paginator.num_pages -2:   #代表这是前两页 或 最后两页，要显示
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,filter_condtions_ele,loop_counter)

        print("我是%s"%loop_counter,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

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
def build_table_header_column(column, orderby_key,filter_condtions):
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

    ele = ele.format(orderby_key=orderby_key,filters=filters,column=column,up_down=up_down)
    return mark_safe(ele)


@register.simple_tag
def set_orderbykey(column,orderby_key):
    print("我是orderby_key:",orderby_key)
    if orderby_key.strip("-") == column:
        if orderby_key.startswith("-"):
            print("我是排序----------------------------------")
            return column
        else:
            return "-%s"%column
    else:
        return column


@register.simple_tag
def render_filter_ele(condtion,admin_class,filter_condtions):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %condtion

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
            print("choice",choice_item,filter_condtions.get(condtion),type(filter_condtions.get(condtion)))
            print("filter_condtions:",filter_condtions)
            if filter_condtions.get(condtion) == str(choice_item[0]):
                #filter_condtions 为当前GET 请求处理过的 过滤参数，类型为字典
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''
    print("type(field_obj)",type(field_obj))
    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)