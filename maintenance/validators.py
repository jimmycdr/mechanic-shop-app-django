import re
from datetime import datetime
from django.core.exceptions import ValidationError

def validate_bolivia_license_plate(value):
    upper_value = value.upper()
    
    if not re.match(r'^\d{3,4}-[A-Z]{3}$', upper_value):
        raise ValidationError(
            f"'{value}' is not a valid Bolivian license plate. "
            f"It must have the format 1234-ABC or 123-XYZ."
        )

def validate_vin(value):
    upper_value = value.upper()
    if len(value) != 17:
        raise ValidationError(
            f"'{value}' is not a valid VIN. It must have exactly 17 characters."
        )

    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', upper_value):
        raise ValidationError(
            f"'{value}' is not a valid VIN. "
            f"It must contain only letters (except I, O, Q) and numbers."
        )

def validate_vehicle_year(value):
    current_year = datetime.now().year
    min_year = 1900
    max_year = current_year + 1
    
    if value < min_year or value > max_year:
        raise ValidationError(
            f"'{value}' is not a valid year. "
            f"It must be between {min_year} and {max_year}."
        )

def validate_bolivia_phone(value):
    clean_value = value.replace(" ", "").replace("-", "")

    if clean_value.startswith("+591"):
        clean_value = clean_value[4:]
    elif clean_value.startswith("591"):
        clean_value = clean_value[3:]
    
    if not re.match(r'^[67]\d{7}$', clean_value):
        raise ValidationError(
            f"'{value}' is not a valid Bolivian phone number. "
        )