import os
from solution import get_letters, count_category, main


class DummyResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


def test_get_letters(monkeypatch):
    html = """
    <div id="mw-subcategories">
      <a href="/wiki/Категория:Животные_на_A">Животные на A</a>
      <a href="/wiki/Категория:Животные_на_B">Животные на B</a>
      <a href="/wiki/Категория:Животные_на_В">Животные на В</a>
    </div>
    """
    monkeypatch.setattr("solution.requests.get", lambda url: DummyResponse(html))
    letters = get_letters()
    assert letters == {
        "A": "https://ru.wikipedia.org/wiki/Категория:Животные_на_A",
        "B": "https://ru.wikipedia.org/wiki/Категория:Животные_на_B",
        "В": "https://ru.wikipedia.org/wiki/Категория:Животные_на_В",
    }


def test_count_category_single_page(monkeypatch):
    html = """
    <div id="mw-pages">
      <ul>
        <li><a>Животное1</a></li>
        <li><a>Животное2</a></li>
        <li><a>Животное3</a></li>
      </ul>
    </div>
    """
    monkeypatch.setattr("solution.requests.get", lambda url: DummyResponse(html))
    assert count_category("any") == 3


def test_count_category_with_next(monkeypatch):
    html1 = """
    <div id="mw-pages">
      <ul>
        <li><a>Жив1</a></li>
        <li><a>Жив2</a></li>
      </ul>
      <a href="/next">Следующая страница</a>
    </div>
    """
    html2 = """
    <div id="mw-pages">
      <ul>
        <li><a>Жив3</a></li>
      </ul>
    </div>
    """
    calls = {"count": 0}

    def fake_get(url):
        calls["count"] += 1
        return DummyResponse(html1 if calls["count"] == 1 else html2)

    monkeypatch.setattr("solution.requests.get", fake_get)
    assert count_category("any") == 3
    assert calls["count"] == 2


def test_main_writes_csv(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "solution.get_letters",
        lambda: {"А": "urlA", "Б": "urlB", "Я": "urlY"},
    )
    monkeypatch.setattr(
        "solution.count_category",
        lambda u: {"urlA": 10, "urlB": 20, "urlY": 5}[u],
    )

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        main()
        data = (tmp_path / "beasts.csv").read_text(encoding="utf-8").splitlines()
        assert "А,10" == data[0]
        assert "Б,20" == data[1]
        assert any(line == "Я,5" for line in data)
    finally:
        os.chdir(cwd)
