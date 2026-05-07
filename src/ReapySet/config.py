
class MwConfig:
    """Main Window configs"""
    mw_title: str = "ReapySet"
    mw_collapse_time: int
    mw_y_offset: int
    mw_width: int = 700
    mw_height: int = 300
    mw_height_expansion: int = 280
    mw_expanded_height: int = mw_height + mw_height_expansion
    mw_expansion_time: int = 600
    mw_collapse_time: int = 450
    mw_y_offset: int = -150 #offsets var px to Y - is up + is down
    class Widget1:
        """Widget 1 config"""
        w1_height: int = 20
    class LangBtnWidget:
        """widget 2: central widget, the one with lang"""
        button_list: list[str] = ["Python", "Kotlin/Java", "C/C++", ".NET",
                                          "Ts/JavaScript", "GDscript", "Rust", "GO",
                                          "Lua"]

        enabled_btns: list[int] = [0]
        cw_height: int = 120
        max_btn_x_row: int = 5
