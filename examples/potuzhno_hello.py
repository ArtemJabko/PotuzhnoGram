from base_plugin import BasePlugin
from ui.settings import Header

__id__ = "potuzhno_hello"
__name__ = "Потужно • Привіт"
__description__ = "Перевірка завантаження плагінів ПотужноGram."
__author__ = "PotuzhnoGram"
__version__ = "1.0.0"

class PotuzhnoHello(BasePlugin):
    def create_settings(self):
        return [Header(text="ПотужноGram 🇺🇦 — плагін працює")]
