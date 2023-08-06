from rest_framework import serializers

from djackal.views.base import DjackalAPIView
from . import mixins
from ..serializers import BaseModelSerializer

__all__ = [
    'ListAPIView',
    'CreateAPIView',
    'ListCreateAPIView',
    'DetailAPIView',
    'UpdateAPIView',
    'DestroyAPIView',
    'DetailUpdateAPIView',
    'DetailDestroyAPIView',
    'UpdateDestroyAPIView',
    'DetailUpdateDestroyAPIView',
    'LabelValueListAPIView',
]


class ListAPIView(DjackalAPIView, mixins.ListViewMixin):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)


class CreateAPIView(DjackalAPIView, mixins.CreateViewMixin):
    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class ListCreateAPIView(DjackalAPIView, mixins.ListViewMixin, mixins.CreateViewMixin):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)

    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class DetailAPIView(DjackalAPIView, mixins.DetailViewMixin):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)


class UpdateAPIView(DjackalAPIView, mixins.UpdateViewMixin):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DestroyAPIView(DjackalAPIView, mixins.DestroyViewMixin):
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DetailUpdateAPIView(DjackalAPIView, mixins.DetailViewMixin, mixins.UpdateViewMixin):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailDestroyAPIView(DjackalAPIView, mixins.DetailViewMixin, mixins.DestroyViewMixin):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateDestroyAPIView(DjackalAPIView, mixins.UpdateViewMixin, mixins.DestroyViewMixin):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DetailUpdateDestroyAPIView(DjackalAPIView, mixins.DetailViewMixin, mixins.UpdateViewMixin,
                                 mixins.DestroyViewMixin):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class LabelValueListAPIView(DjackalAPIView):
    label_field = 'name'
    value_field = 'id'

    def get_serializer_class(self):
        class LabelValueSerializer(BaseModelSerializer):
            label = serializers.CharField(source=self.label_field)
            value = serializers.CharField(source=self.value_field)

            class Meta:
                model = self.get_model()
                fields = ('label', 'value')

        return LabelValueSerializer

    def get(self, request, **kwargs):
        queryset = self.get_filtered_queryset()
        ser = self.get_serializer(queryset, many=True)
        return self.simple_response(ser.data)
