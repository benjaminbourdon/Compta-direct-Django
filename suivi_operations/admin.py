from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from suivi_operations.models import ProfileAC, User

# Inspired by
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Password don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "date_of_birth",
            "is_active",
            "is_staff",
        ]


class ProfilAcInline(admin.StackedInline):
    model = ProfileAC
    can_delete = False
    verbose_name = _("AssoConnect profil")
    verbose_name_plural = _("AssoConnect profiles")


class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "last_login",
    ]
    ordering = ["last_name", "first_name", "email"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email"]
    filter_horizontal = []
    inlines = [ProfilAcInline]

    form = UserChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "phone_number",
                    "date_of_birth",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
