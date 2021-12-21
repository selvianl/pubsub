from django.contrib import admin

from api.models import RestaurantCategory, Restaurant, Food

# Register your models here.


class RestaurantCategoryAdmin(admin.ModelAdmin):
    pass


class RestaurantAdmin(admin.ModelAdmin):
    pass


class FoodAdmin(admin.ModelAdmin):
    pass


admin.site.register(RestaurantCategory, RestaurantCategoryAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Food, FoodAdmin)
