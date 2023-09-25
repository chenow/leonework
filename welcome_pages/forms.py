from django import forms
from .models import User


class NewUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ["email", "password"]
        labels = {
            "password": "Mot de passe",
        }
        widgets = {"password": forms.PasswordInput()}


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "Mot de passe"


class EmailForm(forms.Form):
    object = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "true", "value": "Diplôme manquant"})
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


class AcceuilForm(forms.Form):
    email = forms.EmailField(max_length=150)
    object = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "true", "value": "Diplôme manquant"})
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


class EmailPoste(forms.Form):
    object = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "true", "value": "Poste manquant"})
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ecrivez votre message pour demander à rajouter un poste..."
            }
        ),
        required=True,
        max_length=2000,
    )


class EmailMissingMetierForm(forms.Form):
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


class NewLinkForm(forms.Form):
    email = forms.EmailField(max_length=200)
