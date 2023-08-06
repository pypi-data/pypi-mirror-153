
from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django_select2.forms import Select2Widget
from djforms.fields import DatePickerField

from customers.models import Customer


class CustomerChoiceWidget(Select2Widget):

    empty_label = _('Select customer')


class CustomerChoiceField(forms.ModelChoiceField):

    def __init__(
            self,
            queryset=Customer.objects.all(),
            required=False,
            widget=CustomerChoiceWidget(),
            *args, **kwargs):
        super().__init__(
            queryset=queryset,
            required=required,
            widget=widget,
            *args, **kwargs
        )


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class ReportForm(forms.Form):

    date_from = DatePickerField(label=_('Date from'))

    date_to = DatePickerField(label=_('Date to'))

    def __init__(self, data):

        today = datetime.now().date().strftime(settings.DATE_INPUT_FORMATS[0])

        super().__init__(
            data={
                'date_from': data.get('date_from', today),
                'date_to': data.get('date_to', today),
            }
        )

        self.is_valid()
