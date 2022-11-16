from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


class Category(models.Model):
    """Класс, описывающий модель категории"""
    name = models.CharField(max_length=200, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


def get_upload_path(category, filename):
    return f'{category.name}/{filename}'


class Product(models.Model):
    """Класс, описывающий модель отдельного продукта"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.FileField(blank=True, upload_to=get_upload_path, verbose_name='Изображения')

    # image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')

    SIZE_CHOICES = (('XXS', 'XXS'),
                    ('XS', 'XS'),
                    ('S', 'S'),
                    ('M', 'M'),
                    ('XL', 'XL'),
                    ('XXL', 'XXL'))

    sizes = MultiSelectField(choices=SIZE_CHOICES,
                             max_choices=6,
                             max_length=17)

    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


# def get_upload_path(instance, filename):
#     model = instance.album.model.__class__._meta
#     name = model.verbose_name_plural.replace(' ', '_')
#     return f'{name}/images/{filename}'


class ProductImage(models.Model):
    """Класс для хранения нескольких фото продукта"""
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name='Товар')
    images = models.FileField(upload_to=get_upload_path, verbose_name='Изображения')

    def __str__(self):
        return self.product.name

# class Size(models.Model):
#     """Класс, описывающий доступные размеры каждого товара"""
#     product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE, verbose_name='Товар')
#     sizes = models.CharField(choices=sizes)
