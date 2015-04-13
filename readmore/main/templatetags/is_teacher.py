from django import template
from readmore.main.models import Group
register = template.Library()

@register.filter(name='is_teacher')
def is_teacher(user):
	return len(Group.objects.filter(leader=user))