from django.core.exceptions import ValidationError

def fileSize(value):
    fileSize = value.size
    if fileSize > 1e+8 :
        raise ValidationError("Maximum video size is 100MB")
        