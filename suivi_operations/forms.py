from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _


class ImportFileForm(forms.Form):
    class CategoryFile(models.TextChoices):
        MEMBER_LIST = "Members", _("List of members")
        OPERATIONS_LIST = "Operations", _("List of operations")

    file = forms.FileField(
        label=_("file to import"),
        required=True,
        allow_empty_file=False,
        widget=forms.FileInput,
    )
    category = forms.ChoiceField(label=_("file category"), choices=CategoryFile.choices)
