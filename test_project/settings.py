from django.db import models

class CustomField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        self.model = cls

    def __eq__(self, other):
        if isinstance(other, CustomField):
            return (
                self.creation_counter == other.creation_counter and
                self.model == other.model
            )
        return NotImplemented

    def __hash__(self):
        return hash((self.creation_counter, self.model))

    def __lt__(self, other):
        if isinstance(other, CustomField):
            return (self.creation_counter, self.model) < (other.creation_counter, other.model)
        return NotImplemented

class A(models.Model):
    class Meta:
        abstract = True
    myfield = CustomField()

class B(A):
    pass

class C(A):
    pass
