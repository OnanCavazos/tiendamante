# ventas/ventas/Catalogo/Principal/forms.py
from django import forms
from .models import Mensaje

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['nombre', 'correo', 'mensaje']  # ✅ sin 'asunto'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu correo electrónico'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu mensaje aquí...'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'correo': 'Correo electrónico',
            'mensaje': 'Mensaje',
        }
