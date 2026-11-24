import csv
from collections import defaultdict

subjects = {
    "eng1": "Englisch", "eth1": "Ethik", "deu1": "Deutsch",
    "rus1": "Russisch", "MA1": "Mathematik", "phy1": "Physik",
    "spo1": "Sport", "ggk1": "Gemeinschaftskunde", "lit1": "Literatur",
    "kun1": "Kunst", "DIT06": "LF06", "DIT07": "LF07",
    "DIT08": "LF08", "DIT09": "LF09", "DIT10": "LF10", "DIT11": "LF11",
}

russian_translations = {
    "LK nachholen bzw. nachbessern sowie auswerten": "Leistungskontrolle nachholen bzw. verbessern und auswerten",
    "Читаем текст «Хобби» и отвечаем на вопросы/ моё свободное время": "Wir lesen den Text „Hobbys“ und beantworten Fragen zu meiner Freizeit",
    "множественное число": "Plural",
    "Читаем книгу «Каникулы в Петербурге» и пишем краткое содержание на немецком языке": "Wir lesen das Buch „Ferien in Petersburg“ und schreiben eine Kurzfassung auf Deutsch",
    "читаем и отвечаем: правильно или неправильно": "Wir lesen und antworten: richtig oder falsch",
    "читаем книгу до конца и отвечаем вместе правильно или неправильно": "Wir lesen das Buch bis zum Ende und antworten gemeinsam: richtig oder falsch",
    "Готовимся к контрольной работе": "Wir bereiten uns auf die Kontrollarbeit vor",
    "Контрольная работа 12.1": "Kontrollarbeit 12.1",
}

by_day = defaultdict(list)
with open("live_test_export.csv", "r", encoding="utf-8-sig", newline="") as source:
    for row in csv.DictReader(source):
        by_day[row["date"]].append(row)

sections = []
for day in sorted(by_day):
    rows = by_day[day]
    blocks = []
    for row in rows:
        subject_code = row["subject"]
        subject = subjects.get(subject_code, subject_code)
        topic = row["lesson_topic"].strip()
        if subject == "Russisch" and topic in russian_translations:
            topic = f"{topic}\n({russian_translations[topic]})"
        blocks.append(
            f"Fach: {subject}\n"
            f"Zeit: {row['start']} - {row['end']}\n"
            f"Thema:\n{topic}"
        )

    sections.append(
        f"Tag: {rows[0]['weekday']}, {day}\n\n" + "\n\n".join(blocks)
    )

output = "berichtsheft_2026-10-26_2026-11-20.txt"
with open(output, "w", encoding="utf-8") as target:
    target.write("\n\n\n".join(sections))

print(f"TXT geschrieben: {output}")
print(f"Tage: {len(sections)}, Einträge: {sum(len(rows) for rows in by_day.values())}")
