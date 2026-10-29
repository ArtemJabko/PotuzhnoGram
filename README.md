<div align="center">

<img src="branding/icon.jpg" width="160" alt="PotuzhnoGram">

# ПотужноGram 🇺🇦
### Telegram з українським характером
### Telegram with Ukrainian character

</div>

---

## 🇺🇦 Українська

ПотужноGram — незалежний неофіційний Telegram-клієнт для Android з українським оформленням та підтримкою Python-плагінів.

### Можливості

- Синьо-жовта іконка з українською символікою.
- Світла тема «Потужно • День» і темна «Потужно • Ніч».
- Вбудовані шпалери з орнаментом у стилі вишивки.
- «Батько наш Бандера — minions vocal» як стандартна мелодія вхідних дзвінків.
- Можливість змінювати тему, шпалери та мелодію.
- Python-плагіни на основі відкритого рушія exteraless.
- Окремий пакет `ua.potuzhnogram.messenger` для встановлення поруч з іншими клієнтами.

Власноруч вибрані звуки зберігаються. Основа має шар сумісності з API exteraGram, але робота кожного плагіна exteraGram або AyuGram не гарантується.

### Стан проєкту

Підготовлено зміни вихідного коду, оформлення, мелодію та сценарії підготовки й збирання. Перевірено застосування патча, повторну підготовку, цілісність ресурсів і завантаження прикладу плагіна з SDK.

**Успішне збирання APK та роботу на телефоні ще не підтверджено.**

### Завантаження та підготовка

Виконай на комп’ютері:

    git clone --recursive --shallow-submodules https://github.com/ArtemJabko/PotuzhnoGram.git
    cd PotuzhnoGram
    python prepare.py

Якщо підмодулі не завантажені:

    git submodule update --init --recursive --depth=1
    python prepare.py

### Збирання APK

Потрібні Git, JDK 21, Python 3.11, Android SDK 37, Build Tools 36.0.0, NDK 27.2.12479018 та CMake 3.31.6 або новіша сумісна версія.

1. Отримай власні `api_id` і `api_hash` на https://my.telegram.org/apps.
2. Скопіюй `local.properties.example` у `local.properties`.
3. Заповни `TELEGRAM_APP_ID`, `TELEGRAM_APP_HASH` і шлях до Android SDK.
4. Запусти `python build.py`.

Типово збирається debug APK для ARM64. Додаткові варіанти:

    python build.py --abi universal
    python build.py --release

Результат: `client/TMessagesProj/build/outputs/apk/`.

Для Android Studio спочатку виконай підготовку, потім відкрий папку `client` та вибери JDK 21.

Для власного підпису поклади ключ у `client/TMessagesProj/release.keystore` і заповни параметри підпису в `local.properties`. Без власного ключа основа використовує debug-підпис, зокрема для release-збирання.

### Сповіщення

Для FCM додай власний `google-services.json` у корінь проєкту перед підготовкою. У Firebase зареєструй пакет `ua.potuzhnogram.messenger`.

Без конфігурації FCM доставка сповіщень у фоні залежить від інших механізмів клієнта й обмежень Android.

### Плагіни

Відкрий розділ плагінів у налаштуваннях клієнта, увімкни рушій та встанови файл `.py`.

Приклад: `examples/potuzhno_hello.py`.

Успадковано модель дозволів exteraless. Плагіни, залежні від закритих класів або іншої версії API, можуть потребувати адаптації.

### Структура проєкту

- `client` — Android-основа, закріплена як Git-підмодуль.
- `patches` — зміни вихідного коду ПотужноGram.
- `overlay` — іконки, теми та мелодія.
- `branding` — попередній перегляд оформлення.
- `examples` — приклад плагіна.
- `prepare.py` — підготовка вихідного коду.
- `build.py` — запуск локального збирання.

### Автори та ліцензії

