import datetime as dtime
import sys
import random
from typing import Any

from common.toml_handler import TomlHandler, GREETINGS_PATH, CONFIG_PATH






def get_label_stylesheet() -> str:
    if sys.platform == "darwin":  # macOS
        serif_fallback = "Georgia"
        emoji_font = "Apple Color Emoji"
    elif sys.platform == "win32":  # Windows
        serif_fallback = "Georgia"
        emoji_font = "Segoe UI Emoji"
    else:                           # Linux
        serif_fallback = "DejaVu Serif"
        emoji_font = "Noto Color Emoji"

    return f"""
        QLabel {{ 
            font-family: "Times New Roman", "{serif_fallback}", "{emoji_font}";
            letter-spacing: 1.5px; 
            font-weight: 100;
            font-size: 25pt;
            qproperty-alignment: AlignCenter; 
        }}
    """
#handles fallback fonts for every os



class GreetingsGetter:

    @staticmethod

    def _pick(p_value: Any) -> str | None:

        """

        Returns:

            - a random item if value is a list

            - the value itself if value is a string

            - None otherwise

        """

        if isinstance(p_value, str):

            return p_value

        if isinstance(p_value, list):

            return random.choice(p_value) if p_value else None

        return None

    @staticmethod

    def _get_hour(p_time_now: dtime.time) -> str:

        if dtime.time(5, 0) <= p_time_now < dtime.time(12, 0):

            return "morning"

        if dtime.time(12, 0) <= p_time_now < dtime.time(18, 0):

            return "afternoon"

        if dtime.time(18, 0) <= p_time_now < dtime.time(21, 0):

            return "evening"

        if dtime.time(21, 0) <= p_time_now or p_time_now < dtime.time(1, 0):

            return "night"

        return "late_night"

    @staticmethod
    def get_greeting() -> str:

        toml_file: dict[str, Any] = TomlHandler._toml_read(GREETINGS_PATH)

        name: str = TomlHandler.toml_get(CONFIG_PATH, "personal", "profile_name") or "User"

        lang: str = TomlHandler.toml_get(CONFIG_PATH, "personal", "language") or "en"
        is_greetings_enabled: bool = TomlHandler.toml_get(CONFIG_PATH, "personal", "enabled_greetings")
        if not is_greetings_enabled:
            print(is_greetings_enabled)
            return "\nReadySet\n"


        now: dtime.datetime = dtime.datetime.now()

        format_time: str = now.strftime("%d_%m")

        current_time: dtime.time = now.time()

        lang_data: dict[str, Any] = toml_file.get(lang, {})

        # 1) Holidays / anniversaries

        for section_name in ("holidays", "anniversaries"):

            section: dict[str, Any] = lang_data.get(section_name, {})

            for group in section.values():

                if format_time in group:

                    msg: str | None = GreetingsGetter._pick(group[format_time])

                    if msg:
                        return msg.format(name=name)
        # 2) weekdays
        WEEKDAYS = ( # noqa
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        )
        weekday: str = WEEKDAYS[now.weekday()]

        weekday_msgs: list[str] | str | None = (
            lang_data
            .get("weekdays", {})
            .get(weekday)
        )

        msg = GreetingsGetter._pick(weekday_msgs)

        if msg:
            return msg.format(name=name)
        # 3) Memes: 15% chance before normal greetings
        if random.random() < 0.15:

            memes: dict[str, list[str]] = lang_data.get("memes", {})

            if memes:

                category: str = random.choice(list(memes.keys())) # chooses a random category key put in a list

                msg: str | None = GreetingsGetter._pick(memes[category])

                if msg:
                    return msg.format(name=name)

        # 4) Normal greetings

        period: str = GreetingsGetter._get_hour(current_time)

        greetings: dict[str, Any] = lang_data.get("splashscreens", {}).get("topics", {}).get("greetings", {})

        msg: str | None = GreetingsGetter._pick(greetings.get(period))

        if msg:
            return msg.format(name=name)
        return (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit.\nDonec placerat tortor elit, quis "
            "lacinia augue cursus sed.\nNullam eu quam in libero "
            "laoreet vulputate🏳️‍⚧️!?."
        )






the_label_txt: str = GreetingsGetter.get_greeting()