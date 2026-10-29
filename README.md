<div align="center">
  <img src="branding/logo.svg" width="128" alt="PotuznoGram logo">
  <h1>PotuznoGram 🇺🇦</h1>
  <a href="https://t.me/PotuznoGram">Telegram</a> ·
  <a href="https://github.com/ArtemJabko/PotuzhnoGram/releases">Releases</a>
</div>

## Українська

Неофіційний Telegram-клієнт для Android на базі Telegram **12.10.6**.

- Українські іконки та світла й темна синьо-жовті теми з фотошпалерами.
- Python-плагіни та розширені налаштування інтерфейсу.
- **ПотужноМетр** — жартівливий симулятор зі звуками у Preferences.
- Окремий пакет `ua.potuzhnogram.messenger`: можна встановити поруч з Telegram.

### Збирання

Використовуй Linux або Ubuntu у WSL. Потрібні Git, JDK 21, Python 3.11, `nasm`, `ninja-build`, `pkg-config` та Android SDK: Platform 37, Build Tools 36.0.0, NDK 27.2.12479018, CMake 3.31.6.

```bash
git clone --recursive --shallow-submodules https://github.com/ArtemJabko/PotuzhnoGram.git
cd PotuzhnoGram
cp local.properties.example local.properties
```

У `local.properties` вкажи шлях до **Linux SDK** та власні `TELEGRAM_APP_ID` і `TELEGRAM_APP_HASH` з [my.telegram.org/apps](https://my.telegram.org/apps). Додай Python 3.11 і CMake до `PATH`, потім:

```bash
python3.11 build.py --abi arm64-v8a
```

APK: `client/TMessagesProj/build/outputs/apk/`. Для емулятора використовуй `--abi x86_64`.

Для публічного релізу налаштуй власний ключ `client/TMessagesProj/release.keystore` та `KEYSTORE_PASS`, `ALIAS_NAME`, `ALIAS_PASS` у `local.properties`, після чого додай `--release`. Без ключа використовується debug-підпис. Не публікуй ключі й `local.properties`.

Для FCM-сповіщень потрібен власний `google-services.json` у корені проєкту для пакета `ua.potuzhnogram.messenger`.

## English

An unofficial Android Telegram client based on Telegram **12.10.6**.

- Ukrainian app icons and light/dark blue-and-yellow themes with photo wallpapers.
- Python plugins and extended interface settings.
- **PotuzhnoMeter** — a playful sound-enabled simulator in Preferences.
- Separate package `ua.potuzhnogram.messenger`: install alongside Telegram.

### Building

Use Linux or Ubuntu in WSL. Requirements: Git, JDK 21, Python 3.11, `nasm`, `ninja-build`, `pkg-config`, and Android SDK: Platform 37, Build Tools 36.0.0, NDK 27.2.12479018, CMake 3.31.6.

```bash
git clone --recursive --shallow-submodules https://github.com/ArtemJabko/PotuzhnoGram.git
cd PotuzhnoGram
cp local.properties.example local.properties
```

Set the **Linux SDK** path and your own `TELEGRAM_APP_ID` and `TELEGRAM_APP_HASH` from [my.telegram.org/apps](https://my.telegram.org/apps) in `local.properties`. Add Python 3.11 and CMake to `PATH`, then run:

```bash
python3.11 build.py --abi arm64-v8a
```

APK output: `client/TMessagesProj/build/outputs/apk/`. Use `--abi x86_64` for an emulator.

For a public release, configure your own `client/TMessagesProj/release.keystore` and `KEYSTORE_PASS`, `ALIAS_NAME`, `ALIAS_PASS` in `local.properties`, then add `--release`. Without a keystore, the build uses debug signing. Keep keys and `local.properties` private.

FCM notifications require your own `google-services.json` in the project root for package `ua.potuzhnogram.messenger`.

---

**Основа / Based on:** [exteraless](https://github.com/exteraless/exteraless) and its contributors. Успадкований дизайн / Inherited design: [@the8055u](https://t.me/the8055u), [@BlueprintDsgn](https://t.me/BlueprintDsgn).

**Ліцензія / License:** [GPL-3.0](LICENSE). Сторонні матеріали зберігають власні ліцензії / Third-party materials retain their own licenses.
