import csv
import io
import re
import json
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .forms import ImportFileForm
from .models import User, Transaction


class ImportFileView(SuccessMessageMixin, FormView):
    form_class = ImportFileForm
    template_name = "importfile.html"
    success_url = "#"
    success_message = _("Imported successfully")

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        if form.cleaned_data["category"] == ImportFileForm.CategoryFile.MEMBER_LIST:
            count_new_members = self._import_member_list_from_csv(file)
            self.success_message += f" ({count_new_members} member(s) added)"
        elif (
            form.cleaned_data["category"]
            == ImportFileForm.CategoryFile.TRANSACTION_LIST
        ):
            count_new_transactions = self._import_transactions_from_json(file)
            self.success_message += f" ({count_new_transactions} transaction(s) added)"
        elif form.cleaned_data["category"] == ImportFileForm.CategoryFile.BALANCES_LIST:
            self._import_initial_current_amount_from_csv(file)
            self.success_message += " (balances updated)"
        return super().form_valid(form)

    @transaction.atomic
    def _import_member_list_from_csv(self, file):
        dictreader = csv.DictReader(io.StringIO(file))

        count_new_members = 0
        for line in dictreader:
            try:
                validate_email(line["Email"].strip())
            except ValidationError:
                pass
            else:
                gender = line.get("Sexe")
                if gender == "Masculin":
                    gender = User.Gender.MEN
                elif gender == "Féminin":
                    gender = User.Gender.WOMEN
                else:
                    gender = User.Gender.UNSPECIFIED

                user_values = {
                    "first_name": line.get("Prénom"),
                    "last_name": line.get("Nom"),
                    "gender": gender,
                    "phone_number": line.get("Téléphone mobile")
                    or line.get("Téléphone mobile"),
                    "date_of_birth": datetime.strptime(
                        line["Date de naissance"], "%d/%m/%Y"
                    )
                    if line.get("Date de naissance")
                    else None,
                }

                user, is_new = User.objects.update_or_create(
                    email=line["Email"], defaults=user_values
                )
                if is_new:
                    count_new_members += 1
                    user.is_active = False

                user.profile_ac.idContact = line.get("ID du Contact")
                user.profile_ac.member_revo = (
                    True
                    if line.get("Statut adhérent")
                    and re.match("Adhérent", line["Statut adhérent"])
                    else False
                )
                user.profile_ac.member_CS = line.get("Membre annuels (aides CS)") != ""
                user.profile_ac.detail_url = line.get("Détail")
                user.profile_ac.last_check = datetime.today()

                user.save()

        return count_new_members

    @staticmethod
    def _amount_to_decimal(amount):
        return Decimal(amount.replace(",", ".").replace("\u202f", ""))

    def _import_transactions_from_json(self, json_file):
        list = json.loads(json_file)
        count_new_transactions = 0

        for transaction_data in list:
            if transaction_data["user_id"] in (
                "7993922",
                "8384240",
                "8845003",
                "8716849",
            ):
                continue

            if transaction_data["Crédit (EUR)"]:
                amount = self._amount_to_decimal(transaction_data["Crédit (EUR)"])
            elif transaction_data["Débit (EUR)"]:
                amount = -1 * self._amount_to_decimal(transaction_data["Débit (EUR)"])
            else:
                amount = None

            transaction_values = {
                "user": User.objects.get(
                    profile_ac__idContact=transaction_data["user_id"]
                ),
                "idDocument": transaction_data["Id pièce"],
                "provided_title": transaction_data["Intitulé"],
                "amount": amount,
                "date_event": datetime.strptime(transaction_data["Date"], "%d/%m/%Y"),
                "is_deleted": False,
            }
            transaction, is_new = Transaction.objects.update_or_create(
                entity_id=transaction_data["entity_id"], defaults=transaction_values
            )
            if is_new:
                count_new_transactions += 1

        return count_new_transactions

    def _import_initial_current_amount_from_csv(self, file):
        pass
