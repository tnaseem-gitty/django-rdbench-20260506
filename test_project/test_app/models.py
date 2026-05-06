from django.db import models

class FooBar(models.Model):
    foo_bar = models.CharField('foo', max_length=10, choices=[(1, 'foo'), (2, 'bar')])
    
    def __str__(self):
        return self.custom_display()
    
    def custom_display(self):
        return 'something'

    def get_custom_foo_bar_display(self):
        return self.custom_display()
