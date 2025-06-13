from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        )
    )
    title = models.CharField(
        'Заголовок',
        max_length=256
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    description = models.TextField('Описание')
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'


class Location(models.Model):
    name = models.CharField(
        'Название места',
        max_length=256,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    title = models.CharField(
        'Заголовок',
        max_length=256
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            "Если установить дату и время в будущем — можно "
            "делать отложенные публикации."
        )
    )
    is_published = models.BooleanField(
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True,
        verbose_name='Опубликовано'
    )
    image = models.ImageField(
        upload_to='post_images',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    text = models.TextField('Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    text = models.TextField('Текст')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
