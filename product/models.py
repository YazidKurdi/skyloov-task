import os
import threading
from time import sleep

from PIL import Image
from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed Use'),
    )

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    class Meta:
        ordering = ['-created_at']

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            thread = threading.Thread(target=self.create_image_dimensions)
            thread.start()

    def create_image_dimensions(self):
        # Open the uploaded image using PIL
        sleep(10)
        img = Image.open(self.image.path)

        self.basename = os.path.basename(self.image.name)

        # Resize the image to desired dimensions
        # You can modify these dimensions according to your requirements
        thumbnail_size = (100, 100)
        medium_size = (300, 300)

        # Create thumbnail
        img.thumbnail(thumbnail_size)
        thumbnail_path = self.get_thumbnail_path()
        self.create_directory(os.path.dirname(thumbnail_path))  # Create the directory if it doesn't exist
        img.save(thumbnail_path)

        # Create medium-sized image
        img.thumbnail(medium_size)
        medium_path = self.get_medium_path()
        self.create_directory(os.path.dirname(medium_path))  # Create the directory if it doesn't exist
        img.save(medium_path)

    def create_directory(self, directory_path):
        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def get_thumbnail_path(self):
        # Generate a unique filename for the thumbnail image
        # You can modify this logic to suit your needs
        return f'media/product_images/thumbnails/{self.basename}'

    def get_medium_path(self):
        # Generate a unique filename for the medium-sized image
        # You can modify this logic to suit your needs
        return f'media/product_images/medium/{self.basename}'

    def __str__(self):
        return f'{self.name} - {self.brand}'
