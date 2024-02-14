from django.db import models

NULLABLE = {'null': True, 'blank': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.CharField(max_length=150, unique=True, **NULLABLE)
    content = models.TextField(**NULLABLE, verbose_name='Текст')
    preview_image = models.ImageField(upload_to='blogpost/images/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='В публикации')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}, {self.slug}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
