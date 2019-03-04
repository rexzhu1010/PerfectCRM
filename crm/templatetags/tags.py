from django import template
from django.utils.safestring import mark_safe
from king_admin.utils import prn_obj
from django.utils.timezone import datetime,timedelta
register = template.Library()
from django.core.exceptions import FieldDoesNotExist
# rex.zhu


@register.simple_tag
def render_enroll_contract(request,enroll_obj):
    return enroll_obj.enrollment_class.contract.template.format(course=enroll_obj.enrollment_class.course,customer=enroll_obj.customer.name)