Основа: [exteraless](https://github.com/exteraless/exteraless), відкритий форк NagramX. Подяка авторам Telegram, NagramX, Nagram, Nekogram, exteraGram, AyuGram та інших складових.

Автори успадкованого оформлення exteraGram: @the8055u та @BlueprintDsgn. Початковий опис основи збережено в `UPSTREAM.md`.

Ліцензія основи GPL-3.0 збережена у `LICENSE`. Сторонні компоненти зберігають власні ліцензії. Аудіозапис не перелiцензовується під GPL; права належать відповідним правовласникам.

ПотужноGram не є офіційним застосунком Telegram.

---

## 🇬🇧 English

PotuzhnoGram is an independent, unofficial Telegram client for Android with Ukrainian styling and Python plugin support.

### Features

- Blue-and-yellow app icon with Ukrainian symbolism.
- “Потужно • День” light theme and “Потужно • Ніч” dark theme.
- Bundled embroidery-inspired wallpapers.
- “Батько наш Бандера — minions vocal” as the default incoming-call ringtone.
- Customizable themes, wallpapers and ringtones.
- Python plugins powered by the open-source exteraless engine.
- Separate application ID, `ua.potuzhnogram.messenger`, for installation alongside other clients.

Manually selected ringtones are preserved. The foundation includes an exteraGram API compatibility layer, but compatibility with every exteraGram or AyuGram plugin is not guaranteed.

### Project status

Source modifications, visual assets, the ringtone and preparation/build scripts are provided. Patch application, repeated preparation, asset integrity and loading the example plugin with the upstream SDK have been checked.

**A successful APK build and on-device operation have not yet been verified.**

### Download and prepare

Run on your computer:

    git clone --recursive --shallow-submodules https://github.com/ArtemJabko/PotuzhnoGram.git
    cd PotuzhnoGram
    python prepare.py

If submodules were omitted:

    git submodule update --init --recursive --depth=1
    python prepare.py

### Build the APK

Requirements: Git, JDK 21, Python 3.11, Android SDK 37, Build Tools 36.0.0, NDK 27.2.12479018 and CMake 3.31.6 or a newer compatible version.

1. Obtain your own `api_id` and `api_hash` at https://my.telegram.org/apps.
2. Copy `local.properties.example` to `local.properties`.
3. Set `TELEGRAM_APP_ID`, `TELEGRAM_APP_HASH` and your Android SDK path.
4. Run `python build.py`.

The default output is an ARM64 debug APK. Additional options:

    python build.py --abi universal
    python build.py --release

Output: `client/TMessagesProj/build/outputs/apk/`.

For Android Studio, run preparation first, open the `client` directory and select JDK 21.

For custom signing, place your keystore at `client/TMessagesProj/release.keystore` and configure signing in `local.properties`. Without a custom keystore, the foundation uses debug signing, including for release builds.

### Notifications

For FCM, place your own `google-services.json` in the project root before preparation. Register `ua.potuzhnogram.messenger` as the Android application ID in Firebase.

Without FCM configuration, background notification delivery depends on the client's other mechanisms and Android restrictions.

### Plugins

Open the plugin section in client settings, enable the engine and install a `.py` file.

Example: `examples/potuzhno_hello.py`.

The project inherits the exteraless permission model. Plugins relying on private classes or a different API version may require adaptation.

### Project structure

- `client` — Android foundation pinned as a Git submodule.
- `patches` — PotuzhnoGram source modifications.
- `overlay` — icons, themes and ringtone.
- `branding` — visual previews.
- `examples` — example plugin.
- `prepare.py` — source preparation.
- `build.py` — local build launcher.

### Credits and licensing

Based on [exteraless](https://github.com/exteraless/exteraless), an open-source NagramX fork. Thanks to the authors of Telegram, NagramX, Nagram, Nekogram, exteraGram, AyuGram and other upstream components.

Inherited exteraGram design credits: @the8055u and @BlueprintDsgn. The original upstream description is preserved in `UPSTREAM.md`.

The upstream GPL-3.0 license is preserved in `LICENSE`. Third-party components retain their respective licenses. The audio recording is not relicensed under GPL; its rights remain with the respective rights holders.

PotuzhnoGram is not an official Telegram application.


## PotuznoGram branding update

The default branch is `main`, pinned to Telegram 12.10.6. The visible app name is
PotuznoGram; the Android package remains `ua.potuzhnogram.messenger`, preserving
app data when upgrading with the same signing key. Channel: https://t.me/PotuznoGram.

Five Ukrainian icon styles are available in Chat Settings → App Icon: PotuznoGram,
Вишиванка, Соняшник, Піксель and Льодяник. Original icon choices remain available.
The PotuznoGram icon is also used in Preferences, onboarding and the updater.
The two Потужно themes use a yellow-and-blue palette and include the supplied
photo as their bundled chat wallpaper.
Select Потужно • День or Потужно • Ніч in Chat Settings to use them. Chat-specific
wallpapers still take precedence, as in Telegram.

`python3.11 prepare.py` supports upgrading the previous 12.10.6 branding in place.
It replaces only recognized original assets and refuses conflicting local edits.
Keep your `local.properties`, signing keys and any local changes. Do not reset the
client or remove those files to resolve a preparation conflict.

Host checks: `python3.11 scripts/check.py` and `python3.11 scripts/check_branding.py`.
These do not replace an APK build and an emulator/device test.
The vector artwork is in `branding/icons`; density assets can be regenerated with
`python scripts/generate_branding.py` (host dependency: cairosvg).


### Readability update
The day/night themes now inherit complete bundled palettes, including chat-list,
media and glass-navigation colours. Native theme contrast checks are available via
`python scripts/check_contrast.py`. The default chat-list title uses PotuznoGram;
explicit custom titles remain supported. The in-app logo has rounded transparent
corners. Three extra vector icons: Потужний рейс, Вареник and Поштовий голуб.

After installing this update, reselect Потужно • День or Потужно • Ніч if an older
theme is still cached. Custom per-chat wallpapers retain their existing behaviour.


### ПотужноМетр and wallpaper fix
Preferences → ПотужноМетр opens an offline playful meter. Hold to charge it;
release to pause. At full power it plays an original explosion effect. Tap to
reset. The sound toggle uses media volume; playback stops on leaving the screen.
This is a joke simulator, not a radiation measurement device. No sensors,
microphone or network are used.

Photo themes use v4 assets without `chat_wallpaper` colour keys, which otherwise
take precedence over embedded JPEGs. Existing per-chat wallpaper overrides are
preserved. Reselect the Потужно day/night theme after updating if necessary.

Before publishing an APK, test on a phone: hold/release/cancel, finish/reset,
mute, leave the page during playback, background the app, rotate the device,
and check both photo themes. Host checks do not validate an Android build.
