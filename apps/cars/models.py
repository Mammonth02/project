from audioop import reverse
from django.db import models
from django.contrib.auth.models import User
from django.template import Origin
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model


class AutoType(models.Model):
    title = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='type_icon/', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Типы'
        verbose_name= 'Тип'


class Make(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Марки'
        verbose_name= 'Марка'

    def __str__(self):
        return f'{self.title}'

class Auto(models.Model):
    DRIVE_TYPE = (
    ('RWD', 'RWD'),
    ('FWD', 'FWD'),
    ('4WD', '4WD'),
    ('AWD', 'AWD'),
    )

    TRANSMISSION = (
        ('механическая', 'механическая'),
        ('автоматическая', 'автоматическая'),
        ('роботизированная', 'роботизированная'),
        ('бесступенчатая', 'бесступенчатая'),
    )

    CONDITION = (
    ('Новый', 'Новый'),
    ('Б/У', 'Б/У'),
    )

    FUEL_TYPE = (
    ('бензин', 'бензин'),
    ('дизель', 'дизель'),
    ('биодизель', 'биодизель'),
    ('биоэтанол', 'биоэтанол'),
    ('керосин', 'керосин'),
    ('газ', 'газ'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='пользователь')
    make = models.ForeignKey(Make, on_delete=models.CASCADE, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    color = models.CharField(max_length=100, verbose_name='Цвет')
    drive_type = models.CharField(choices=DRIVE_TYPE, max_length=20, verbose_name='Тип привода')
    transmission = models.CharField(choices=TRANSMISSION, max_length=100, verbose_name='Каробка передач')
    сondition = models.CharField(choices=CONDITION, max_length=20, verbose_name='Состояние')
    year = models.IntegerField( verbose_name='Год')
    mileage = models.IntegerField(verbose_name='Пробег')
    fuel_type = models.CharField(choices=FUEL_TYPE, max_length=50, verbose_name='Тип топлива')
    engine_size = models.IntegerField( verbose_name='Обьём мотора')
    doors = models.IntegerField(verbose_name='Двери')
    cylinders = models.IntegerField(verbose_name='Цилиндры')
    vin = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='auto/', blank=True, null=True, verbose_name='Фото')
    prise = models.IntegerField(blank=True, null=True, verbose_name='Цена')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    video_link = models.URLField(null=True, blank=True, verbose_name='Ссылка(ютуб)')
    type_auto = models.ForeignKey(AutoType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tип') 

    class Meta:
        verbose_name_plural = 'Автомабили'
        verbose_name= 'Автомабиль'
        ordering = ['-id']

    def __str__(self):
        return f'{self.make} {self.model}'

    def get_absolute_url(self):
        return reverse('single_page', kwargs={
            'id':self.pk
        }) 

class Auto_like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Лайки'
        verbose_name= 'Лайк'


class Images(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='auto_image_slider/', null=True, blank=True)
    def __str__(self):
        return f'{self.auto}'

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="50px">')
        else:
            return ''

    class Meta:
        verbose_name_plural = 'Картинки'
        verbose_name= 'Картинка'

class Reviews(models.Model):
    RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reviews = models.TextField(verbose_name='отзыв')
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    comfort = models.IntegerField(choices=RATING, verbose_name='комфорт')
    performance = models.IntegerField(choices=RATING, verbose_name='представление')
    exterior_styling = models.IntegerField(choices=RATING, verbose_name='внешний вид')
    interior_design = models.IntegerField(choices=RATING,  verbose_name='дизайн интерьера')
    value_for_the_money = models.IntegerField(choices=RATING, verbose_name='ценa и качество')
    reliability = models.IntegerField(choices=RATING, verbose_name='надежность')
    time_c = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Коментарии'
        verbose_name= 'Коментарий'


