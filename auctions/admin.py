from django.contrib import admin
from .models import User, Categories, Listings, Bids, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
