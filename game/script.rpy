# =====================================
# АВТО-ПОДГОНКА КАРТИНОК
# =====================================

init python:
    config.default_transform = Transform(
        xalign=0.5,
        yalign=0.5,
        xsize=config.screen_width,
        ysize=config.screen_height
    )

# =====================================
# ПЕРСОНАЖИ
# =====================================

define h = Character("Герой")
define m = Character("Мама")
define f = Character("Друг")

# =====================================
# ЭКРАН КОНЦОВКИ
# =====================================

screen end_menu():

    tag menu

    add Solid("#000")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        text "Конец" size 60

        textbutton "Start Game":
            action Start()

        textbutton "Load Game":
            action ShowMenu("load")

        textbutton "Quit":
            action Quit()

# =====================================
# НАЧАЛО
# =====================================

label start:

    play music "audio/calm_music.mp3" fadein 2.0

    # --- НОЧЬ ---
    scene room_night_1
    with fade
    h "Ещё один раз…"

    scene room_night_2
    with dissolve
    play sound "audio/click.mp3"
    h "Я почти отыгрался."

    scene room_night_3
    with dissolve
    play sound "audio/slot_spin.mp3"
    h "Сейчас точно повезёт…"

    # --- ПРОИГРЫШ ---
    scene loss_1
    with hpunch
    play sound "audio/lose.mp3"
    h "Нет…"

    scene loss_2
    with dissolve
    h "Да ладно…"

    # --- ТЕЛЕФОН ---
    scene phone_bank_1
    with fade
    play sound "audio/notification.mp3"
    h "Сообщение от банка…"

    scene phone_bank_2
    with dissolve
    h "Недостаточно средств…"

    # --- КУХНЯ ---
    scene kitchen_1
    with fade
    m "Ты опять не спал?"

    scene kitchen_2
    with dissolve
    h "Всё нормально."

    scene kitchen_3
    with dissolve
    m "Ты выглядишь уставшим."

    # --- ДРУГ ---
    scene friend_1
    with fade
    f "Ты снова играл?"

    scene friend_2
    with dissolve
    h "Я почти выиграл."

    scene friend_3
    with dissolve
    f "Ты так всегда говоришь."

    # --- УЛИЦА ---
    scene street
    with fade
    h "Они не понимают…"

    # --- У ДВЕРИ ---
    scene door_sit
    with dissolve
    h "Мне нужно ещё немного…"

    # --- КАЗИНО ---
    scene casino_1
    with fade
    play sound "audio/slot_spin.mp3"
    h "Вот он шанс."

    scene casino_2
    with dissolve
    h "Последние деньги…"

    # --- ВЫБОР ---
    scene casino_3
    with dissolve
    play sound "audio/click.mp3"
    h "Я должен решить…"

    menu:
        "Поставить всё":
            jump bad
        "Остановиться":
            jump good


# =====================================
# ❌ ПЛОХАЯ КОНЦОВКА
# =====================================

label bad:

    scene casino_4
    with hpunch
    play sound "audio/click.mp3"
    h "Давай…"

    scene bad_1
    with dissolve
    play sound "audio/slot_spin.mp3"
    h "Сейчас… сейчас…"

    scene bad_2
    with hpunch
    play sound "audio/lose.mp3"
    h "…нет."

    scene bad_3
    with fade
    h "Я всё потерял…"

    scene bad_4
    with dissolve
    h "Но я всё равно хочу ещё…"

    stop music fadeout 2.0
    "Плохая концовка."

    call screen end_menu
    return


# =====================================
# ✅ ХОРОШАЯ КОНЦОВКА
# =====================================

label good:

    scene good_1
    with fade
    h "Стоп…"

    scene good_2
    with dissolve
    f "Я рядом."
    h "..."

    scene good_3
    with dissolve
    h "Что я делаю?"

    scene good_4
    with fade
    h "Хватит."

    scene good_5
    with dissolve
    h "Я справлюсь."

    "Хорошая концовка."

    call screen end_menu
    return