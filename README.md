# Testing_academy_Projekt_3

# Tři automatizované testy (Playwright)

Autor: Martina Ježková
Email: jezkova.m94@gmail.com
----------------------------------------------------------

## Obsah: 
1. 🎯 Cíl projektu
2. 🗂 Struktura projektu
3. 🤖 Co se testuje
4. ⚙️ Požadavky
5. ▶️ Spuštění (krok za krokem)
6. 🧪 Spouštění testů – příklady
7. 📝 Poznámky

----------------------------------------------------------

# 🎯 Cíl projektu

Vytvořit alespoň 3 automatizované testy nad webem https://www.vytahyelex.cz/ 
pomocí Playwright + pytest

Testy běží napříč prohlížeči (Chromium, Firefox, WebKit) a pro dva profily (desktop a iPhone 13). 

Mobilní profil je ve Firefoxu automaticky přeskočen (nepodporuje mobilní emulaci).

⚠️ Bezpečnost/Test hygiene: Formuláře na produkčním webu se NEODESÍLAJÍ.
Testy pouze vyplňují pole a ověřují hodnoty.


# 🗂 Struktura projektu

```
Projekt_3/
├─ tests/
│  ├─ conftest.py
│  └─ test_vytahy.py
├─ pytest.ini
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

# 🤖 Co se testuje

1. **test_cookie_banner_accept**

- Otevře homepage
- Robustně přijme/uzavře cookie banner 
- Ověří, že banner zmizel (nebo aspoň nemá třídu cmplz-show)

2. **test_kontakty_form_na_strance**
(horní formulář na stránce Kontakty)

- Klik na Kontakty z hlavního menu / burger menu
- Ověření URL .../kontakty/
- Plynulý scroll k hornímu formuláři (#wpcf7-f4-p740-o1)
- Vyplnění **jméno, e-mail, zpráva** a ověření hodnot
- **NEodesílá!**

3. **test_kontakty_form_v_paticce**
(formulář v zápatí)

- Stejný postup, ale cílí na wrapper #wpcf7-f4-o2
- Vyplnění polí + ověření
- **NEodesílá**

# ⚙️ Požadavky

- Python 3.10+ (doporučeno 3.11+)
- macOS / Linux / Windows
- Nainstalované prohlížeče pro Playwright

# ▶️ Spuštění
1. Ujisti se, že máš nainstalovaný Python 3.10+
    ```bash
    python --version
    ```

  nebo v některých systémech:
    ```bash 
    python3 --version
    ```

2. V terminálu/příkaz. řádku se přesuň do složky, kde máš uložené soubory
  z repozitáře https://github.com/MartinaJeza/Testing_academy_Projekt_3.git
    ```bash 
    cd /cesta/k/projektu
    ```

💡Virtuální prostředí 
(doporučeno až **povinné**, aby nedošlo k rozhození vašich jiných projektů!):

3. Vytvoř si virtuální prostředí:
    ```bash 
    python3 -m venv nazev_vir_prostredi
    ```

4. Aktivuj prostředí: 
    macOS/Linux:
    ```bash
    source nazev_vir_prostredi/bin/activate
    ```

    Windows:
    ```bash 
    nazev_vir_prostredi\Scripts\activate
    ```

💡Instalace knihoven:

5. Nainstaluj požadované knihovny pomocí requirements.txt
    ```bash 
    pip install -r requirements.txt
    ```

6. Nainstaluj Playwright prohlížeče:
    ```bash
    playwright install
    ```

# 🧪 Spouštění testů – příklady 

- Všechny testy (3 prohlížeče x 2 profily; mobil ve Firefoxu se přeskočí):
    ```bash 
    pytest
    ```

- Konfigurace (pytest.ini)
    Ukázkový obsah: 
    ```
    [pytest]
    addopts = --headed --browser chromium --browser firefox --browser webkit
    testpaths = tests
    ```

- CLI parametry mají přednost, takže když chceš třeba jen Chromium:
    ```bash
    pytest -o addopts="" --headed --browser=chromium
    ```

- Jen konkrétní test
    ```bash
    pytest -k test_cookie_banner_accept
    pytest -k test_kontakty_form_na_strance
    pytest -k test_kontakty_form_v_paticce
    ```


# 7. 📝 Poznámky

- Firefox nepodporuje isMobile → mobilní běh je přeskočen (řešeno ve conftest.py).
- Selektory formulářů jsou scoped přes unikátní wrapper ID (#wpcf7-f4-p740-o1, #wpcf7-f4-o2) + name + :visible, aby se netrefil jiný formulář.
- Pro základní lint/format lze použít Ruff (viz pyproject.toml).
Příklad: 
 ```bash
 ruff check --fix tests/test_vytahy.py
 ```

