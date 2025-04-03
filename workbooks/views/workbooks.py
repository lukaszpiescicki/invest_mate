from django.views.generic import DetailView

from ..models import Workbook


class WorkbookDetailView(DetailView):
    model = Workbook
    template_name = "workbooks/workbook.html"
    context_object_name = "workbook"
