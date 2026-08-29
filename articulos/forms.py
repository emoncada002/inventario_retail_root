from django import forms
from .models import Producto
from django.core.exceptions import ValidationError

class ProductoModelForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku','nombre', 'categoria', 'precio', 'stock_actual', 'stock_minimo', 'imagen']
        widgets = {
            'sku': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # Sanitización y validación individual de campo (clean_<campo>)
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise ValidationError("El nombre es demasiado corto (mínimo 3 caracteres).")
        # Sanitización: elimina espacios vacíos basura y aplica formato título
        return nombre.strip().title()

    # Validación global multicampo del formulario (clean)
    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        precio = cleaned_data.get('precio')

        # Regla de negocio cruzada entre dos campos
        if categoria == 'Gorras y mochilas' and precio and precio > 5000:
            raise ValidationError("Una gorra o mochila no puede costar más de $5000 MXN.")
        return cleaned_data# Formularios de alta con validación de SKU
