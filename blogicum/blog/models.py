from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        + 'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        verbose_name='Местоположение',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('id', )

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        + 'разрешены символы латиницы, цифры, дефис и подчёркивание.',
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(verbose_name='Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
