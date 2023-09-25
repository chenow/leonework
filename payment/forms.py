from django import forms


class EmailOffersForm(forms.Form):
    object = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "true", "value": "Métier manquant"})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ecrivez votre message pour demander à rajouter une formation..."
            }
        ),
        required=True,
        max_length=2000,
    )
