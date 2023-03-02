from django_filters import FilterSet, ModelChoiceFilter, CharFilter, ChoiceFilter
from .models import Ad, Category, ResponseAd


class AdFilter(FilterSet):
    titels = CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'
    )

    status = ChoiceFilter(
        field_name='status',
        choices=Ad.STATUS_CHOICES,
        label='Статус объявления',
        empty_label='Все'
    )

    status_responses = ChoiceFilter(
        field_name='responses__status',
        choices=ResponseAd.STATUS_CHOICES,
        label='Отклики со статусом',
        empty_label='Все'
    )

    class Meta:
        model = Ad
        fields = { }


class AdsFilter(FilterSet):
    titels = CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'
    )

    author = CharFilter(
        field_name='author__username',
        label='Автор',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ad
        fields = { }
