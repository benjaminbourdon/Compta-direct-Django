import csv
import io
import re
from datetime import datetime

from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .forms import ImportFileForm
from .models import User


class ImportFileView(SuccessMessageMixin, FormView):
    form_class = ImportFileForm
    template_name = "importfile.html"
    success_url = "#"
    success_message = _("Imported successfully")

    def form_valid(self, form):
        read_csv = csv.DictReader(io.StringIO(form.cleaned_data["file"]))

        if form.cleaned_data["category"] == ImportFileForm.CategoryFile.MEMBER_LIST:
            count_new_members = self._import_member_list_from_csv(read_csv)
            self.success_message += f" ({count_new_members} member(s) added)"

        return super().form_valid(form)

    @transaction.atomic
    def _import_member_list_from_csv(dictreader):
        count_new_members = 0
        for line in dictreader:
            try:
                validate_email(line["Email"])
            except ValidationError:
                pass
            else:
                user_values = {
                    "first_name": line["Prénom"],
                    "last_name": line["Nom"],
                    "gender": User.Gender.MEN
                    if line["Sexe"] == "Masculin"
                    else User.Gender.WOMEN,
                    "phone_number": line["Téléphone mobile"]
                    if line["Téléphone mobile"] != ""
                    else None,
                    "date_of_birth": datetime.strptime(
                        line["Date de naissance"], "%d/%m/%Y"
                    )
                    if line["Date de naissance"]
                    else None,
                }
                user, is_new = User.objects.update_or_create(
                    email=line["Email"], defaults=user_values
                )
                if is_new:
                    count_new_members += 1
                    user.is_active = False

                user.profile_ac.idContact = line["ID du Contact"]
                user.profile_ac.member_revo = (
                    True
                    if re.match("Adhérent", line["Statut adhérent"]) is not None
                    else False
                )
                user.profile_ac.member_CS = line["Membre annuels (aides CS)"] != ""
                user.profile_ac.detail_url = line["Détail"]
                user.profile_ac.last_check = datetime.today()

                user.save()

        return count_new_members
