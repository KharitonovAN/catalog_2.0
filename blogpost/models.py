from django.db import models

NULLABLE = {'null': True, 'blank': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=150, unique=True, **NULLABLE)
    content = models.TextField(**NULLABLE)
    preview_image = models.ImageField(upload_to='blogpost/images/', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}, {self.slug}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
