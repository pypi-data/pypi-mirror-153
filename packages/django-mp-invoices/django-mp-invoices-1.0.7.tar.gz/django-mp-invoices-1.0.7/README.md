# MP-invoices

Django invoices app.

### Installation

Install with pip:

```
pip install django-mp-invoices
```
 
Update invocies on product change:
```
def save_model(self, request, obj, form, change):
    super().save_model(request, obj, form, change)
    form.commit(obj)
    request.env.invoices.handle_product_change(obj)
```

### ! Stock fields should be float.
