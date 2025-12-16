from django.contrib import admin

from .models import (
    Artist,
    ArtistStat,
    CompanyInfo,
    Department,
    DepartmentHighlight,
)


class DepartmentHighlightInline(admin.TabularInline):
    model = DepartmentHighlight
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DepartmentHighlightInline]
    ordering = ("order", "name")


class ArtistStatInline(admin.TabularInline):
    model = ArtistStat
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    inlines = [ArtistStatInline]
    ordering = ("order", "name")


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "tagline", "mission", "vision", "email", "phone", "location")


admin.site.register(DepartmentHighlight)
admin.site.register(ArtistStat)
