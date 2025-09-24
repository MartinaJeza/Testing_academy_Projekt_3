import re

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(params=["desktop", "iphone 13"], ids=["desktop", "iphone13"])
def context(browser, playwright, request, browser_name):
    """
    Deskop a mobilní profil (iPhone 13).
    Pro Firefox mobilní profil přeskočíme (nepodporuje mobile emulaci).
    """
    # přeskoč mobilní profil ve Firefoxu
    if request.param != "desktop" and browser_name == "firefox":
        pytest.skip("Firefox nepodporuje mobile emulaci – mobilní profil přeskočen.")

    if request.param == "desktop":
        browser_context = browser.new_context()
    else:
        browser_context = browser.new_context(**playwright.devices["iPhone 13"])

    try:
        yield browser_context
    finally:
        browser_context.close()


@pytest.fixture
def page(context):
    page_obj = context.new_page()
    try:
        yield page_obj
    finally:
        page_obj.close()


@pytest.fixture
def accept_cookies_if_present():
    """
    Vrátí funkci, která spolehlivě přijme / zavře cookie banner
    na aktuální stránce (napříč prohlížeči).
    Použití v testu: accept_cookies_if_present(page)
    """
    def _accept(page: Page) -> None:
        banner = page.locator("div.cmplz-cookiebanner[role='dialog']").first

        # 1) krátce počkej, jestli se banner objeví
        try:
            banner.wait_for(state="visible", timeout=3000)
        except Exception:
            return  # žádný banner = není co řešit

        # 2) pro jistotu do viewportu (často nutné ve WebKitu / iOS emulaci)
        try:
            banner.scroll_into_view_if_needed()
        except Exception:
            pass

        # 3) primárně podle role/label (CZ/EN), fallback přes třídu
        btn_accept = banner.get_by_role(
            "button",
            name=re.compile(r"(rozumím|accept|i understand|souhlasím|ok)", re.I),
        ).first
        if not btn_accept.count():
            btn_accept = banner.locator("button.cmplz-accept").first

        # fallback: uložit předvolby / odmítnout
        if btn_accept.count():
            try:
                btn_accept.scroll_into_view_if_needed()
                btn_accept.click(timeout=5000)
            except Exception:
                btn_accept.click(force=True)
        else:
            btn_save = banner.get_by_role(
                "button",
                name=re.compile(r"(uložit předvolby|save preferences)", re.I),
            ).first
            if btn_save.count():
                btn_save.click()
            else:
                banner.locator("button.cmplz-deny").first.click()

        # 4) ověř, že banner zmizel (nebo aspoň není 'cmplz-show')
        try:
            expect(banner).to_be_hidden(timeout=5000)
        except AssertionError:
            expect(banner).to_have_attribute(
                "class", re.compile(r"^(?!.*\bcmplz-show\b).*$"), timeout=7000
            )

    return _accept