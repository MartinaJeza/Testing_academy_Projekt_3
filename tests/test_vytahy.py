import re

from playwright.sync_api import Page, expect

BASE_URL = "https://www.vytahyelex.cz/"

# ----------------------------------------------------------------------------
# 1. TS = Přijetí cookies
# ----------------------------------------------------------------------------
def test_cookie_banner_accept(page: Page, accept_cookies_if_present):
    """
    Ověří zobrazení cookie banneru a přijme cookies („Rozumím“).
    """
    page.goto(BASE_URL, wait_until="domcontentloaded")

    accept_cookies_if_present(page)

    # „druhá pojistka“ – banner by teď už neměl být vidět / aktivní
    cookies_banner = page.locator("div.cmplz-cookiebanner[role='dialog']").first
    try:
        expect(cookies_banner).to_be_hidden(timeout=2000)
    except AssertionError:
        expect(cookies_banner).to_have_attribute(
            "class", re.compile(r"^(?!.*\bcmplz-show\b).*$")
        )


# ----------------------------------------------------------------------------
# 2. TS = Kontakty → ověření URL → vyplnění HORNÍHO formuláře (NEodesílat)
# ----------------------------------------------------------------------------
def test_kontakty_form_na_strance(
    page: Page, base_url: str, accept_cookies_if_present
):
    """
    Z homepage kliknutím přejde na 'Kontakty', ověří URL,
    najde HORNÍ formulář a vyplní: jméno, e-mail, zprávu.
    NIC NEODESÍLÁ.
    """
    # otevři homepage
    page.goto(BASE_URL, wait_until="domcontentloaded")

    # cookies
    accept_cookies_if_present(page)

    # menu → Kontakty (desktop/mobil)
    link = page.locator("#menu-item-743 > a").first
    if link.count() and link.is_visible():
        link.click()
    else:
        burger = page.get_by_role("link", name=re.compile(r"mobile menu", re.I)).first
        if not burger.count():
            burger = page.locator(
                "a.responsive-menu-toggle[aria-label*='mobile menu' i]"
            ).first
        assert (
            burger.count() and burger.is_visible()
        ), "Burger menu nenalezeno – nemohu otevřít 'Kontakty'."
        burger.click()
        page.get_by_role("link", name="Kontakty").first.click()

    # ověření URL a ustálení stránky
    expect(page).to_have_url(re.compile(r"^https://www\.vytahyelex\.cz/kontakty/?$"))
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")

    # vyber přímo HORNÍ formulář (unikátní wrapper id)
    wrapper = page.locator("#wpcf7-f4-p740-o1").first
    expect(wrapper).to_be_visible(timeout=10000)

    # viditelný scroll k formuláři
    wrapper.evaluate(
        "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })"
    )
    page.wait_for_timeout(800)

    # fallback – pár „odrolování“ kolečkem, kdyby prohlížeč smooth ignoroval
    if not wrapper.is_visible():
        for _ in range(6):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(120)
    wrapper.scroll_into_view_if_needed()

    # pole (scopované do vybraného wrapperu)
    name_input = wrapper.locator("input[name='your-name']:visible").first
    email_input = wrapper.locator("input[name='your-email']:visible").first
    msg_input = wrapper.locator("textarea[name='your-message']:visible").first

    name_input.wait_for(state="visible", timeout=10000)
    email_input.wait_for(state="visible", timeout=10000)
    msg_input.wait_for(state="visible", timeout=10000)

    # vyplnění (NEodesílat)
    name_input.click()
    name_input.fill("Martina Ježková")

    email_input.click()
    email_input.fill("jezkova.m94@gmail.com")

    msg_input.click()
    msg_input.fill("Automatický test – prosím NEODESÍLAT.")

    # kontrola hodnot
    expect(name_input).to_have_value("Martina Ježková")
    expect(email_input).to_have_value("jezkova.m94@gmail.com")
    expect(msg_input).to_have_value("Automatický test – prosím NEODESÍLAT.")


# ----------------------------------------------------------------------------
# 3. TS = Kontakty → ověření URL → vyplnění formuláře v ZÁPATÍ (NEodesílat)
# ----------------------------------------------------------------------------
def test_kontakty_form_v_paticce(
    page: Page, base_url: str, accept_cookies_if_present
):
    """
    Z homepage klikne na 'Kontakty', ověří URL a vyplní
    formulář v ZÁPATÍ stránky (widget vpravo). NIC NEODESÍLÁ.
    """
    # otevři homepage
    page.goto(BASE_URL, wait_until="domcontentloaded")

    # cookies
    accept_cookies_if_present(page)

    # menu → Kontakty (desktop/mobil)
    link = page.locator("#menu-item-743 > a").first
    if link.count() and link.is_visible():
        link.click()
    else:
        burger = page.get_by_role("link", name=re.compile(r"mobile menu", re.I)).first
        if not burger.count():
            burger = page.locator(
                "a.responsive-menu-toggle[aria-label*='mobile menu' i]"
            ).first
        assert (
            burger.count() and burger.is_visible()
        ), "Burger menu nenalezeno – nemohu otevřít 'Kontakty'."
        burger.click()
        page.get_by_role("link", name="Kontakty").first.click()

    # ověření URL a ustálení stránky
    expect(page).to_have_url(re.compile(r"^https://www\.vytahyelex\.cz/kontakty/?$"))
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")

    # ZÁPATÍ – unikátní wrapper id tohoto CF7 formuláře
    wrapper = page.locator("#wpcf7-f4-o2").first
    expect(wrapper).to_be_visible(timeout=10000)

    # viditelný scroll k formuláři
    wrapper.evaluate(
        "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })"
    )
    page.wait_for_timeout(800)
    if not wrapper.is_visible():
        for _ in range(6):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(120)
    wrapper.scroll_into_view_if_needed()

    # pole (scopované do wrapperu)
    name_input = wrapper.locator("input[name='your-name']:visible").first
    email_input = wrapper.locator("input[name='your-email']:visible").first
    msg_input = wrapper.locator("textarea[name='your-message']:visible").first

    name_input.wait_for(state="visible", timeout=10000)
    email_input.wait_for(state="visible", timeout=10000)
    msg_input.wait_for(state="visible", timeout=10000)

    # vyplnění (NEodesílat)
    name_input.click()
    name_input.fill("Martina Ježková")

    email_input.click()
    email_input.fill("jezkova.m94@gmail.com")

    msg_input.click()
    msg_input.fill("Automatický test – prosím NEODESÍLAT.")

    # kontrola hodnot
    expect(name_input).to_have_value("Martina Ježková")
    expect(email_input).to_have_value("jezkova.m94@gmail.com")
    expect(msg_input).to_have_value("Automatický test – prosím NEODESÍLAT.")