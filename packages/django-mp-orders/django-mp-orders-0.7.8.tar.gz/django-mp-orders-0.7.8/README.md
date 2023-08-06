Install:
```
pip install django-mp-orders
```
settings.py
```
from orders.settings import OrdersSettings
 
class CommonSettings(
        OrdersSettings,
        ...):
    pass

```

urls.py
```
from orders.urls import orders_urlpatterns
 
urlpatterns = [

    ...

] + orders_urlpatterns
```

admin menu
```
ParentItem(
    _('Orders'), 
    url='admin:orders_order_changelist',
    icon='fa fa-shopping-cart'
),
```
