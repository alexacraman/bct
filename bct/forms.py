from django import forms
from django_recaptcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255,
        widget=forms.TextInput(
            attrs={'class': ' text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block'}
        )
    )
    email = forms.EmailField(max_length=255,required=True,
        widget=forms.EmailInput(
            attrs={'class': 'text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block'}
        )
    )
    phone = forms.IntegerField(required=False,
        widget=forms.NumberInput(
            attrs={'class': 'text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block'}
        )
    )
    message = forms.CharField(max_length=500, required=True,
        widget=forms.Textarea(
            attrs={'class': 'text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block', 'rows': 3, 'cols': 19}
        )
    )
    captcha = ReCaptchaField()

    forbidden_words = ['seo', 'ranking', 'whitehat', 'ranks', 'organically','keywords','baclink', 'toxic', 'profile', 'toxicity','Stacking','comprehensive','metrics']

    def clean_message(self, *args, **kwargs):
        message = self.cleaned_data.get('message')
        for keyword in self.forbidden_words:
            if keyword.lower() in message.lower():
                raise forms.ValidationError("Forbidden")
        return message