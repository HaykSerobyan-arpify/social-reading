from rest_framework.exceptions import ValidationError


def CharValidator(value):
    for el in value.split():
        if '-' in el or not el.isalpha():
            if not el.replace('-', '', 1).isalpha():
                raise ValidationError(detail="Name characters must be alphabet letters or contain only one '-' symbol")
