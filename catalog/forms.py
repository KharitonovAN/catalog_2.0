from django import forms
from .models import Product, Version
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class CrispyFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class ProductForm(forms.ModelForm, CrispyFormMixin):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(f'Слово "{word}" запрещено в названии продукта.')
        return name

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in forbidden_words:
            if word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено в описании продукта.')
        return description


class VersionForm(forms.ModelForm, CrispyFormMixin):
    class Meta:
        model = Version
        fields = '__all__'


class ModeratorProductForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'image', 'price', 'description', 'is_published')
