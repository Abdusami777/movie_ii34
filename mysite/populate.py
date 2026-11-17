import random

from store_app.models import (UserProfile, Category, SubCategory, Product,
                              ProductImage, Review)

DATA = {
    'Film': {
        'Kids': [('Lego for boys', 14000), ('Duna', 1000)],
        'carsfilm': [('Cars 1', 800), ('Cars 2', 900)],
        'japans': [('Spirited Away', 1200), ('Totoro', 1100)],
    },
    'Electronics': {
        'Phones': [('iPhone 15', 90000), ('Samsung S24', 80000)],
        'Laptops': [('MacBook Air', 120000), ('Lenovo ThinkPad', 70000)],
    },
    'Clothes': {
        'Men': [('T-shirt', 1500), ('Jeans', 3500)],
        'Women': [('Dress', 4500), ('Jacket', 6000)],
    },
}

# тест колдонуучулар (пикир калтыруу үчүн)
users = []
for i in range(1, 6):
    u, created = UserProfile.objects.get_or_create(
        username=f'testuser{i}',
        defaults={'first_name': f'User{i}', 'email': f'user{i}@test.com'},
    )
    if created:
        u.set_password('test12345')
        u.save()
    users.append(u)

article = 100000 + Product.objects.count() * 10
for cat_name, subs in DATA.items():
    cat, _ = Category.objects.get_or_create(
        Category_name=cat_name,
        defaults={'Category_image': 'photo_category/test.jpg'},
    )
    for sub_name, products in subs.items():
        sub, _ = SubCategory.objects.get_or_create(
            subcategory_name=sub_name, defaults={'category': cat})
        for name, price in products:
            if Product.objects.filter(product_name=name).exists():
                continue
            article += 1
            p = Product.objects.create(
                product_name=name,
                price=price,
                subcategory=sub,
                description=f'{name} - test description',
                product_type=random.choice([True, False]),
                article=article,
            )
            ProductImage.objects.create(
                product=p, product_image='image_product/test.jpg')
            for u in random.sample(users, k=random.randint(2, 5)):
                Review.objects.create(
                    user=u, product=p,
                    star=random.randint(1, 5), text='Good product')

print('Done:',
      Category.objects.count(), 'categories,',
      SubCategory.objects.count(), 'subcategories,',
      Product.objects.count(), 'products,',
      Review.objects.count(), 'reviews')