from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    extra_standard_fields = ()

    def __new__(cls, *args, **kwargs):
        if kwargs.get('many', False) is True:
            context = kwargs.get('context', {})
            context.update(has_many=kwargs.get('many', True))
            kwargs.update(context=context)
        return super().__new__(cls, *args, **kwargs)

    @property
    def has_many(self):
        return self.context.get('has_many', False)

    def get_fields(self):
        fields = super().get_fields()

        for field_name in fields:
            if isinstance(fields[field_name], serializers.ListSerializer):
                if isinstance(fields[field_name].child, BaseModelSerializer):
                    fields[field_name].child._context = self._context
            elif isinstance(fields[field_name], BaseModelSerializer):
                fields[field_name]._context = self._context

        return fields

    def request(self):
        return self.context.get('request')

    def current_user(self):
        request = self.request()
        if request is None:
            return self.context.get('user') or self.context.get('current_user')
        return request.user

    def build_field(self, field_name, info, model_class, *args, **kwargs):
        model_field = model_class._meta.get_field(field_name)
        if model_field.__class__ in self.extra_standard_fields:
            return self.build_standard_field(field_name, model_field)
        return super().build_field(field_name, info, model_class, *args, **kwargs)
