from django.core.validators import RegexValidator

# Allows letters (including accented), spaces, hyphens, and apostrophes.
# Disallows names starting or ending with spaces, hyphens, or apostrophes.

name_validator = RegexValidator(
    regex=r"^(?![\s\-'])[A-Za-zÀ-ÖØ-öø-ÿ\s\-']*(?<![\s\-'])$",
    message="Veuillez entrer un nom valide. Seules les lettres, espaces, tirets et apostrophes sont autorisés.",
)
