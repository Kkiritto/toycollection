from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Toy, Brand, Category
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import CollectionItem
from .forms import CollectionItemForm


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
    toy = get_object_or_404(
        Toy.objects.select_related('brand', 'category'), slug=slug
    )
    return render(request, 'toys/toy_detail.html', {'toy': toy})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def my_collection(request):
    items = CollectionItem.objects.select_related(
        'toy', 'toy__brand', 'toy__category'
    ).filter(user=request.user)

    total_items = items.count()
    total_value = items.aggregate(total=Sum('purchase_price'))['total'] or 0

    return render(request, 'toys/my_collection.html', {
        'items': items,
        'total_items': total_items,
        'total_value': total_value,
    })


@login_required
def add_to_collection(request, slug):
    toy = get_object_or_404(Toy, slug=slug)

    if CollectionItem.objects.filter(user=request.user, toy=toy).exists():
        messages.warning(request, 'Эта игрушка уже в вашей коллекции!')
        return redirect('toy_detail', slug=slug)

    if request.method == 'POST':
        form = CollectionItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.toy = toy
            item.save()
            messages.success(request, f'«{toy.title}» добавлена в коллекцию!')
            return redirect('my_collection')
    else:
        form = CollectionItemForm()

    return render(request, 'toys/add_to_collection.html', {
        'form': form,
        'toy': toy,
    })


@login_required
def remove_from_collection(request, item_id):
    item = get_object_or_404(CollectionItem, id=item_id, user=request.user)
    if request.method == 'POST':
        toy_title = item.toy.title
        item.delete()
        messages.success(request, f'«{toy_title}» удалена из коллекции.')
    return redirect('my_collection')