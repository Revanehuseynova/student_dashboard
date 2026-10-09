# Task 2 — Refactoring guide

Faylda: `task2_refactoring.py` (`calc` = əvvəl, qalan funksiyalar = sonra).

| Problem (BEFORE) | Qayda | Həll (AFTER) |
|---|---|---|
| `d`, `t`, `mx`, `mn`, `r`, `i`, `g` | Meaningful Names | `records`, `student_score`, `highest`, `lowest` |
| `90, 80, 70, 60, 100, 999` kodun içində | Magic Numbers | `MAX_SCORE`, `GRADE_THRESHOLDS` sabitləri |
| Bir funksiya yoxlayır, hesablayır, çap edir | Single Responsibility | `is_valid_score`, `calculate_grade`, `calculate_statistics`, `build_report`, `print_report` |
| 5 budaqlı `if/elif` zənciri | KISS | `GRADE_THRESHOLDS` üzərində sadə dövr |
| `i[1]` 10+ dəfə təkrarlanır | DRY | `score` bir dəfə açılır |
| `len(r) == 0` olduqda `ZeroDivisionError` | Düzgünlük | `calculate_statistics` boş siyahını idarə edir |
| Funksiya ~25 sətir | Funksiya ölçüsü | Hər funksiya 2–6 sətir |
