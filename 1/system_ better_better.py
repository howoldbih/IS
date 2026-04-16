class TileExpertSystem:
    """
    Экспертная система "Выбор способа укладки плитки".

    Логика вывода построена в виде многоуровневых цепочек:
      ВХОДЫ -> ПРОМЕЖУТОЧНЫЙ* -> ПРОМЕЖУТОЧНЫЙ* -> ПРОМЕЖУТОЧНЫЙ* -> ИТОГ*

    Главная цепочка глубины 4 (четыре уровня вывода):
      PATTERN + TILESIZE + EXP
        -> DIFFIC*   (сложность рисунка)
        -> SKILLREQ* (требуемый уровень мастерства, + AREA)
        -> NEEDPRO*  (нужен профессионал,           + BUDGET)
        -> LAYPAT*   (способ укладки,               + SURFACE, BASECOND, STYLE, TILESHP)

    Побочная цепочка глубины 3:
      BASEMAT + WARMFL
        -> ELAST*     (нужен эластичный клей)
        -> GLUECLASS* (класс клея, + TILETYP)
        -> GLUE*      (конкретный тип клея, + LOAD, TEMPMOD, ADHES)

    Побочная цепочка глубины 3:
      HUMID + ROOM
        -> WETENV* (степень влажности среды)
        -> HYDRO*  (гидроизоляция, + OUTDOOR)
        -> GROUT*  (затирка, + JOINT, FROST, ALLERGY_ECO)
    """

    def __init__(self):
        self.facts = {}
        self.derived = {}  # промежуточные выводы со *

    # ============================================================
    # Вспомогательный ввод
    # ============================================================
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
                print("   Ошибка: введите номер из списка!")
            except ValueError:
                print("   Ошибка: введите число!")

    # ============================================================
    # СБОР ВХОДНЫХ ДАННЫХ
    # ============================================================
    def collect_input(self):
        print("=" * 100)
        print("   ЭКСПЕРТНАЯ СИСТЕМА: Выбор способа укладки плитки")
        print("=" * 100)

        f = self.facts
        f['surface'] = self.ask("1. Тип поверхности",
            ["Пол", "Стена", "Потолок"])
        f['base_material'] = self.ask("2. Материал основания",
            ["Бетон", "Гипсокартон", "Дерево/ДСП",
             "Штукатурка", "Металл"])
        f['base_condition'] = self.ask("3. Состояние основания",
            ["Идеально ровное", "С небольшими неровностями",
             "С трещинами/дефектами",
             "Требует капитального выравнивания"])
        f['room_type'] = self.ask("4. Тип помещения",
            ["Ванная/санузел", "Кухня", "Гостиная/коридор",
             "Балкон/лоджия", "Наружные работы"])
        f['humidity'] = self.ask("5. Уровень влажности",
            ["Сухое помещение", "Влажное",
             "Мокрое (постоянный контакт с водой)"])
        f['tile_type'] = self.ask("6. Тип плитки",
            ["Керамика", "Керамогранит", "Мозаика", "Клинкер"])
        f['tile_size'] = self.ask("7. Размер плитки",
            ["Маленькая (до 20×20 см)", "Средняя (20–40 см)",
             "Большая (свыше 40 см)"])
        f['pattern'] = self.ask("8. Желаемый рисунок укладки",
            ["Прямая", "Диагональная", "Елочкой",
             "Со смещением", "Модульная"])
        f['experience'] = self.ask("9. Уровень опыта укладчика",
            ["Новичок", "Средний", "Профессионал"])
        f['budget'] = self.ask("10. Бюджет",
            ["Низкий", "Средний", "Высокий"])
        f['area'] = self.ask("11. Площадь укладки",
            ["До 5 м²", "5–15 м²", "15–30 м²", "Более 30 м²"])
        f['tile_shape'] = self.ask("12. Форма плитки",
            ["Квадрат", "Прямоугольник", "Шестигранник"])

        if f['surface'] == "Пол":
            f['warm_floor'] = self.ask("13. Есть ли тёплый пол?",
                ["Да", "Нет"])
            f['load'] = self.ask("14. Ожидаемая нагрузка",
                ["Низкая (пешеходная)", "Средняя", "Высокая"])
        else:
            f['warm_floor'] = "Нет"
            f['load'] = "Низкая (пешеходная)"

        f['joint_width'] = self.ask("15. Ширина швов",
            ["Тонкие (1–2 мм)", "Средние (3–5 мм)",
             "Широкие (более 5 мм)"])
        f['adhesion'] = self.ask("16. Адгезия основания",
            ["Высокая", "Средняя", "Низкая (требует грунтовки)"])
        f['temp_mode'] = self.ask("17. Температурный режим",
            ["Стандартный (18–25°C)", "Низкие температуры",
             "Высокие температуры"])
        f['style'] = self.ask("18. Стиль дизайна",
            ["Современный", "Классический", "Минимализм"])
        f['allergy_eco'] = self.ask(
            "19. Аллергия на химию или важна экологичность?",
            ["Да", "Нет"])

        # outdoor выводится из room_type без отдельного вопроса
        f['outdoor'] = ("Наружные"
                       if f['room_type'] == "Наружные работы"
                       else "Внутренние")
        # frost выводится из outdoor + temp_mode
        f['frost'] = ("Да"
                      if f['outdoor'] == "Наружные"
                         or f['temp_mode'] == "Низкие температуры"
                      else "Нет")

        print("\n" + "=" * 100)

    # ============================================================
    # УРОВЕНЬ 1 промежуточных выводов
    # ============================================================
    def _derive_diffic(self):
        """DIFFIC* — сложность рисунка укладки."""
        f = self.facts
        hard_patterns = {"Диагональная", "Елочкой", "Модульная"}
        if f['pattern'] in hard_patterns \
                or f['tile_size'] == "Большая (свыше 40 см)":
            level = "Высокая"
        elif f['pattern'] == "Со смещением" \
                or f['tile_size'] == "Средняя (20–40 см)":
            level = "Средняя"
        else:
            level = "Низкая"
        # опыт укладчика влияет в сторону усложнения
        if f['experience'] == "Новичок" and level != "Высокая":
            level = "Средняя"
        self.derived['DIFFIC'] = level
        return level

    def _derive_elast(self):
        """ELAST* — нужна ли эластичность клея."""
        f = self.facts
        if f['base_material'] == "Дерево/ДСП" \
                or f['warm_floor'] == "Да":
            val = "Обязательна"
        elif f['base_material'] in ("Гипсокартон", "Металл"):
            val = "Желательна"
        else:
            val = "Не требуется"
        self.derived['ELAST'] = val
        return val

    def _derive_wetenv(self):
        """WETENV* — степень влажности среды."""
        f = self.facts
        if f['humidity'] == "Мокрое (постоянный контакт с водой)" \
                or f['room_type'] == "Ванная/санузел":
            val = "Мокрая"
        elif f['humidity'] == "Влажное" \
                or f['room_type'] == "Кухня":
            val = "Влажная"
        else:
            val = "Сухая"
        self.derived['WETENV'] = val
        return val

    # ============================================================
    # УРОВЕНЬ 2 промежуточных выводов
    # ============================================================
    def _derive_skillreq(self):
        """SKILLREQ* — требуемый уровень мастерства.
        Строится из DIFFIC и AREA."""
        diffic = self.derived['DIFFIC']
        area = self.facts['area']
        big_area = area in ("15–30 м²", "Более 30 м²")
        if diffic == "Высокая" or (diffic == "Средняя" and big_area):
            val = "Высокий"
        elif diffic == "Средняя" or big_area:
            val = "Средний"
        else:
            val = "Низкий"
        self.derived['SKILLREQ'] = val
        return val

    def _derive_glueclass(self):
        """GLUECLASS* — класс клея. Из ELAST и TILETYP."""
        elast = self.derived['ELAST']
        tile = self.facts['tile_type']
        if elast == "Обязательна":
            val = "Эластичный"
        elif tile in ("Керамогранит", "Клинкер"):
            val = "Усиленный"
        elif elast == "Желательна":
            val = "Улучшенный"
        else:
            val = "Стандартный"
        self.derived['GLUECLASS'] = val
        return val

    def _derive_hydro(self):
        """HYDRO* — требуется ли гидроизоляция. Из WETENV и OUTDOOR."""
        wet = self.derived['WETENV']
        outdoor = self.facts['outdoor']
        if wet == "Мокрая" or outdoor == "Наружные":
            val = "Обязательна"
        elif wet == "Влажная":
            val = "Желательна"
        else:
            val = "Не нужна"
        self.derived['HYDRO'] = val
        return val

    # ============================================================
    # УРОВЕНЬ 3 промежуточных выводов (только у главной цепочки)
    # ============================================================
    def _derive_needpro(self):
        """NEEDPRO* — нужен ли профессионал. Из SKILLREQ и BUDGET."""
        skill = self.derived['SKILLREQ']
        budget = self.facts['budget']
        exp = self.facts['experience']
        if skill == "Высокий" and exp != "Профессионал":
            val = "Да"
        elif skill == "Средний" and exp == "Новичок" \
                and budget != "Низкий":
            val = "Да"
        else:
            val = "Нет"
        self.derived['NEEDPRO'] = val
        return val

    # ============================================================
    # УРОВЕНЬ 4 — ИТОГОВЫЕ ВЫВОДЫ
    # ============================================================
    def _infer_laypat(self):
        """LAYPAT* — способ укладки."""
        f = self.facts
        needpro = self.derived['NEEDPRO']
        # если нужен профессионал — можно взять любой рисунок
        if needpro == "Да":
            return f['pattern']
        # иначе упрощаем до доступного
        if f['experience'] == "Новичок":
            if f['pattern'] in ("Диагональная", "Елочкой", "Модульная"):
                return "Прямая (упрощение сложного рисунка)"
            return f['pattern']
        if f['base_condition'] == "Идеально ровное" \
                and f['style'] == "Минимализм":
            return "Прямая"
        return f['pattern']

    def _infer_glue(self):
        """GLUE* — конкретный тип клея."""
        f = self.facts
        gclass = self.derived['GLUECLASS']
        wet = self.derived['WETENV']
        if wet == "Мокрая":
            return "Для влажных помещений (на базе " + gclass.lower() + ")"
        if f['temp_mode'] == "Низкие температуры":
            return "Быстросохнущий (" + gclass.lower() + ")"
        if f['load'] == "Высокая" and gclass != "Эластичный":
            return "Усиленный"
        if f['adhesion'] == "Низкая (требует грунтовки)":
            return gclass + " + грунтовка"
        return gclass

    def _infer_grout(self):
        """GROUT* — тип затирки."""
        f = self.facts
        hydro = self.derived['HYDRO']
        if hydro == "Обязательна" or f['frost'] == "Да":
            return "Эпоксидная"
        if f['joint_width'] == "Широкие (более 5 мм)":
            return "Декоративная"
        if hydro == "Желательна" or f['allergy_eco'] == "Да":
            return "Антигрибковая"
        return "Цементная"

    # ============================================================
    # Главный метод вывода
    # ============================================================
    def infer(self):
        # уровень 1
        self._derive_diffic()
        self._derive_elast()
        self._derive_wetenv()
        # уровень 2
        self._derive_skillreq()
        self._derive_glueclass()
        self._derive_hydro()
        # уровень 3
        self._derive_needpro()
        # уровень 4 (итоги)
        laypat = self._infer_laypat()
        glue   = self._infer_glue()
        grout  = self._infer_grout()

        recs = []
        d = self.derived
        recs.append(f"[DIFFIC*]    Сложность рисунка: {d['DIFFIC']}")
        recs.append(f"[ELAST*]     Эластичность клея: {d['ELAST']}")
        recs.append(f"[WETENV*]    Влажность среды:   {d['WETENV']}")
        recs.append(f"[SKILLREQ*]  Требуемый уровень мастерства: {d['SKILLREQ']}")
        recs.append(f"[GLUECLASS*] Класс клея:        {d['GLUECLASS']}")
        recs.append(f"[HYDRO*]     Гидроизоляция:     {d['HYDRO']}")
        recs.append(f"[NEEDPRO*]   Нужен профессионал: {d['NEEDPRO']}")
        recs.append("─" * 70)
        recs.append(f"[LAYPAT*] Способ укладки: {laypat}")
        recs.append(f"[GLUE*]   Тип клея:       {glue}")
        recs.append(f"[GROUT*]  Тип затирки:    {grout}")
        return recs

    # ============================================================
    # Вывод результата
    # ============================================================
    def show_result(self, recommendations):
        print("=" * 100)
        print("               ИТОГОВЫЕ РЕКОМЕНДАЦИИ")
        print("=" * 100)
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
