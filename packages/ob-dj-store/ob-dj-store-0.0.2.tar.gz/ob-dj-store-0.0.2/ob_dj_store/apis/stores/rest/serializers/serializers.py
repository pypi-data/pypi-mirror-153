import typing

from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ob_dj_store.core.stores.models import (
    Attribute,
    AttributeChoice,
    Cart,
    CartItem,
    Category,
    Favorite,
    OpeningHours,
    Order,
    OrderHistory,
    OrderItem,
    Product,
    ProductAttribute,
    ProductMedia,
    ProductTag,
    ProductVariant,
    Store,
)


class AttributeChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeChoice
        fields = (
            "id",
            "name",
            "price",
        )


class AttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            "id",
            "name",
            "attribute_choices",
        )


class InventoryValidationMixin:
    def validate(self, attrs: typing.Dict) -> typing.Dict:
        if attrs["product_variant"].has_inventory and attrs["quantity"] < 1:
            raise serializers.ValidationError(_("Quantity must be greater than 0."))
        # validate quantity in inventory
        stock_quantity = (
            attrs["product_variant"]
            .inventories.get(store=attrs["product_variant"].product.store)
            .quantity
        )
        if (
            attrs["product_variant"].has_inventory
            and attrs["quantity"] > stock_quantity
        ):
            raise serializers.ValidationError(
                _("Quantity is greater than the stock quantity.")
            )
        return super().validate(attrs)


class CartItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            "id",
            "cart",
            "product_variant",
            "quantity",
            "unit_price",
            "total_price",
            "notes",
            "attribute_choices",
        )

    def create(self, validated_data):
        return super().create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "customer",
            "items",
            "total_price",
        )
        read_only_fields = ("id", "total_price")

    def update(self, instance, validated_data):
        instance.items.all().delete()
        # update or create instance items
        for item in validated_data["items"]:
            cart_item = CartItem.objects.create(
                cart=instance,
                product_variant=item["product_variant"],
                quantity=item["quantity"],
                notes=item["notes"],
            )
            cart_item.attribute_choices.set(item["attribute_choices"])
            cart_item.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description", "is_active")


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):

    opening_hours = OpeningHourSerializer(many=True, read_only=True)
    in_range_delivery = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "address",
            "location",
            "is_active",
            "currency",
            "minimum_order_amount",
            "delivery_charges",
            "min_free_delivery_amount",
            "opening_hours",
            "in_range_delivery",
            "is_favorite",
            "created_at",
            "updated_at",
        )

    def get_in_range_delivery(self, obj):
        user_location = self.context["request"].query_params.get("point")
        if user_location and obj.poly:
            long, lat = user_location.split(",")
            return obj.poly.contains(Point(float(long), float(lat)))
        return False

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if user:
            try:
                Favorite.objects.favorite_for_user(obj, user)
                return True
            except Favorite.DoesNotExist:
                pass
        return False


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = (
            "id",
            "order",
            "status",
            "created_at",
        )


class OrderItemSerializer(InventoryValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_variant",
            "quantity",
            "total_amount",
            "preparation_time",
            "notes",
            "attribute_choices",
        )

    def create(self, validated_data):
        return super().create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["attribute_choices"] = AttributeChoiceSerializer(
            instance.attribute_choices.all(), many=True
        ).data

        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    history = OrderHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "store",
            "shipping_method",
            "payment_method",
            "shipping_address",
            "customer",
            "status",
            "items",
            "total_amount",
            "preparation_time",
            "history",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "customer": {"read_only": True},
        }

    def validate(self, attrs):
        # The Cart items must not be empty
        user = self.context["request"].user
        if not user.cart.items.exists():
            raise serializers.ValidationError(_("The Cart must not be empty"))
        return super().validate(attrs)

    def create(self, validated_data: typing.Dict):
        order_items = validated_data.pop("items")

        order = Order.objects.create(**validated_data)
        for item in order_items:
            attribute_choices = item.pop("attribute_choices")
            order_item = OrderItem.objects.create(order=order, **item)
            order_item.attribute_choices.set(attribute_choices)
            order_item.save()
        return order


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            "id",
            "name",
            "text_color",
            "background_color",
        )


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_choices = AttributeChoiceSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = (
            "id",
            "name",
            "attribute_choices",
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    product_attributes = ProductAttributeSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "name",
            "price",
            "quantity",
            "sku",
            "is_deliverable",
            "is_active",
            "product_attributes",
        )


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = (
            "id",
            "is_primary",
            "image",
            "order_value",
        )


class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(many=False)
    variants = ProductVariantSerializer(many=True, source="product_variants")
    product_images = ProductMediaSerializer(many=True, source="images")
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_favorite",
            "product_images",
            "variants",
            "store",
        )

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if user:
            try:
                Favorite.objects.favorite_for_user(obj, user)
                return True
            except Favorite.DoesNotExist:
                pass
        return False


class ProductListSerializer(ProductSerializer):
    product_variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "product_images",
            "product_variants",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "description", "products", "is_active")
