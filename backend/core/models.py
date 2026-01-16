from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class DivorceData(models.Model):
    """
    A model to store the responses to the divorce prediction questionnaire.
    Each field 'qX' corresponds to a question in the survey.
    The responses are integers, typically on a scale of 0 to 4.
    """
    q1 = models.IntegerField(
        verbose_name="1. When one of our apologies apologizes when our discussions go in a bad direction, the issue does not extend.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q2 = models.IntegerField(
        verbose_name="2. I know we can ignore our differences, even if things get hard sometimes.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q3 = models.IntegerField(
        verbose_name="3. When we need it, we can take our discussions with my wife from the beginning and correct it.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q4 = models.IntegerField(
        verbose_name="4. When I argue with my wife, it will eventually work for me to contact him.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q5 = models.IntegerField(
        verbose_name="5. The time I spent with my wife is special for us.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q6 = models.IntegerField(
        verbose_name="6. We don't have time at home as partners.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q7 = models.IntegerField(
        verbose_name="7. We are like two strangers who share the same environment at home rather than family.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q8 = models.IntegerField(
        verbose_name="8. I enjoy our holidays with my wife.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q9 = models.IntegerField(
        verbose_name="9. I enjoy traveling with my wife.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q10 = models.IntegerField(
        verbose_name="10. My wife and most of our goals are common.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q11 = models.IntegerField(
        verbose_name="11. I think that one day in the future, when I look back, I see that my wife and I are in harmony with each other.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q12 = models.IntegerField(
        verbose_name="12. My wife and I have similar values in terms of personal freedom.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q13 = models.IntegerField(
        verbose_name="13. My husband and I have similar entertainment.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q14 = models.IntegerField(
        verbose_name="14. Most of our goals for people (children, friends, etc.) are the same.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q15 = models.IntegerField(
        verbose_name="15. Our dreams of living with my wife are similar and harmonious",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q16 = models.IntegerField(
        verbose_name="16. We're compatible with my wife about what love should be",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q17 = models.IntegerField(
        verbose_name="17. We share the same views with my wife about being happy in your life",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q18 = models.IntegerField(
        verbose_name="18. My wife and I have similar ideas about how marriage should be",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q19 = models.IntegerField(
        verbose_name="19. My wife and I have similar ideas about how roles should be in marriage",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q20 = models.IntegerField(
        verbose_name="20. My wife and I have similar values in trust",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q21 = models.IntegerField(
        verbose_name="21. I know exactly what my wife likes.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q22 = models.IntegerField(
        verbose_name="22. I know how my wife wants to be taken care of when she's sick.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q23 = models.IntegerField(
        verbose_name="23. I know my wife's favorite food.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q24 = models.IntegerField(
        verbose_name="24. I can tell you what kind of stress my wife is facing in her life.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q25 = models.IntegerField(
        verbose_name="25. I have knowledge of my wife's inner world.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q26 = models.IntegerField(
        verbose_name="26. I know my wife's basic concerns.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q27 = models.IntegerField(
        verbose_name="27. I know what my wife's current sources of stress are.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q28 = models.IntegerField(
        verbose_name="28. I know my wife's hopes and wishes.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q29 = models.IntegerField(
        verbose_name="29. I know my wife very well.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q30 = models.IntegerField(
        verbose_name="30. I know my wife's friends and their social relationships.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q31 = models.IntegerField(
        verbose_name="31. I feel aggressive when I argue with my wife.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q32 = models.IntegerField(
        verbose_name="32. When discussing with my wife, I usually use expressions such as \"you always\" or \"you never\".",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q33 = models.IntegerField(
        verbose_name="33. I can use negative statements about my wife's personality during our discussions.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q34 = models.IntegerField(
        verbose_name="34. I can use offensive expressions during our discussions.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q35 = models.IntegerField(
        verbose_name="35. I can insult our discussions.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q36 = models.IntegerField(
        verbose_name="36. I can be humiliating when we argue.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q37 = models.IntegerField(
        verbose_name="37. My argument with my wife is not calm.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q38 = models.IntegerField(
        verbose_name="38. I hate my wife's way of bringing it up.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q39 = models.IntegerField(
        verbose_name="39. Fights often occur suddenly.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q40 = models.IntegerField(
        verbose_name="40. We're just starting a fight before I know what's going on.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q41 = models.IntegerField(
        verbose_name="41. When I talk to my wife about something, my calm suddenly breaks.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q42 = models.IntegerField(
        verbose_name="42. When I argue with my wife, it only snaps in and I don't say a word.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q43 = models.IntegerField(
        verbose_name="43. I'm mostly thirsty to calm the environment a little bit.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q44 = models.IntegerField(
        verbose_name="44. Sometimes I think it's good for me to leave home for a while.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q45 = models.IntegerField(
        verbose_name="45. I'd rather stay silent than argue with my wife.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q46 = models.IntegerField(
        verbose_name="46. Even if I'm right in the argument, I'm thirsty not to upset the other side.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q47 = models.IntegerField(
        verbose_name="47. When I argue with my wife, I remain silent because I am afraid of not being able to control my anger.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q48 = models.IntegerField(
        verbose_name="48. I feel right in our discussions.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q49 = models.IntegerField(
        verbose_name="49. I have nothing to do with what I've been accused of.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q50 = models.IntegerField(
        verbose_name="50. I'm not actually the one who's guilty about what I'm accused of.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q51 = models.IntegerField(
        verbose_name="51. I'm not the one who's wrong about problems at home.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q52 = models.IntegerField(
        verbose_name="52. I wouldn't hesitate to tell her about my wife's inadequacy.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q53 = models.IntegerField(
        verbose_name="53. When I discuss it, I remind her of my wife's inadequate issues.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    q54 = models.IntegerField(
        verbose_name="54. I'm not afraid to tell her about my wife's incompetence.",
        validators=[MinValueValidator(0), MaxValueValidator(4)], null=True, blank=True
    )
    divorce_class = models.IntegerField(
        verbose_name="Class",
        validators=[MinValueValidator(0), MaxValueValidator(1)], null=True, blank=True
    )

    def __str__(self):
        return f"Divorce Form Data {self.pk}"