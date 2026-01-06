from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Prediction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='predictions'
    )
    risk_score = models.FloatField(help_text="Prawdopodobieństwo rozwodu (0.0 - 1.0)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - {self.risk_score:.2f}"

class SurveyAnswer(models.Model):
    prediction = models.OneToOneField(
        Prediction, 
        on_delete=models.CASCADE, 
        related_name='answers'
    )

    # Definiujemy 54 pola. 
    # Dataset używa skali 0-4. Używamy PositiveSmallIntegerField dla oszczędności miejsca.
    # Aby nie pisać tego ręcznie, możesz użyć pętli, ale dla czytelności i IDE
    # najlepiej zadeklarować je jawnie (poniżej skrócona wersja, musisz mieć q1...q54):
    
    q1 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q2 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q3 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q4 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q5 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q6 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q7 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q8 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q9 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q10 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q11 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q12 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q13 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q14 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q15 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q16 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q17 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q18 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q19 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q20 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q21 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q22 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q23 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q24 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q25 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q26 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q27 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q28 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q29 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q30 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q31 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q32 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q33 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q34 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q35 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q36 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q37 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q38 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q39 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q40 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q41 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q42 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q43 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q44 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q45 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q46 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q47 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q48 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q49 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q50 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q51 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q52 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q53 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    q54 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])

    def __str__(self):
        return f"Answers for Prediction {self.prediction.id}"