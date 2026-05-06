from django.db import models
from django.forms import ModelForm, RadioSelect

class BatchData(models.Model):
    name = models.CharField(max_length=100)

class TestRun(models.Model):
    data_file = models.ForeignKey(BatchData, on_delete=models.SET_NULL, null=True, blank=False)

class TestRunForm(ModelForm):
    class Meta:
        model = TestRun
        fields = ['data_file']
        widgets = {'data_file': RadioSelect()}
