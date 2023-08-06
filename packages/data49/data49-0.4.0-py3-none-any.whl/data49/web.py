import contextlib
import enum
import functools
import importlib
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union, Tuple, Sequence
import warnings

import selenium.common.exceptions as selenium_exceptions
from bs4 import BeautifulSoup
from requests import get, post  # As for API
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webdriver, webelement
from selenium.webdriver.support import expected_conditions  # As for API
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore[attr-defined]

from . import internal

__all__ = [
    "get_browser",
    "Browser",
    "BrowserType",
    "BrowserContext",
    "Element",
    "expected_conditions",
    "get",
    "post",
    "Soup",  # TODO: Better name
]


def Soup(html: str, **kwargs) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser", **kwargs)


class BrowserType(enum.Enum):
    """An enumeration of popular, supported browsers for browser automation"""

    CHROME = {"name": "Chrome", "make_headless": lambda x: x.add_argument("--headless")}
    SAFARI = {"name": "Safari", "make_headless": None}
    FIREFOX = {
        "name": "Firefox",
        "make_headless": lambda x: setattr(x, "headless", True),
    }


__get_browser_cache: Dict[
    Tuple[Tuple[BrowserType, ...], bool, Optional[Tuple[str, ...]]],
    Optional[webdriver.WebDriver],
] = {}


def get_browser(
    priority: Tuple[BrowserType, ...] = (
        BrowserType.CHROME,
        BrowserType.FIREFOX,
        BrowserType.SAFARI,
    ),
    headless: bool = True,
    arguments: Optional[Sequence[str]] = None,
) -> webdriver.WebDriver:
    """Lil' helper function to attempt to get a valid WebDriver"""
    _cache_key = (
        priority,
        headless,
        tuple(arguments) if arguments is not None else None,
    )
    if _cache_key in __get_browser_cache:
        if __get_browser_cache[_cache_key] is None:
            raise RuntimeError("Could not find any browser that supports your needs")

    def _(browser_name: BrowserType) -> Optional[webdriver.WebDriver]:
        try:
            options = importlib.import_module(
                ".options", f"selenium.webdriver.{browser_name.value['name'].lower()}"
            ).Options()
            if headless:
                try:
                    browser_name.value["make_headless"](options)
                except TypeError:
                    return None
            if arguments:
                for arg in arguments:
                    options.add_argument(arg)
            browser = functools.partial(
                getattr(
                    importlib.import_module(".webdriver", "selenium"),
                    browser_name.value["name"],
                ),
                options=options,
                service_log_path=os.devnull,
            )
            # There is no better way to check than to open and close it...
            browser().close()
        except selenium_exceptions.WebDriverException:
            return None
        else:
            return browser

    for browser in priority:
        found = _(browser)
        if found is not None:
            __get_browser_cache[_cache_key] = found
            return found
    __get_browser_cache[_cache_key] = None
    # TODO: Download geckodriver and use it
    raise RuntimeError("Could not find any browser that supports your needs")


@internal.add_typo_safety
@dataclass
class Element:
    """Represents a DOM element.

    Should not be instantiated directly but instead with methods like :meth:`BrowserContext.query_selector`
    """

    item: webelement.WebElement

    def soup(self) -> BeautifulSoup:
        return Soup(self["innerHTML"])

    # get_attribute documentation says it may return booleans...
    # @functools.lru_cache()
    def get(self, attr: str) -> Optional[str]:
        return self.item.get_attribute(attr)  # type: ignore

    def __getitem__(self, attr: str) -> str:
        output = self.get(attr)
        if output is None:
            raise KeyError(attr)
        return output

    def click(self) -> None:
        self.item.click()  # type: ignore

    def send_keys(self, keys) -> None:
        self.item.send_keys(keys)  # type: ignore


@internal.add_typo_safety
@dataclass
class BrowserContext:
    url: str
    driver: webdriver.WebDriver
    _waits: Dict[float, WebDriverWait] = field(default_factory=dict)

    def go(self, to: str) -> None:
        self.driver.get(to)

    def query_selector(self, css_selector: str) -> Element:
        """Instantly find an element that matches the given CSS selector

        .. note::

            If the element you want to find isn't readily available, you can use
            :meth:`wait` instead (or :meth:`css`, which combines this with :meth:`wait`).

        Args:
            css_selector (str): The CSS selector to match

        Returns:
            Element: The element found by the given CSS selector

        Raises:
            NoElementException: The element doesn't exist

        """
        return Element(self.driver.find_element(By.CSS_SELECTOR, css_selector))

    def css(self, css_selector: str, wait_up_to: float = 10.0) -> Element:
        return self.wait(
            expected_conditions.presence_of_element_located(  # type: ignore
                (By.CSS_SELECTOR, css_selector)
            ),
            wait_up_to,
        )

    # TODO: css_all

    def query_selector_all(self, css_selector: str) -> List[Element]:
        return list(
            map(Element, self.driver.find_elements(By.CSS_SELECTOR, css_selector))
        )

    def js(self, javascript: str) -> Any:
        return self.driver.execute_script(javascript)

    def _get_wait_up_to(self, seconds: float) -> WebDriverWait:
        if seconds not in self._waits:
            self._waits[seconds] = WebDriverWait(self.driver, seconds)
        return self._waits[seconds]

    def wait(
        self,
        until: Callable[[webdriver.WebDriver], Union[webelement.WebElement, bool]],
        up_to: float = 10.0,
    ) -> Element:
        """Wait until an element is located.

        Returns that `Element` if found under `up_to`, the time limit in seconds.

        Raises `TimeoutError` if the element is not found in time.

        Args:
            until (Callable[[webdriver.WebDriver], Union[webelement.WebElement, bool]]):
                        An object that when `__call__` is called,
                        return `False` indicating that the element was not found
                        or the `selenium.webdriver.remote` when found.
                        You may use Selenium's `expected_conditions`.
            up_to (float): The time limit in seconds. Defaults to 10.0.

        Returns:
            Element: The element that was found

        Raises:
            TimeoutError: The element was not found in time.

        """
        try:
            return Element(self._get_wait_up_to(up_to).until(until))
        except selenium_exceptions.TimeoutException as error:
            raise TimeoutError(
                f"Could not find element under {up_to} seconds"
            ) from error

    # def wait_until  # Recieves a function that returns boolean as parameter. Polls.


@internal.add_typo_safety
@dataclass
class Browser(contextlib.AbstractContextManager):
    """
    >>> with Browser("https://google.com"): pass
    >>> with Browser("https://google.com", driver=get_browser(priority=(BrowserType.FIREFOX,))):
    ...     pass
    >>> from selenium import webdriver
    >>> from selenium.webdriver.firefox.options import Options
    >>> with Browser("https://google.com", driver=lambda: webdriver.Firefox(options=Options)):
    ...     pass
    >>> with Browser("https://google.com", driver=webdriver.Ie): pass
    """

    url: str
    # pylint: disable=unnecessary-lambda
    # No, we need that lambda for lazy loading
    driver: webdriver.WebDriver = field(default_factory=get_browser)

    def __post_init__(self):
        self.driver = self.driver()

    def open(self) -> BrowserContext:
        self.driver.get(self.url)
        return BrowserContext(self.url, self.driver)

    def close(self) -> None:
        self.driver.close()

    def __enter__(self) -> BrowserContext:
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
