from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        u = self.create_user(email=email,
                            password=password,
                            )
        u.is_admin = True
        u.is_staff = True
        u.is_superuser=True
        u.save(using=self._db)
        return u