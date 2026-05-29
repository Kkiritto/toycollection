from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Toy, Brand, Category


def home(request):
    latest_toys = Toy.objects.select_related('brand', 'category').all()[:6]
    total_toys = Toy.objects.count()
    total_brands = Brand.objects.count()
    return render(request, 'toys/home.html', {
        'latest_toys': latest_toys,
        'total_toys': total_toys,
        'total_brands': total_brands,
    })


def toy_list(request):
    toys = Toy.objects.select_related('brand', 'category').all()

    query = request.GET.get('q', '').strip()
    if query:
        toys = toys.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    brand_slug = request.GET.get('brand')
    if brand_slug:
        toys = toys.filter(brand__slug=brand_slug)

    category_slug = request.GET.get('category')
    if category_slug:
        toys = toys.filter(category__slug=category_slug)

    rarity = request.GET.get('rarity')
    if rarity:
        toys = toys.filter(rarity=rarity)

    context = {
        'toys': toys,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'rarities': Toy.RARITY_CHOICES,
        'query': query,
        'selected_brand': brand_slug,
        'selected_category': category_slug,
        'selected_rarity': rarity,
    }
    return render(request, 'toys/toy_list.html', context)


def toy_detail(request, slug):
    toy = get_object_or_404(Toy.objects.select_related('brand', 'category'), slug=slug)
    return render(request, 'toys/toy_detail.html', {'toy': toy})