"""
kangaroo_automations/filters.py
"""

from kangaroo.filters import KangarooFilterSet, django_filters
from kangaroo_automations.models import MailAutomation


class AutomationFilter(KangarooFilterSet):
    """
    AutomationFilter
    """

    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = MailAutomation
        fields = "__all__"
