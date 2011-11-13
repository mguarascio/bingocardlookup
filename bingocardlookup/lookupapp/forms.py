from django.forms import ModelForm
from .models      import BingoCard

class BingoCardForm(ModelForm):
    class Meta:
        model = BingoCard
