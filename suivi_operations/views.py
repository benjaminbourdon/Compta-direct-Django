from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from .forms import ImportFileForm


class ImportFileView(SuccessMessageMixin, FormView):
    form_class = ImportFileForm
    template_name = "importfile.html"
    success_url = "#"
    success_message = _("Imported successfully")
