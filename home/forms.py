from django import forms


class EmailSupportForm(forms.Form):
    objet = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea(), required=True, max_length=2000)
