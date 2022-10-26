from django.contrib import admin
from .models import Card, Tile


class TileInLine(admin.StackedInline):
    model = Tile
    extra = 5


class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', ]}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [TileInLine]


admin.site.register(Card, CardAdmin)
