import os
import django

# 1. Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from todo.models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

def generate_skins():
    # Ищем автора (или создаем админа, если база пустая)
    author = User.objects.first()
    if not author:
        author = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Создан пользователь 'admin' с паролем 'admin123'")

    # Очищаем старые задачи, чтобы не было дублей при повторном запуске
    Task.objects.all().delete()
    print("Старая база очищена.")

    # Список скинов (Название, Описание)
    skins = [
        # AK-47
        ("AK-47 | Redline", "Классический скин с минималистичным дизайном. Красные линии на черном фоне."),
        ("AK-47 | Vulcan", "Бело-оранжевый футуристичный дизайн. Один из самых узнаваемых скинов."),
        ("AK-47 | Bloodsport", "Спортивный стиль с красными и белыми акцентами. Яркий дизайн."),
        ("AK-47 | Asiimov", "Оранжево-белый дизайн в стиле научной фантастики."),
        ("AK-47 | The Empress", "Королевский дизайн с изображением женщины в доспехах."),
        ("AK-47 | Fuel Injector", "Индустриальный стиль с оранжевыми и черными элементами."),
        ("AK-47 | Neon Rider", "Синтвейв-стиль с неоновыми огнями и ретро-эстетикой 80-х."),
        ("AK-47 | Nightwish", "Темный дизайн с яркими неоновыми акцентами. Мистическая атмосфера."),
        ("AK-47 | Fire Serpent", "Огненная змея на зеленом фоне. Очень редкий скин."),
        ("AK-47 | Case Hardened", "Синие и золотые пятна на металле. Цена зависит от синего."),
        
        # AWP
        ("AWP | Asiimov", "Легендарный оранжево-белый дизайн. Самый популярный скин на AWP."),
        ("AWP | Dragon Lore", "Дракон на белом фоне. Самый известный и дорогой скин."),
        ("AWP | Neo-Noir", "Стиль нуар с изображением девушки. Контрастные цвета."),
        ("AWP | Wildfire", "Огонь и драконы. Яркий и агрессивный дизайн."),
        ("AWP | Redline", "Минималистичный дизайн с красными линиями. Чистый стиль."),
        ("AWP | Lightning Strike", "Молния на синем фоне. Один из самых чистых скинов."),
        ("AWP | Gungnir", "Скандинавский орнамент и золотые элементы. Очень редкий."),
        ("AWP | Fade", "Градиентный окрас от розового к желтому."),
        ("AWP | Oni Taiji", "Японский демон Они на ярком фоне."),
        ("AWP | Atheris", "Змеиный дизайн с зелеными и фиолетовыми элементами."),

        # M4A1-S
        ("M4A1-S | Printstream", "Бело-черный глянцевый дизайн. Самый стильный скин."),
        ("M4A1-S | Cyrex", "Красно-белый дизайн с футуристичными элементами."),
        ("M4A1-S | Hyper Beast", "Яркий монстр с открытой пастью. Агрессивный дизайн."),
        ("M4A1-S | Golden Coil", "Золотые и черные элементы. Роскошный скин."),
        ("M4A1-S | Blue Phosphor", "Синий фосфорный дизайн. Яркий и запоминающийся."),
        ("M4A1-S | Player Two", "Пиксельный стиль в духе аркадных игр."),
        ("M4A1-S | Icarus Fell", "Изображение Икара. Красивый и трагичный сюжет."),
        ("M4A1-S | Hot Rod", "Ярко-красный дизайн. Простой, но заметный."),
        ("M4A1-S | Decimator", "Футуристичный дизайн с оранжевыми элементами."),
        ("M4A1-S | Nightmare", "Кошмарный дизайн с черепами и темными тонами."),

        # USP-S
        ("USP-S | Kill Confirmed", "Череп на прицеле. Один из самых популярных скинов."),
        ("USP-S | Printstream", "Бело-черный глянцевый дизайн. Сочетается с M4A1-S."),
        ("USP-S | Neo-Noir", "Нуарный стиль с яркими акцентами."),
        ("USP-S | Cortex", "Абстрактный дизайн с извилинами."),
        ("USP-S | Whiteout", "Белый камуфляж. Чистый и зимний стиль."),
        ("USP-S | Cyrex", "Красно-белый дизайн в стиле Cyrex."),
        ("USP-S | The Traitor", "Предатель на скине. Интересный сюжет."),
        ("USP-S | Ticket to Hell", "Билет в ад. Мрачный и атмосферный скин."),
        ("USP-S | Jawbreaker", "Сломанная челюсть. Агрессивный дизайн."),
        ("USP-S | Stainless", "Нержавеющая сталь. Строгий металлический вид."),

        # Desert Eagle
        ("Desert Eagle | Printstream", "Бело-черный глянцевый дизайн. Очень популярный."),
        ("Desert Eagle | Blaze", "Огненный дизайн. Классика CS."),
        ("Desert Eagle | Code Red", "Красный код. Агрессивный и яркий дизайн."),
        ("Desert Eagle | Mecha Industries", "Механический дизайн с белыми элементами."),
        ("Desert Eagle | Conspiracy", "Теория заговора. Темный и загадочный дизайн."),
        ("Desert Eagle | Golden Koi", "Золотая рыбка кои. Красивый и элегантный."),
        ("Desert Eagle | Ocean Drive", "Ретро-стиль 80-х с неоновыми огнями."),
        ("Desert Eagle | Emerald Jörmungandr", "Изумрудный змей. Очень редкий скин."),
        ("Desert Eagle | Fennec Fox", "Лисица фенек. Милый и необычный дизайн."),
        ("Desert Eagle | Heat Treated", "Термическая обработка. Синие и золотые узоры."),
    ]

    print("Начинаем генерацию скинов...")
    count = 0

    for title, content in skins:
        # Генерируем уникальную ссылку (slug)
        slug = f"{slugify(title)}-{count}"
        
        # Создаем скин
        task = Task.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=author,
            status=Task.Status.PUBLISHED,
            is_sold=False,
            publish=timezone.now() - timedelta(days=count)
        )
        
        # --- АВТОМАТИЧЕСКИ ПРИВЯЗЫВАЕМ ТЕГИ ---
        if "AK-47" in title:
            task.tags.set(["AK-47", "автомат", "оружие"])
        elif "AWP" in title:
            task.tags.set(["AWP", "снайперская винтовка", "оружие"])
        elif "M4A1-S" in title:
            task.tags.set(["M4A1-S", "автомат", "оружие"])
        elif "USP-S" in title:
            task.tags.set(["USP-S", "пистолет", "оружие"])
        elif "Desert Eagle" in title:
            task.tags.set(["Desert Eagle", "пистолет", "оружие"])
            
        count += 1

    print(f"Успешно добавлено {count} скинов в магазин!")

if __name__ == '__main__':
    generate_skins()