import sys
the_label_txt: str = ("Lorem ipsum dolor sit amet, consectetur "
                      "adipiscing elit.\n Donec placerat tortor elit, quis "
                      "lacinia augue cursus sed.\n Nullam eu quam in libero "
                      "laoreet vulputate🏳️‍⚧️!?.").capitalize()


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
            font-style: italic; 
            font-weight: 100;
            font-size: 25pt;
            qproperty-alignment: AlignCenter; 
        }}
    """
#handles fallback fonts for every os