from auctions.models import User
from django.contrib import admin
from .models import ArticleType, ActiveListing, Bids, User, Watchlist, Comment, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(ArticleType)
admin.site.register(ActiveListing)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bids)