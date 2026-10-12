"""Database models for Brain.ua products."""

from django.db import models


class ProductModel(models.Model):
    """Database entity representing a scraped product."""

    title = models.CharField(
        max_length=500,
        verbose_name="Назва",
        null=True,
        blank=True,
    )
    manufacturer = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Виробник",
    )
    color = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Колір",
    )
    memory = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Вбудована пам'ять",
    )
    regular_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Звичайна ціна (грн)",
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Акційна ціна (грн)",
    )
    images = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Список зображень",
    )
    product_code = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Код товару (артикул)",
    )
    review_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Кількість відгуків",
    )
    screen_diagonal = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Діагональ екрану",
    )
    screen_resolution = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Роздільна здатність екрану",
    )
    characteristics = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Всі характеристики",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Створено",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Оновлено",
    )

    class Meta:
        db_table = "products_productmodel"
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.title or 'Без назви'} [{self.product_code or 'без коду'}]"
