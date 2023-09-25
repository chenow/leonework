from django.db import models


class Degree(models.Model):
    POSSIBLE_LEVELS = [
        "BAC PRO",
        "BACHELOR",
        "BM",
        "BP",
        "BTS",
        "BUT",
        "CAP",
        "DCG",
        "DEC",
        "DEUST",
        "DMA",
        "DSCG",
        "Licence",
        "Licence Professionnelle",
        "MBA",
        "MS",
        "Master",
        "Titre ingénieur",
    ]
    level = models.CharField(
        max_length=350, choices=[(level, level) for level in POSSIBLE_LEVELS]
    )
    subject = models.CharField(max_length=350)

    class Meta:
        ordering = ["level"]
        verbose_name_plural = "Diplômes possibles"
        verbose_name = "Diplôme"

    def __str__(self):
        return f"{self.level} ({self.subject})"


class Language(models.Model):
    language = models.CharField(max_length=100)

    class Meta:
        ordering = ["language"]
        verbose_name_plural = "Langues parlées possibles"
        verbose_name = "Langue"

    def __str__(self):
        return f"{self.language}"


class Quality(models.Model):
    quality = models.CharField(max_length=100)

    class Meta:
        ordering = ["quality"]
        verbose_name_plural = "Qualités des étudiants possibles"
        verbose_name = "Qualité"

    def __str__(self):
        return f"{self.quality}"


class CompanyValue(models.Model):
    value = models.CharField(max_length=100)

    class Meta:
        ordering = ["value"]
        verbose_name_plural = "Valeurs des entreprises possibles"
        verbose_name = "Valeur"

    def __str__(self):
        return f"{self.value}"


class City(models.Model):
    city = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    region = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.city}"

    class Meta:
        ordering = ["city"]
        verbose_name_plural = "Villes possibles"
        verbose_name = "Ville"


class Domain(models.Model):
    domain = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.domain}"

    class Meta:
        ordering = ["domain"]
        verbose_name_plural = "Domaines des métiers"
        verbose_name = "Domaine"


class Profession(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    profession = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.profession}"

    class Meta:
        ordering = ["profession"]
        verbose_name_plural = "Liste des métiers"
        verbose_name = "Métier"
