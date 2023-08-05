from django.db.models import Prefetch
from django_filters import rest_framework as filters

from ob_dj_store.core.stores.models import (
    Category,
    Order,
    Product,
    ProductVariant,
    Store,
)


class StoreFilter(filters.FilterSet):
    """Store filters"""

    location = filters.CharFilter(method="by_location")
    shipping_methods = filters.CharFilter(method="by_shipping_methods")

    class Meta:
        model = Store
        fields = [
            "delivery_charges",
            "min_free_delivery_amount",
        ]

    def by_location(self, queryset, name, value):
        return queryset.filter(poly__contains=value)

    def by_shipping_methods(self, queryset, name, value):
        return queryset.filter(
            shipping_methods__name__in=[
                value,
            ]
        )


class ProductFilter(filters.FilterSet):
    """Product filters"""

    class Meta:
        model = Product
        fields = [
            "store",
            "is_featured",
            "category__name",
        ]


class VariantFilter(filters.FilterSet):
    """Variant filters"""

    class Meta:
        model = ProductVariant
        fields = [
            "product__name",
            "product__category__name",
        ]


class CategoryFilter(filters.FilterSet):
    """Category filters"""

    store = filters.CharFilter(method="by_store")

    class Meta:
        model = Category
        fields = [
            "name",
        ]

    def by_store(self, queryset, name, value):
        return queryset.prefetch_related(
            Prefetch("products", queryset=Product.objects.filter(store=value))
        ).filter(products__store=value)


class OrderFilter(filters.FilterSet):
    """Order filters"""

    class Meta:
        model = Order
        fields = [
            "status",
        ]
