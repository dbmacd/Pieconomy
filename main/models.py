from django.contrib.auth.models import User
from django.db import models


class BootstrapColours(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Allergens(models.Model):
    name = models.TextField()
    colour = models.ForeignKey(BootstrapColours, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class PieList(models.Model):
    name = models.TextField()
    cost = models.DecimalField(decimal_places=2, max_digits=5)
    to_json: models.JSONField()
    image_url = models.ImageField()
    image_alt_text = models.TextField()
    heading_text = models.TextField(max_length=50)
    blurb_text = models.TextField(max_length=100)
    button_text = models.TextField(max_length=20)
    button_link = models.TextField()
    show_in_shop = models.BooleanField(default=True)
    heading_text_style = models.TextField(default='text-dark')
    blurb_text_style = models.TextField(default='text-dark')
    button_style = models.TextField(default='btn-primary')
    allergens = models.ManyToManyField(Allergens)
    sort_order = models.IntegerField(default=1)
    ingredients = models.TextField()

    def __str__(self):
        return self.name


class Pies(models.Model):
    pie_id = models.ForeignKey(PieList, on_delete=models.RESTRICT)
    to_json: models.JSONField()
    quantity: models.IntegerField()
    can_afford: models.BooleanField()

    def __str__(self):
        return self.pie_id.name


class NutritionalInfo(models.Model):
    pie_id = models.ForeignKey(PieList, on_delete=models.RESTRICT)
    serving_size = models.IntegerField()
    energy_di = models.IntegerField(default=8700)
    energy = models.IntegerField()
    protein_di = models.IntegerField(default=50)
    protein = models.IntegerField()
    fat_di = models.IntegerField(default=70)
    fat = models.IntegerField()
    carbohydrate_di = models.IntegerField(default=310)
    carbohydrate = models.IntegerField()
    sodium_di = models.IntegerField(default=2300)
    sodium = models.IntegerField()

    def __str__(self):
        return self.pie_id.name

    @property
    def energy_di_percent(self):
        return round(self.energy / self.energy_di * 100)

    @property
    def protein_di_percent(self):
        return round(self.protein / self.protein_di * 100)

    @property
    def fat_di_percent(self):
        return round(self.fat / self.fat_di * 100)

    @property
    def carbohydrate_di_percent(self):
        return round(self.carbohydrate / self.carbohydrate_di * 100)

    @property
    def sodium_di_percent(self):
        return round(self.sodium / self.sodium_di * 100)

    @property
    def energy_per_100(self):
        return round(self.energy / self.serving_size * 100)

    @property
    def protein_per_100(self):
        return round(self.protein / self.serving_size * 100, 1)

    @property
    def fat_per_100(self):
        return round(self.fat / self.serving_size * 100, 1)

    @property
    def carbohydrate_per_100(self):
        return round(self.carbohydrate / self.serving_size * 100, 1)

    @property
    def sodium_per_100(self):
        return round(self.sodium / self.serving_size * 100)


class PieHeaders(models.Model):
    pie_data = models.ForeignKey(PieList, on_delete=models.RESTRICT)
    button_text = models.TextField(max_length=20)
    button_link = models.TextField()
    show_on_header = models.BooleanField()
    heading_text_style = models.TextField(default='text-dark')
    blurb_text_style = models.TextField(default='text-dark')
    button_style = models.TextField(default='btn-primary')


class CarouselItems(models.Model):
    image_url = models.ImageField()
    image_alt_text = models.TextField()
    heading_text = models.TextField(max_length=50)
    blurb_text = models.TextField(max_length=100)
    button_text = models.TextField(max_length=20)
    button_link = models.TextField()
    show_on_carousel = models.BooleanField()
    is_first = models.BooleanField()
    left_align = models.BooleanField(default=True)
    heading_text_style = models.TextField(default='text-dark')
    blurb_text_style = models.TextField(default='text-dark')
    button_style = models.TextField(default='btn-primary')


class FeaturedItems(models.Model):
    image_url = models.ImageField()
    image_alt_text = models.TextField()
    heading_dark_text = models.TextField(max_length=50)
    heading_light_text = models.TextField(max_length=100)
    blurb_text = models.TextField(max_length=200)
    show_on_page = models.BooleanField()
    left_align = models.BooleanField(default=True)


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    is_ordered = models.BooleanField(default=False)
    create_date_time = models.DateTimeField(null=True, blank=True)
    last_updated_date_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.is_ordered:
            qs = type(self).objects.filter(is_ordered=False, user_id=self.user_id.id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            qs.update(is_ordered=True)
        super(Orders, self).save(*args, **kwargs)

    @property
    def sub_total(self):
        order_items = OrderItems.objects.filter(order_id=self.id)
        return sum([item.item_id.cost*item.quantity for item in order_items])


class OrderItems(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.RESTRICT)
    item_id = models.ForeignKey(PieList, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)

