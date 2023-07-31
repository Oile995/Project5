from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify



HOMEPAGE_DEAL = ((0, "Not visable in Homepage carousel"), (1, "Visable in Homepage carousel"))


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'


    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class SubCategory(models.Model):

    class Meta:
        verbose_name_plural = 'SubCategories'


    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    subcategory = models.ForeignKey('SubCategory', null=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True, editable=False)
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True, editable=False)
    brand = models.CharField(max_length=254)
    description = models.TextField()
    specification = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
        )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    active_deal = models.IntegerField(choices=HOMEPAGE_DEAL, default=0)

    def generate_sku(self):
        """
        Helper function to generate a SKU,
        rgo = first 3 char in brand name
        ctg = category 
        sctg = subcategory
        cs = product name
        """
        rgo = self.brand[0:3]
        ctg = self.subcategory.category.friendly_name
        print(ctg)
        if "AC" in ctg:
            ctg = "AC"
        else:
            ctg = ctg[0:3]
        sctg = self.subcategory.name
        namelist = sctg.split("-")
        sctg_name = ""
        for i in namelist:
            sctg_name += i[0]
        sctg = sctg_name
        cs = self.name[0:3]
        generated_sku = rgo + ctg + sctg + cs
        return generated_sku

    # auto-set slug as name with slugify
    # from https://stackoverflow.com/questions/50436658/how-to-auto-generate-slug-from-my-album-model-in-django-2-0-4
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.sku:
            self.sku = generate_sku()
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.comment