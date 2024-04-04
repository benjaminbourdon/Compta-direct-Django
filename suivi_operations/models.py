from datetime import date

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
        help_text=_("This email also serves as identifier."),
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    class Gender(models.TextChoices):
        MEN = "M", _("Men")
        WOMEN = "W", _("Women")
        UNSPECIFIED = "U", _("Unspecified")

    gender = models.CharField(
        _("gender"),
        blank=False,
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNSPECIFIED,
        help_text=_("Gender choices are limited to existing Ultimate categories."),
    )

    phone_number = models.PositiveIntegerField(_("phone number"), null=True, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,  # Personnaliser selon présence d'un mdp
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} <{self.email}>"
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class ProfileAC(models.Model):
    """Profile contenant les informations AssoConnect des contacts"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_ac",
    )
    idContact = models.PositiveIntegerField(
        _("contact identifier"), unique=True, null=True, blank=True, default=None
    )
    initial_amount = models.DecimalField(
        _("initial balance"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    current_amount = models.DecimalField(
        _("current balance"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    member_revo = models.BooleanField(_("revolution'air membership"), default=False)
    member_CS = models.BooleanField(_("Championnet Sports membership"), default=False)
    detail_url = models.URLField(_("detail url"), blank=True)
    last_check = models.DateField(_("last check"), default=date.today)


class Transaction(models.Model):
    entity_id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    idDocument = models.PositiveIntegerField(_("document identifier"), unique=False)
    provided_title = models.CharField(_("provided title"), max_length=300)
    amount = models.DecimalField(
        _("amount"),
        max_digits=7,
        decimal_places=2,
        help_text=_(
            "Transaction amount, from the considered individual perspective."
            "So, a negative amount is a debt owned by an individuel to the club,"
            " or a paiement from the club.  "
        ),
    )
    date_event = models.DateField(_("date of the transaction"))
    last_update = models.DateTimeField(_("last check"), auto_now=True)
    imported_date = models.DateTimeField(_("date of first import"), auto_now_add=True)
    is_deleted = models.BooleanField(_("state of deletion"), default=False)

    @property
    def verbose_title(self):
        if self.amount > 0:
            if "paiement" in self.provided_title or "Paiement" in self.provided_title:
                return "Paiement recu par le club"
        if " - Transaction #" in self.provided_title:
            return self.provided_title.partition(" - Transaction #")[0]
        return self.provided_title


class Reminder(models.Model):
    datetime = models.DateTimeField(default="")
    subject = models.CharField(max_length=300)
    # type = models.TextChoices()
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    balance = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
