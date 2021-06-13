import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from ..task.settings import SECRET_KEY
import jwt

class CouriersManager(BaseUserManager):
    def create_user(self, phone, full_name, password=None):
        if not phone:
            raise ValueError("Не заполнен Телефон")
        if not full_name:
            raise ValueError("Не заполнено имя")

        user = self.model(
            phone=phone,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password):
        user = self.create_user(
            phone=phone,
            password=password,
            full_name=full_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class Couriers(AbstractBaseUser):
    phone = models.DecimalField(max_digits=12, decimal_places=0, unique=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField("Address", max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["full_name"]

    objects = CouriersManager()

    class Meta:
        # app_label = 'clients_auth'
        # db_table = 'clients_user'
        verbose_name = "Courier"
        verbose_name_plural = "Couriers"

    def __str__(self) -> str:
        return str(self.full_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = Couriers.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except Couriers.MultipleObjectsReturned:
            return None
        except Couriers.DoesNotExist:
            return None
        return None

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Обычно это имя и фамилия пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.full_name

    def get_short_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Как правило, это будет имя пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.full_name

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')



class Companies:
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateField( auto_now_add=True, null=False)
    updated_at = models.DateField( auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordered_by = ['updated_at']

    def __str__(self):
        return self.name

class Devices(models.Model):

    company_id = company = models.ForeignKey(
        Companies, verbose_name="Company", on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100, null=False)
    device_model = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    app = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordered_by = ['updated_at']

    def __str__(self):
        return self.device_model

class Locations(models.Model):
    latitude = models.DecimalField( max_digits=22, decimal_places=16)
    longitude = models.DecimalField( max_digits=22, decimal_places=16)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    company = models.ForeignKey(
        Companies, verbose_name="Company", on_delete=models.CASCADE)
    device = models.ForeignKey(
        Devices, verbose_name="Device", on_delete=models.CASCADE)
    data = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordered_by = ['updated_at']

    def __str__(self):
        return str(self.id)