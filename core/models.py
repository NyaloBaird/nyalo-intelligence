from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompanyInfo(TimeStampedModel):
    name = models.CharField(max_length=150, default="Nyalo Intelligence")
    tagline = models.CharField(max_length=255, blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    owner_primary = models.CharField(max_length=150, blank=True)
    owner_secondary = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class Department(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    order = models.PositiveIntegerField(default=0)
    theme_primary = models.CharField(
        max_length=7, default="#0ea5e9", help_text="Primary HEX color for this department"
    )
    theme_accent = models.CharField(
        max_length=7, default="#38bdf8", help_text="Accent HEX color for this department"
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class DepartmentHighlight(models.Model):
    department = models.ForeignKey(
        Department, related_name="highlights", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.department.name}: {self.text}"


class Artist(TimeStampedModel):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    youtube_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ArtistStat(models.Model):
    artist = models.ForeignKey(Artist, related_name="stats", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.artist.name}: {self.text}"
