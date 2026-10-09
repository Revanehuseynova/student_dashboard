# Student Performance Dashboard 🎓

Streamlit + SQL Server (`UniversityDB`) ilə tələbə nəticələrinin idarə edilməsi.
Clean Code və qatlı (layered) memarlıq:

```
SQL Server (UniversityDB, GetStudentResult)
        ↓
database.py   – bazaya giriş
        ↓
services.py   – grade, statistika, validasiya
        ↓
app.py        – Streamlit interfeysi
```

## Fayllar
| Fayl | Məqsəd |
|---|---|
| `config.py` | Bütün sabitlər (magic number yoxdur) |
| `database.py` | `create_connection`, `add_student`, `get_students`, `get_student` |
| `services.py` | `calculate_grade`, `calculate_statistics`, validasiya |
| `app.py` | UI: əlavə et, siyahı, axtarış, statistika, qrafik |
| `task1_university_db.sql` | **Task 1** – baza, cədvəl, `GetStudentResult` |
| `task2_refactoring.py` + `docs/task2_refactoring_guide.md` | **Task 2** – refactoring |
| `tests/test_services.py` | Unit testlər |

## Qurulum
```bash
pip install -r requirements.txt
sqlcmd -S ".\SQLEXPRESS" -E -i task1_university_db.sql   # və ya SSMS-də icra edin
python -m unittest discover tests
python task2_refactoring.py
streamlit run app.py        # və ya run.bat
```
Server adı fərqlidirsə: `set DB_SERVER=localhost` (Windows) əvvəl təyin edin.

## Grade cədvəli
90+ → A, 80+ → B, 70+ → C, 60+ → D, qalanı F.
