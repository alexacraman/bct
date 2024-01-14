from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255,
        widget=forms.TextInput(
            attrs={'class': ' text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block'}
        )
    )
    email = forms.EmailField(max_length=255,
        widget=forms.EmailInput(
            attrs={'class': 'text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block'}
        )
    )
    message = forms.CharField(max_length=500,
        widget=forms.Textarea(
            attrs={'class': 'text-slate-700 bg-blue-50 rounded border-2 border-slate-400 p-2 my-2 text-sm w-full block', 'rows': 3, 'cols': 19}
        )
    )