from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe

from Web.utils import BaseModel, ImageModel, STATES


# Create your models here.
class Icon(models.Model):
    name = models.CharField(max_length=150, unique=True)
    class_or_id = models.CharField(max_length=150, null=True, blank=True)
    icon_style = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Localisation(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    lot = models.CharField(max_length=15)
    state = models.CharField(max_length=250, choices=STATES)
    zip_code = models.CharField(max_length=10)
    map = models.TextField(blank=True)

    def admin_map(self):
        return mark_safe(f"{self.map}")

    def __str__(self):
        return f"{self.lot} {self.city} {self.state}"


class Contact(BaseModel):
    value = models.CharField(max_length=15)
    privilege = models.BooleanField(default=False, null=True)
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.value


class Degree(BaseModel):
    name = models.CharField(max_length=150)
    stars = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
        choices=[(i, str(i)) for i in range(6)], null=True, blank=True
    )

    def __str__(self):
        return self.name


class Email(BaseModel):
    value = models.CharField(max_length=250)
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.value


class Web(BaseModel):
    title = models.CharField(max_length=150)
    url = models.URLField()
    privilege = models.BooleanField(default=False, null=True)
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Social(BaseModel):
    title = models.CharField(max_length=150)
    url = models.URLField()
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Introduction(BaseModel):
    title = models.CharField(max_length=150)
    introduction = models.TextField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title


class Profile(BaseModel, ImageModel):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    pseudo = models.CharField(max_length=50)
    birthday = models.DateField()
    degrees = models.ManyToManyField(Degree, blank=True)
    socials = models.ManyToManyField(Social, blank=True)
    web = models.ForeignKey(Web, on_delete=models.CASCADE, null=True, blank=True)
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Fact(models.Model):
    count = models.IntegerField(blank=True, null=True)
    phrase_begin = models.CharField(max_length=100, null=True)
    phrase_end = models.CharField(max_length=150, null=True)
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.phrase_begin} {self.phrase_end}"


class Competence(ImageModel):
    name = models.CharField(max_length=150)
    rate = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ], blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rate']


class Skill(BaseModel):
    libel = models.TextField()
    competences = models.ManyToManyField(Competence)

    def __str__(self):
        return self.libel


class List(models.Model):
    value = models.CharField(max_length=250)

    def __str__(self):
        return self.value


class Education(models.Model):
    title = models.CharField(max_length=150)
    begin = models.CharField(max_length=100, null=True, blank=True)
    end = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    details = models.TextField()

    def __str__(self):
        return self.title


class Experience(models.Model):
    title = models.CharField(max_length=150)
    begin = models.CharField(max_length=100, null=True, blank=True)
    end = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    lists = models.ManyToManyField(List, blank=True)

    def __str__(self):
        return self.title


class Summary(models.Model):
    title = models.CharField(max_length=150)
    details = models.TextField()
    lists = models.ManyToManyField(List, blank=True)

    def __str__(self):
        return self.title


class SectionType(BaseModel):
    value = models.CharField(unique=True, max_length=50)
    icons = models.ForeignKey(Icon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.value


class Section(BaseModel):
    title = models.CharField(unique=True, max_length=150)
    type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    libel = models.TextField()

    def __str__(self):
        return self.title


class ImagePortfolio(ImageModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class CategoryPortfolio(BaseModel):
    name = models.CharField(max_length=150)
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ClientPortfolio(ImageModel):
    name = models.CharField(unique=True, max_length=150)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Portfolio(BaseModel):
    name = models.CharField(max_length=150)
    url = models.URLField(blank=True)
    details = models.TextField()
    begin = models.DateField()
    end = models.DateField(blank=True)
    category = models.ForeignKey(CategoryPortfolio, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientPortfolio, on_delete=models.CASCADE)
    images = models.ManyToManyField(ImagePortfolio)

    def __str__(self):
        return self.name
