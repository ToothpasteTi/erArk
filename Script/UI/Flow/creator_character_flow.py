import random
from functools import wraps
from typing import List
from types import FunctionType
from Script.Core import get_text, constant, game_type, cache_control, flow_handle, py_cmd

from Script.Design import (
    handle_panel,
    character,
    character_handle,
    cooking,
    map_handle,
    attr_calculation,
    basement,
)
from Script.UI.Moudle import panel, draw
from Script.UI.Panel import see_character_info_panel,assistant_panel
from Script.Config import normal_config, game_config

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """
width = normal_config.config_normal.text_width
""" 屏幕宽度 """
line_feed_draw = draw.NormalDraw()
""" 绘制换行对象 """
line_feed_draw.text = "\n"
line = draw.LineDraw("=", width)
""" 标题线绘制对象 """


@handle_panel.add_panel(constant.Panel.CREATOR_CHARACTER)
def creator_character_panel():
    """创建角色面板"""
    cache.character_data[0] = game_type.Character()
    character_handle.init_character_list()
    while 1:
        confirm_game_info_panel()
        if input_name_panel():
            character.init_attr(0)
            # game_start()
            cache.base_resouce = basement.get_base_zero()
            if confirm_character_attr_panel():
                game_start()
                break
        cache.character_data[0] = game_type.Character()
    cache.now_panel_id = constant.Panel.IN_SCENE


def game_start():
    """初始化游戏数据"""
    character_handle.init_character_dormitory()
    character_handle.init_character_position()
    character_handle.init_character_facility_open()
    # course.init_phase_course_hour()
    # interest.init_character_interest()
    # course.init_character_knowledge()
    # course.init_class_teacher()
    # course.init_class_time_table()
    # course.init_teacher_table()
    cooking.init_recipes()
    cooking.init_restaurant_data()
    character_position = cache.character_data[0].position
    map_handle.character_move_scene(["0","0"], character_position, 0)
    cache.school_longitude = random.uniform(120.9, 122.12)
    cache.school_latitude = random.uniform(30.7, 31.53)
    basement.get_base_updata()
    # print(f"debug 2facility_open = {cache.base_resouce.facility_open}")

def confirm_game_info_panel():
    """确认游戏说明面板"""
    now_line = draw.LineDraw("-", width)
    now_line.draw()
    info_text = f"\n\n  免责声明：1.本游戏仅为开发者本人自娱自乐及代码练习所用，开发它是因为我个人趣味低下，思想低俗所至致，无任何经济收益和利益驱动。\n\n\n            2.本游戏含有R18内容和浓重的era要素，包括且不限于软硬色情、性剥削、轻度SM、超自然等。\n\n\n            3.本游戏为完全纯爱，不含有任何NTR和R18G，且在设计理念和游戏内容上缝合了大量era与其他各类作品。\n\n\n            4.本游戏仅适合开发者本人游玩，不适合普通人游玩，特别是严厉禁止未成年人游玩，非开发者以外的任何人游玩该游戏出现的任何意外都和开发者本人无关。\n\n\n            5.本游戏禁止任何人在任何渠道对游戏本体或选取部分内容进行传播、交流、展示，公开和私底下都不行，禁止任何人用该游戏通过任何方式进行盈利。\n\n\n            6.虽然你大概率也不会听，但我个人建议看到这条信息的你现在关掉窗口并立刻删除该游戏。\n\n\n            7.总之只要不删我就默认你已经理解并遵守该声明，在不遵守的情况下出现的任何事故和法律责任都和开发者没有任何关系。\n\n\n"
    askfor_list = [_("我读完并理解了以上7条，我对自己负责，我不删，我要玩")]
    askfor_panel = panel.OneMessageAndSingleColumnButton()
    askfor_panel.set(askfor_list, info_text, 0)
    while 1:
        askfor_panel.draw()
        askfor_panel_return_list = askfor_panel.get_return_list()
        ask_list = []
        ask_list.extend(askfor_panel_return_list.keys())
        yrn = flow_handle.askfor_all(ask_list)
        py_cmd.clr_cmd()
        if yrn in askfor_panel_return_list:
            break

def confirm_character_attr_panel():
    """确认角色属性面板"""
    # now_attr_panel = see_character_info_panel.SeeCharacterInfoPanel(0, width)
    askfor_panel = panel.OneMessageAndSingleColumnButton()
    while 1:
        line_feed_draw.draw()
        now_attr_panel = Character_creat_Handle()
        now_attr_panel.draw()
        ask_list = []
        ask_list.extend(now_attr_panel.return_list)
        line_feed_draw.draw()
        now_line = draw.LineDraw("~", width)
        now_line.draw()
        askfor_list = [_("睁开双眼"), _("重新设定")]
        start_id = 0
        now_id_judge = 0
        now_id_list = []
        for now_id in ask_list:
            if now_id.isdigit():
                now_id_judge = 1
                now_id_list.append(int(now_id))
        if now_id_judge:
            start_id = max(now_id_list) + 1
        askfor_panel.set(askfor_list, _("这样可以吗?"), start_id)
        askfor_panel.draw()
        askfor_panel_return_list = askfor_panel.get_return_list()
        ask_list.extend(askfor_panel_return_list.keys())
        yrn = flow_handle.askfor_all(ask_list)
        py_cmd.clr_cmd()
        if yrn in askfor_panel_return_list:
            return askfor_panel_return_list[yrn] == askfor_list[0]


def input_name_panel() -> bool:
    """
    输入角色名面板
    Return arguments:
    bool -- 完成角色创建校验
    """
    character_data = cache.character_data[0]
    ask_name_panel = panel.AskForOneMessage()
    ask_name_panel.set(_("你能回忆起自己的名字吗？（默认称呼为博士，此处仅输入姓名即可）"), 10)
    line_feed_draw.draw()
    line.draw()
    not_num_error = draw.NormalDraw()
    not_num_error.text = _("角色名不能为纯数字，请重新输入\n")
    not_system_error = draw.NormalDraw()
    not_system_error.text = _("角色名不能为系统保留字，请重新输入\n")
    not_name_error = draw.NormalDraw()
    not_name_error.text = _("已有角色使用该姓名，请重新输入\n")
    create_judge = 0
    while 1:
        now_name = ask_name_panel.draw()
        if now_name.isdigit():
            not_num_error.draw()
            continue
        if now_name in get_text.translation_values or now_name in get_text.translation._catalog:
            not_system_error.draw()
            continue
        if now_name in cache.npc_name_data:
            not_name_error.draw()
            continue
        character_data.name = now_name
        character_data.nick_name = "博士"
        create_judge = 1

        break
    return create_judge


class Character_creat_Handle:
    """
    角色创建页面对象
    Keyword arguments:
    """

    def __init__(self):
        """初始化绘制对象"""
        self.width = normal_config.config_normal.text_width
        info_draw = see_character_info_panel.CharacterInfoHead(0, width)
        info_draw.draw_title = False
        sex_draw = Character_Sex(self.width)
        jj_draw = Character_JJ(self.width)
        debug_draw = Character_Debug(self.width)
        firstNpc_draw = Character_FirstNPC(self.width)
        bonus_draw = Character_Bonus(self.width)
        # abi_draw = see_character_info_panel.CharacterabiText(0, width)
        tal_draw = see_character_info_panel.CharacterTalentText(0, width, 8, 0)
        self.draw_list: List[draw.NormalDraw] = [
            info_draw,
            sex_draw,
            jj_draw,
            debug_draw,
            firstNpc_draw,
            bonus_draw,
            # abi_draw,
            tal_draw,
        ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        line_feed_draw.draw()
        title_draw = draw.TitleLineDraw(_("详细设定"), self.width)
        title_draw.draw()
        for label in self.draw_list:
            label.draw()
            if "return_list" in label.__dict__:
                self.return_list.extend(label.return_list)



class Character_Sex:
    """
    角色性别面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """

        character_data: game_type.Character = cache.character_data[0]
        sex_text = game_config.config_sex_tem[character_data.sex].name
        now_draw = panel.LeftDrawTextListPanel()

        sex_draw = draw.LeftDraw()
        sex_draw.width = 1
        sex_draw.text = f"\n 性别：{sex_text}      "
        now_draw.draw_list.append(sex_draw)
        now_draw.width += len(sex_draw.text)

        button_text = f"    【改变性别】"
        sex_button_draw = draw.LeftButton(
            _(button_text),
            _('改变性别'),
            self.width /10,
            cmd_func=self.change)
        self.return_list.append(sex_button_draw.return_text)

        now_draw.draw_list.append(sex_button_draw)
        now_draw.width += len(sex_button_draw.text)
        # now_draw.draw_list.append(line_feed_draw)

        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed_draw.draw()
            else:
                label.draw()

    def change(self):
        """性别改变"""
        character_data: game_type.Character = cache.character_data[0]
        if character_data.sex:
            character_data.sex = 0
        else:
            character_data.sex = 1


class Character_JJ:
    """
    角色阴茎面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """

        character_data: game_type.Character = cache.character_data[0]
        jj_text = game_config.config_jj_tem[character_data.pl_ability.jj_size].name
        now_draw = panel.LeftDrawTextListPanel()

        jj_draw = draw.LeftDraw()
        jj_draw.width = 1
        jj_draw.text = f"\n 阴茎大小：{jj_text}      "
        now_draw.draw_list.append(jj_draw)
        now_draw.width += len(jj_draw.text)

        button_text = f"    【改变大小】"
        jj_button_draw = draw.LeftButton(
            _(button_text),
            _('改变大小'),
            self.width / 10,
            cmd_func=self.change)
        self.return_list.append(jj_button_draw.return_text)

        now_draw.draw_list.append(jj_button_draw)
        now_draw.width += len(jj_button_draw.text)

        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        if cache.character_data[0].sex == 0:
            for label in self.draw_list:
                if isinstance(label, list):
                    for value in label:
                        value.draw()
                    line_feed_draw.draw()
                else:
                    label.draw()

    def change(self):
        """大小改变"""
        character_data: game_type.Character = cache.character_data[0]
        if character_data.pl_ability.jj_size == 3:
            character_data.pl_ability.jj_size = 0
        else:
            character_data.pl_ability.jj_size += 1



class Character_Debug:
    """
    Debug面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """

        now_draw = panel.LeftDrawTextListPanel()
        now_draw.draw_list.append(line_feed_draw)

        if cache.debug_mode:
            button_text = f"    【关闭debug模式】"
        else:
            button_text = f"    【开启debug模式】"
        button_draw = draw.LeftButton(
            _(button_text),
            _('debug'),
            self.width / 10,
            cmd_func=self.change)
        self.return_list.append(button_draw.return_text)

        now_draw.draw_list.append(button_draw)
        now_draw.width += len(button_draw.text)

        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        if cache.character_data[0].sex == 0:
            for label in self.draw_list:
                if isinstance(label, list):
                    for value in label:
                        value.draw()
                    line_feed_draw.draw()
                else:
                    label.draw()

    def change(self):
        """改变"""
        cache.debug_mode = not cache.debug_mode


class Character_FirstNPC:
    """
    角色初始干员面板
    Keyword arguments:
    width -- 最大宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        self.npc_select_now = 3
        """ 当前还可以选择的NPC数量 """

        now_draw = panel.LeftDrawTextListPanel()
        now_draw.draw_list.append(line_feed_draw)
        now_draw.draw_list.append(line_feed_draw)
        line = draw.LineDraw("↘", 1)
        now_draw.draw_list.append(line)

        info_draw = draw.LeftDraw()
        info_draw.width = 1
        info_draw.text = f" 当前初始干员有："
        info_draw.text += f"\n   基础:"
        for character_id in cache.npc_id_got:
            npc_character_data = cache.character_data[character_id]
            if npc_character_data.name in {"阿米娅","凯尔希","可露希尔","特蕾西娅","华法琳","温蒂","杜宾"}:
                info_draw.text += f" ●{npc_character_data.name}"
        info_draw.text += f"\n   自选:"
        for character_id in cache.npc_id_got:
            npc_character_data = cache.character_data[character_id]
            if npc_character_data.name not in {"阿米娅","凯尔希","可露希尔","特蕾西娅","华法琳","温蒂","杜宾"}:
                info_draw.text += f" ●{npc_character_data.name}"

        now_draw.draw_list.append(info_draw)
        now_draw.width += len(info_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        button_text = f"   【选择初期干员】"
        button_select_draw = draw.LeftButton(
            _(button_text),
            _('选择初期干员'),
            self.width,
            cmd_func=self.select_npc,
            )
        self.return_list.append(button_select_draw.return_text)
        now_draw.draw_list.append(button_select_draw)
        now_draw.width += len(button_select_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        info_last_draw = draw.LeftDraw()
        info_last_draw.width = 1
        if cache.debug_mode:
            self.npc_select_now = 999
        else:
            self.npc_select_now = 10 - len(cache.npc_id_got)
        if self.npc_select_now:
            info_last_draw.text = f" 当前剩余可选干员数量 = {self.npc_select_now}"
        else:
            info_last_draw.text = f" 已选择全部初始干员"
        now_draw.draw_list.append(info_last_draw)
        now_draw.width += len(info_last_draw.text)

        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed_draw.draw()
            else:
                label.draw()

    def select_npc(self):
        """选择初期干员"""

        self.handle_panel = panel.PageHandlePanel([], SelectFirstNPCButton, 999, 6, self.width, 1, 1, 0)

        while 1:

            # 显示当前助手
            line = draw.LineDraw("-", self.width)
            line.draw()
            now_npc_draw = draw.NormalDraw()
            if cache.debug_mode:
                self.npc_select_now = 999
            else:
                self.npc_select_now = 10 - len(cache.npc_id_got)
            now_npc_draw.text = f"\n 当前剩余可选干员数量 = {self.npc_select_now}\n"
            now_npc_draw.draw()
            line_feed_draw.draw()

            # 遍历所有NPC
            id_list = [i + 1 for i in range(len(cache.npc_tem_data))]
            # print("debug id_list = ",id_list)
            self.handle_panel.text_list = id_list
            self.handle_panel.update()
            self.handle_panel.draw()
            return_list = []
            return_list.extend(self.handle_panel.return_list)
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width)
            back_draw.draw()
            line_feed_draw.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                break


class SelectFirstNPCButton:
    """
    点击后可选择作为初期干员的NPC的按钮对象
    Keyword arguments:
    text -- 选项名字
    width -- 最大宽度
    is_button -- 绘制按钮
    num_button -- 绘制数字按钮
    button_id -- 数字按钮id
    """

    def __init__(
        self, NPC_id: int, width: int, is_button: bool, num_button: bool, button_id: int
    ):
        """初始化绘制对象"""

        self.NPC_id: int = NPC_id
        """ 干员角色编号 """
        self.draw_text: str = ""
        """ 绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """

        target_data: game_type.Character = cache.character_data[NPC_id]
        button_text = f"[{str(target_data.adv).rjust(4,'0')}]：{target_data.name}"
        name_draw = draw.LeftDraw()
        if self.NPC_id in cache.npc_id_got:
            if target_data.name in {"阿米娅","凯尔希","可露希尔","特蕾西娅","华法琳","温蒂","杜宾"}:
                button_text += f" (基础)"
                name_draw.text = button_text
                name_draw.width = self.width
                name_draw.style = "nowmap"
            else:
                button_text += f" (自选)"
                name_draw = draw.LeftButton(button_text, self.button_return, self.width,normal_style = "nowmap", cmd_func=self.button_0)
        else:
            name_draw = draw.LeftButton(button_text, self.button_return, self.width, cmd_func=self.button_0)

        # 按钮绘制
        # self.button_return = NPC_id
        self.draw_text = button_text

        """ 绘制的对象 """
        self.now_draw = name_draw

    def button_0(self):
        """选项1"""
        if self.NPC_id in cache.npc_id_got:
            cache.npc_id_got.remove(self.NPC_id)
        elif cache.debug_mode:
            cache.npc_id_got.add(self.NPC_id)
        elif 10 - len(cache.npc_id_got):
            cache.npc_id_got.add(self.NPC_id)

    def draw(self):
        """绘制对象"""
        self.now_draw.draw()


class Character_Bonus:
    """
    角色奖励点数面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        self.talent_id = 0
        """ 当前需要改变的素质 """

        character_data: game_type.Character = cache.character_data[0]
        bonus_all = 0
        now_draw = panel.LeftDrawTextListPanel()
        now_draw.draw_list.append(line_feed_draw)
        now_draw.draw_list.append(line_feed_draw)
        line = draw.LineDraw("↘", 1)
        now_draw.draw_list.append(line)

        info_draw = draw.LeftDraw()
        info_draw.width = 1
        info_draw.text = f" 当前为第 {str(cache.game_round)} 周目\n"
        info_draw.text += f" 当前总奖励点数 ="
        if cache.game_round == 1:
            bonus_all += 20
            info_draw.text += f" {bonus_all} (新玩家奖励+20)"
        if cache.debug_mode:
            bonus_all += 999
        self.bonus_now = bonus_all

        now_draw.draw_list.append(info_draw)
        now_draw.width += len(info_draw.text)

        info_talent_draw = draw.LeftDraw()
        info_talent_draw.width = 1
        info_talent_draw.text = f"\n 可选奖励有：\n"
        now_draw.draw_list.append(info_talent_draw)
        now_draw.width += len(info_talent_draw.text)

        talent_data_304 = game_config.config_talent[304]
        if character_data.talent[304]:
            button_text = f"   ●{talent_data_304.name}(10)：{talent_data_304.info}"
            self.bonus_now -= 10
            draw_style = "nowmap"
        else:
            button_text = f"   ○{talent_data_304.name}(10)：{talent_data_304.info}"
            draw_style = "standard"
        button_304_draw = draw.LeftButton(
            _(button_text),
            _(talent_data_304.name),
            self.width,
            normal_style = draw_style,
            cmd_func=self.get_talent,
            args=304)
        self.return_list.append(button_304_draw.return_text)
        now_draw.draw_list.append(button_304_draw)
        now_draw.width += len(button_304_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        talent_data_307 = game_config.config_talent[307]
        if character_data.talent[307]:
            button_text = f"   ●{talent_data_307.name}(10)：{talent_data_307.info}"
            self.bonus_now -= 10
            draw_style = "nowmap"
        else:
            button_text = f"   ○{talent_data_307.name}(10)：{talent_data_307.info}"
            draw_style = "standard"
        button_307_draw = draw.LeftButton(
            _(button_text),
            _(talent_data_307.name),
            self.width,
            normal_style = draw_style,
            cmd_func=self.get_talent,
            args=307)
        self.return_list.append(button_307_draw.return_text)
        now_draw.draw_list.append(button_307_draw)
        now_draw.width += len(button_307_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        if cache.base_resouce.money:
            button_text = f"   ●启动资金(5)：初始获得50000龙门币、6000合成玉和100粉色凭证"
            self.bonus_now -= 5
            draw_style = "nowmap"
        else:
            button_text = f"   ○启动资金(5)：初始获得50000龙门币和6000合成玉和100粉色凭证"
            draw_style = "standard"
        button_money_draw = draw.LeftButton(
            _(button_text),
            _('启动资金'),
            self.width,
            normal_style = draw_style,
            cmd_func=self.get_money,
            )
        self.return_list.append(button_money_draw.return_text)
        now_draw.draw_list.append(button_money_draw)
        now_draw.width += len(button_money_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        if character_data.assistant_character_id:
            target_data: game_type.Character = cache.character_data[character_data.assistant_character_id]
            button_text = f"   ●助理干员(5)：选择[{target_data.name}]成为助理干员，初始拥有1000点好感和50%信赖度"
            self.bonus_now -= 5
            draw_style = "nowmap"
        else:
            button_text = f"   ○助理干员(5)：选择一名干员成为助理干员，初始拥有1000点好感和50%信赖度"
            draw_style = "standard"
        button_assistant_draw = draw.LeftButton(
            _(button_text),
            _('助理干员'),
            self.width,
            normal_style = draw_style,
            cmd_func=self.get_assistant,
            )
        self.return_list.append(button_assistant_draw.return_text)
        now_draw.draw_list.append(button_assistant_draw)
        now_draw.width += len(button_assistant_draw.text)
        now_draw.draw_list.append(line_feed_draw)
        now_draw.width += 1

        info_last_draw = draw.LeftDraw()
        info_last_draw.width = 1
        if self.bonus_now:
            info_last_draw.text = f" 当前剩余奖励点数 = {self.bonus_now}\n"
        else:
            info_last_draw.text = f" 奖励点数消耗完毕\n"
        now_draw.draw_list.append(info_last_draw)
        now_draw.width += len(info_last_draw.text)

        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed_draw.draw()
            else:
                label.draw()

    def get_talent(self,talent_id:int):
        """获得素质"""
        character_data: game_type.Character = cache.character_data[0]
        if character_data.talent[talent_id]:
            character_data.talent[talent_id] = 0
        elif self.bonus_now >= 10:
            character_data.talent[talent_id] = 1
        else:
            info_last_draw = draw.WaitDraw()
            info_last_draw.width = 1
            info_last_draw.text = f"\n 当前剩余奖励不足\n"
            info_last_draw.draw()

    def get_money(self):
        """获得金钱"""
        if cache.base_resouce.money:
            cache.base_resouce.money = 0
            cache.base_resouce.orundum = 0
            cache.base_resouce.pink_certificate = 0
        elif self.bonus_now >= 5:
            cache.base_resouce.money = 50000
            cache.base_resouce.orundum = 6000
            cache.base_resouce.pink_certificate = 100
        else:
            info_last_draw = draw.WaitDraw()
            info_last_draw.width = 1
            info_last_draw.text = f"\n 当前剩余奖励不足\n"
            info_last_draw.draw()

    def get_assistant(self):
        """获得助理干员"""
        character_data: game_type.Character = cache.character_data[0]

        # 旧助理的好感信赖清零
        if character_data.assistant_character_id:
            target_data: game_type.Character = cache.character_data[character_data.assistant_character_id]
            target_data.favorability[0] = 0
            target_data.trust = 0
            character_data.assistant_character_id = 0
        
        # 这里直接沿用的助理页面的代码
        elif self.bonus_now >= 5:

            self.handle_panel = panel.PageHandlePanel([], assistant_panel.SeeNPCButtonList, 999, 8, self.width, 1, 1, 0)

            while 1:

                # 显示当前助手
                character_data: game_type.Character = cache.character_data[0]
                target_data: game_type.Character = cache.character_data[character_data.assistant_character_id]
                line = draw.LineDraw("-", self.width)
                line.draw()
                line_feed_draw.draw()
                now_npc_draw = draw.NormalDraw()
                if character_data.assistant_character_id != 0:
                    now_npc_text = f"当前助理为 {target_data.name} ，如果要更换，请在下面选择新的助理："
                else:
                    now_npc_text = f"当前无助理，请选择新的助理："
                now_npc_draw.text = now_npc_text
                now_npc_draw.draw()
                line_feed_draw.draw()
                line_feed_draw.draw()

                # 遍历所有NPC
                id_list = [i for i in cache.npc_id_got]
                # print("debug id_list = ",id_list)
                self.handle_panel.text_list = id_list
                self.handle_panel.update()
                self.handle_panel.draw()
                return_list = []
                return_list.extend(self.handle_panel.return_list)
                back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width)
                back_draw.draw()
                line_feed_draw.draw()
                return_list.append(back_draw.return_text)
                yrn = flow_handle.askfor_all(return_list)
                if yrn in return_list:
                    break

            # 在这里处理好感和信赖的增加
            target_data: game_type.Character = cache.character_data[character_data.assistant_character_id]
            target_data.favorability[0] = 1000
            target_data.trust = 50

        else:
            info_last_draw = draw.WaitDraw()
            info_last_draw.width = 1
            info_last_draw.text = f"\n 当前剩余奖励不足\n"
            info_last_draw.draw()

