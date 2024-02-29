from .models import *
from modeltranslation.translator import TranslationOptions, register

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'body', 'level')

@register(Part)
class PartTranslationOptions(TranslationOptions):
    fields = ('name',)