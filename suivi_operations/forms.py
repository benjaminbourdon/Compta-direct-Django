import csv
import io

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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
        validators=[FileExtensionValidator(["csv"])],
        help_text=_("File must be CSV text type."),
    )
    category = forms.ChoiceField(label=_("file category"), choices=CategoryFile.choices)

    def clean(self):
        cleaned_data = super().clean()

        if "file" in cleaned_data:
            file = cleaned_data["file"].read()
            try:
                decoded_file = file.decode("utf-8")
            except UnicodeDecodeError:
                # Could be a validator or extend to more encodings
                raise ValidationError(_("File must be encode with UTF-8."))
            else:
                cleaned_data["file"] = decoded_file
                read_csv = csv.DictReader(io.StringIO(decoded_file))

                if cleaned_data["category"] == ImportFileForm.CategoryFile.MEMBER_LIST:
                    if "Email" not in read_csv.fieldnames:
                        raise ValidationError(
                            _('CSV file doesn\'t have an "Email" colomn.')
                        )
        return cleaned_data
