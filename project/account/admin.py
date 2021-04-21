from django.contrib import admin
from account.models import Account, Profile

# register Account and Profile models to be seen in the admin page
admin.site.register(Account)
admin.site.register(Profile)