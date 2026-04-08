class TileExpertSystem:
    def __init__(self):
        self.facts = {}

    def ask(self, question: str, options: list) -> str:
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            try:
                choice = int(input("   Ваш выбор (номер): "))
                if 1 <= choice <= len(options):
                    selected = options[choice - 1]
                    print(f"   → Выбрано: {selected}")
                    return selected
                else:
                    print("   Ошибка: введите номер из списка!")
            except ValueError:
                print("   Ошибка: введите число!")

    def collect_input(self):
        print("=" * 100)
        print("   ЭКСПЕРТНАЯ СИСТЕМА: Выбор способа укладки плитки")
        print("=" * 100)

        self.facts['surface'] = self.ask("1. Тип поверхности", ["Пол", "Стена", "Потолок"])
        self.facts['base_material'] = self.ask("2. Материал основания", ["Бетон", "Гипсокартон", "Дерево/ДСП", "Штукатурка", "Металл", "Другое"])
        self.facts['base_condition'] = self.ask("3. Состояние основания", ["Идеально ровное", "С небольшими неровностями", "С трещинами/дефектами", "Требует капитального выравнивания"])
        self.facts['room_type'] = self.ask("4. Тип помещения", ["Ванная/санузел", "Кухня", "Гостиная/коридор", "Балкон/лоджия", "Наружные работы", "Другое"])
        self.facts['humidity'] = self.ask("5. Уровень влажности", ["Сухое помещение", "Влажное", "Мокрое (постоянный контакт с водой)"])
        self.facts['tile_type'] = self.ask("6. Тип плитки", ["Керамика", "Керамогранит", "Мозаика", "Клинкер"])
        self.facts['tile_size'] = self.ask("7. Размер плитки", ["Маленькая (до 20×20 см)", "Средняя (20–40 см)", "Большая (свыше 40 см)"])
        self.facts['pattern'] = self.ask("8. Желаемый рисунок укладки", ["Прямая", "Диагональная", "Елочкой", "Со смещением", "Модульная", "Другое"])
        self.facts['experience'] = self.ask("9. Уровень опыта укладчика", ["Новичок", "Средний", "Профессионал"])
        self.facts['budget'] = self.ask("10. Бюджет", ["Низкий", "Средний", "Высокий"])

        self.facts['area'] = self.ask("11. Площадь укладки", ["До 5 м²", "5–15 м²", "15–30 м²", "Более 30 м²"])
        self.facts['tile_shape'] = self.ask("12. Форма плитки", ["Квадрат", "Прямоугольник", "Шестигранник", "Другая"])
        self.facts['tile_thickness'] = self.ask("13. Толщина плитки", ["Тонкая (до 8 мм)", "Стандартная (8–12 мм)", "Толстая (свыше 12 мм)"])

        if self.facts['surface'] == "Пол":
            self.facts['warm_floor'] = self.ask("14. Есть ли теплый пол?", ["Да", "Нет"])
            self.facts['load'] = self.ask("15. Ожидаемая нагрузка", ["Низкая (пешеходная)", "Средняя", "Высокая"])
            self.facts['anti_slip'] = self.ask("16. Требуется антискольжение?", ["Да", "Нет"])
            self.facts['soundproof'] = self.ask("17. Нужна ли шумоизоляция?", ["Да", "Нет"])
        else:
            self.facts['warm_floor'] = self.facts['load'] = self.facts['anti_slip'] = self.facts['soundproof'] = "Нет"

        if self.facts['humidity'] in ["Влажное", "Мокрое (постоянный контакт с водой)"] or self.facts['room_type'] == "Ванная/санузел":
            self.facts['hydro'] = self.ask("18. Требуется гидроизоляция?", ["Да", "Нет"])
        else:
            self.facts['hydro'] = "Нет"

        if self.facts['tile_size'] == "Большая (свыше 40 см)" or self.facts['experience'] == "Новичок" or self.facts['pattern'] in ["Диагональная", "Елочкой", "Модульная"]:
            self.facts['svp'] = self.ask("19. Использовать СВП?", ["Да", "Нет"])
            if self.facts['svp'] == "Да":
                self.facts['svp_type'] = self.ask("19.1 Тип СВП:", ["Обычные клинья", "С колпачками (Rubi/Litokol)", "Профессиональная 3D-система", "Другая"])
            else:
                self.facts['svp_type'] = "Не используется"
        else:
            self.facts['svp'] = self.facts['svp_type'] = "Нет"

        if self.facts['room_type'] == "Наружные работы":
            self.facts['frost'] = self.ask("20. Требуется морозостойкость?", ["Да", "Нет"])
            self.facts['outdoor'] = "Наружные"
        else:
            self.facts['frost'] = "Нет"
            self.facts['outdoor'] = "Внутренние"

        self.facts['allergy'] = self.ask("21. Есть аллергия на химию?", ["Да", "Нет"])
        self.facts['eco'] = self.ask("22. Важна экологичность?", ["Да", "Нет"])

        if self.facts['base_condition'] != "Идеально ровное":
            self.facts['leveling'] = self.ask("23. Планируете предварительное выравнивание?", ["Да", "Нет"])
        else:
            self.facts['leveling'] = "Нет"

        self.facts['joint_width'] = self.ask("24. Предпочтительная ширина швов", ["Тонкие (1–2 мм)", "Средние (3–5 мм)", "Широкие (более 5 мм)"])
        self.facts['communications'] = self.ask("25. Есть коммуникации под плиткой?", ["Да", "Нет"]) if self.facts['surface'] != "Потолок" else "Нет"
        self.facts['temp_mode'] = self.ask("26. Температурный режим", ["Стандартный (18–25°C)", "Низкие температуры", "Высокие температуры"])
        self.facts['tools'] = self.ask("27. Есть профессиональные инструменты?", ["Да", "Нет"])
        self.facts['time_limit'] = self.ask("28. Жёсткие сроки?", ["Да", "Нет"])
        self.facts['glue_pref'] = self.ask("29. Предпочитаемый тип клея", ["Стандартный", "Эластичный", "Для влажных помещений", "Быстросохнущий", "Другое"])
        self.facts['grout_pref'] = self.ask("30. Тип затирки", ["Стандартная цементная", "Эпоксидная", "Антигрибковая", "Цветная/декоративная"])
        self.facts['style'] = self.ask("31. Стиль дизайна", ["Современный", "Классический", "Минимализм", "Другое"])
        self.facts['price_level'] = self.ask("32. Цена за м²", ["Низкая", "Средняя", "Высокая"])
        self.facts['availability'] = self.ask("33. Доступность материалов", ["В наличии", "Ограничена"])
        self.facts['adhesion'] = self.ask("34. Адгезия основания", ["Высокая", "Средняя", "Низкая (требует грунтовки)"])

        print("\n" + "="*100)
    

    def infer(self):
        recs = []

        # ==================== АКТИВНОЕ ИСПОЛЬЗОВАНИЕ ВСЕХ ПАРАМЕТРОВ ====================

        # base_material
        if self.facts['base_material'] == "Дерево/ДСП":
            recs.append("Основание из дерева/ДСП → обязательно использовать эластичный клей")
        elif self.facts['base_material'] == "Гипсокартон":
            recs.append("Гипсокартон → использовать клей для гипсокартона и лёгкую плитку")
        elif self.facts['base_material'] == "Металл":
            recs.append("Металлическое основание → специальный клей с высокой адгезией")

        # tile_type
        if self.facts['tile_type'] == "Керамогранит":
            recs.append("Керамогранит → рекомендуется усиленный клей и СВП при большом формате")
        elif self.facts['tile_type'] == "Мозаика":
            recs.append("Мозаика → укладка на специальную сетку + белый клей")
        elif self.facts['tile_type'] == "Клинкер":
            recs.append("Клинкерная плитка → подходит для наружных работ и высоких нагрузок")

        # joint_width
        if self.facts['joint_width'] == "Тонкие (1–2 мм)":
            recs.append("Тонкие швы (1-2 мм) требуют высокой точности укладки и профессионального уровня")
        elif self.facts['joint_width'] == "Широкие (более 5 мм)":
            recs.append("Широкие швы → рекомендуется декоративная или эпоксидная затирка")
        else:
            recs.append("Средние швы (3-5 мм) — наиболее универсальный и удобный вариант")

        # Остальные параметры (для полноты)
        if self.facts['surface'] == "Пол" and self.facts['base_condition'] == "Идеально ровное":
            recs.append("Способ укладки: Прямая укладка")

        if self.facts['tile_size'] == "Большая (свыше 40 см)":
            recs.append("Большая плитка требует обязательного использования СВП")

        if self.facts['svp'] == "Да":
            recs.append(f"Тип СВП: {self.facts['svp_type']}")

        if self.facts['humidity'] == "Мокрое (постоянный контакт с водой)" or self.facts['room_type'] == "Ванная/санузел":
            recs.append("Гидроизоляция обязательна + клей для влажных помещений")

        if self.facts['warm_floor'] == "Да":
            recs.append("Эластичный клей обязателен (тёплый пол)")

        if self.facts['load'] == "Высокая":
            recs.append("Высокая нагрузка → керамогранит + усиленный клей")

        if self.facts['pattern'] in ["Диагональная", "Елочкой", "Модульная"]:
            recs.append(f"Сложный рисунок ({self.facts['pattern']}) — рекомендуется профессионал")

        if self.facts['experience'] == "Новичок":
            recs.append("Новичку рекомендуется простой способ укладки + СВП")

        if self.facts['outdoor'] == "Наружные" or self.facts['frost'] == "Да":
            recs.append("Морозостойкий клей + эпоксидная затирка")

        if self.facts['anti_slip'] == "Да":
            recs.append("Антискользящая плитка")

        if self.facts['soundproof'] == "Да":
            recs.append("Шумоизоляционная подложка")

        if self.facts['communications'] == "Да":
            recs.append("Аккуратная резка вокруг коммуникаций")

        if self.facts['adhesion'] == "Низкая (требует грунтовки)":
            recs.append("Нанести грунтовку")

        if self.facts['allergy'] == "Да" or self.facts['eco'] == "Да":
            recs.append("Низкотоксичные экологичные материалы")

        if self.facts['temp_mode'] == "Низкие температуры":
            recs.append("Быстросохнущий клей или добавки")

        if self.facts['glue_pref'] != "Другое":
            recs.append(f"Выбранный тип клея: {self.facts['glue_pref']}")

        if self.facts['grout_pref'] != "Стандартная цементная":
            recs.append(f"Выбранная затирка: {self.facts['grout_pref']}")

        if self.facts['style'] == "Современный" and self.facts['tile_size'] == "Большая (свыше 40 см)":
            recs.append("Современный стиль + большая плитка = минималистичные тонкие швы")

        if self.facts['budget'] == "Низкий" or self.facts['price_level'] == "Низкая":
            recs.append("Бюджетный вариант: прямая укладка + стандартная затирка")

        if self.facts['availability'] == "Ограничена":
            recs.append("Материалы ограничены в доступности — рекомендуется сделать запас")
            recs.append(f"Дополнительно: {self.facts['extra']}")

        if not recs:
            recs.append("Рекомендуется стандартная прямая укладка со стандартными материалами")

        return recs

    def show_result(self, recommendations):
        print("=" * 100)
        print("               ИТОГОВЫЕ РЕКОМЕНДАЦИИ")
        print("=" * 100)
        print("Рекомендации:\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i:2}. {rec}")

        print("\n" + "-" * 100)
        print("Общие советы:")
        print("• Используйте СИЗ")
        print("• Соблюдайте время высыхания материалов")
        print("• При сомнениях — проконсультируйтесь со специалистом")
        print("=" * 100)


# ===================== ЗАПУСК =====================
if __name__ == "__main__":
    es = TileExpertSystem()
    es.collect_input()
    recommendations = es.infer()
    es.show_result(recommendations)