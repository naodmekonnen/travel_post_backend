from rest_framework import serializers

class ForeignKeyField(serializers.PrimaryKeyRelatedField):
    """
    To use: 
        class ParentSerializer(ModelSerializer):
            child = ForeignKeyField(queryset=Child.objects.all(), serializer=ChildSerializer)
    """

    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)

class CustomManyToManyField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', None)
        self.field_name = kwargs.pop('field_name', None)

        if self.model is None:
            raise TypeError('"model" is not a valid model class')

        if self.field_name is None:
            raise TypeError('"field_name" is not a valid field_name on model')

        super().__init__(**kwargs)

 
    def to_representation(self, model):
        return getattr(model, self.field_name)

    def to_internal_value(self, id):
        if isinstance(id, int):
            instance = self.model.objects.filter(id=id).first()
            if instance:
                return instance

        raise serializers.ValidationError(
            "No instance exists with id \"%s\"." % str(id),
        )