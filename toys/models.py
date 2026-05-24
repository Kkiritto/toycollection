from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField('Бренд', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Toy(models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычная'),
        ('rare', 'Редкая'),
        ('ultra_rare', 'Ультра-редкая'),
        ('limited', 'Лимитированная'),
        ('legendary', 'Легендарная'),
    ]

    CONDITION_CHOICES = [
        ('mint', 'Mint (идеальное)'),
        ('near_mint', 'Near Mint'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('played', 'Played'),
        ('poor', 'Poor'),
    ]

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='toys', verbose_name='Бренд')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='toys', verbose_name='Категория')
    rarity = models.CharField('Редкость', max_length=20, choices=RARITY_CHOICES, default='common')
    year = models.PositiveIntegerField('Год выпуска')
    estimated_price = models.DecimalField('Примерная рыночная цена', max_digits=12, decimal_places=2)
    condition = models.CharField('Состояние', max_length=20, choices=CONDITION_CHOICES, default='mint')
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='toys/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Игрушка'
        verbose_name_plural = 'Игрушки'
        ordering = ['-year', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.brand})"

    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'slug': self.slug})


class CollectionItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, verbose_name='Игрушка')
    personal_condition = models.CharField(
        'Моё состояние', max_length=20, choices=Toy.CONDITION_CHOICES, default='mint'
    )
    purchase_price = models.DecimalField('Цена покупки', max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField('Дата покупки', null=True, blank=True)
    notes = models.TextField('Заметки', blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'toy')
        verbose_name = 'Элемент коллекции'
        verbose_name_plural = 'Коллекция пользователя'
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.toy.title} — {self.user.username}"