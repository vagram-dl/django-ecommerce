from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Например: 'Смартфоны','Ноутбуки'"
    )

    slug = models.SlugField(
        max_length=100,
        unique = True,
        blank = True,
        verbose_name = "URL-адрес",
        help_text = "Автоматически заполняется из названия. Например: 'smartfony'"
    )

    parent = models.ForeignKey(
         'self',
         on_delete=models.CASCADE,
         null = True,
         blank = True,
         related_name = 'children',
         verbose_name = "Родительская категория",
         help_text = "Выберите родительскую категорию или оставьте пустым для корневой"

     )

    order = models.IntegerField(
        default = 0,
        verbose_name = "Порядок сортировки",
        help_text = "Чем меньше число, тем выше в списке"
    )

    is_active = models.BooleanField(
        default = True,
        verbose_name = "Активна",
        help_text = "Отображать категорию на сайте"
    )

    description = models.TextField(
        blank = True,
        verbose_name = "Описание",
        help_text = "Используется для SEO и отображения на странице категории"
    )

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="SEO заголовок",
        help_text="Для поисковиков.Если пусто - используем название"
    )

    seo_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="SEO описание",
        help_text="Короткое описание для поиска (до 160 символов)"
    )

    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")



    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name

# Create your models here.
