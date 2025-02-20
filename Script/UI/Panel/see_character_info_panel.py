from distutils.command.config import config
from itertools import count
from Script.UI.Flow import creator_character_flow
from uuid import UUID
from typing import Tuple, List
from types import FunctionType
from Script.UI.Moudle import draw, panel
from Script.UI.Panel import see_clothing_info_panel, see_item_info_panel
from Script.Core import (
    cache_control,
    get_text,
    value_handle,
    game_type,
    text_handle,
    py_cmd,
    flow_handle,
    constant,
    rich_text,
)
from Script.Config import game_config, normal_config
from Script.Design import attr_text, map_handle, attr_calculation, handle_premise

panel_info_data = {}

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """

line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1
window_width = normal_config.config_normal.text_width
""" 屏幕宽度 """


class SeeCharacterInfoPanel:
    """
    用于查看角色属性的面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel: str = _("基础属性")
        """ 当前的属性页id """
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        main_first_draw = SeeCharacterFirstPanel(character_id, width)
        main_second_draw = SeeCharacterSecondPanel(character_id, width)
        main_third_draw = SeeCharacterThirdPanel(character_id, width)
        # see_daily_draw = SeeCharacterDailyPanel(character_id, width)
        # main_attr_draw = SeeCharacterMainAttrPanel(character_id, width)
        # see_status_draw = SeeCharacterStatusPanel(character_id, width, 5, 0)
        # see_clothing_draw = see_clothing_info_panel.SeeCharacterPutOnClothingListPanel(character_id, width)
        # see_item_draw = see_item_info_panel.SeeCharacterItemBagPanel(character_id, width)
        # see_knowledge_draw = SeeCharacterKnowledgePanel(character_id, width)
        # see_language_draw = SeeCharacterLanguagePanel(character_id, width)
        # see_nature_draw = SeeCharacterNaturePanel(character_id, width)
        # see_social_draw = SeeCharacterSocialContact(character_id, width)
        if character_id == 0:
            self.draw_data = {
                _("基础属性"): main_first_draw,
                _("能力、经验与宝珠"): main_second_draw,
                _("玩家能力"): main_third_draw,
                # _("属性（原）"): main_attr_draw,
                # _("状态"): see_status_draw,
                # _("服装"): see_clothing_draw,
                # _("道具"): see_item_draw,
                # _("技能"): see_knowledge_draw,
                # _("语言"): see_language_draw,
                # _("性格"): see_nature_draw,
                # _("社交"): see_social_draw,
            }
        else:
            self.draw_data = {
                _("基础属性"): main_first_draw,
                _("能力、经验与宝珠"): main_second_draw,
                # _("日程与喜好"): see_daily_draw,
                _("肉体情况"): main_third_draw,
                # _("属性（原）"): main_attr_draw,
                # _("状态"): see_status_draw,
                # _("服装"): see_clothing_draw,
                # _("道具"): see_item_draw,
                # _("技能"): see_knowledge_draw,
                # _("语言"): see_language_draw,
                # _("性格"): see_nature_draw,
                # _("社交"): see_social_draw,
            }
        """ 按钮文本对应属性面板 """
        self.handle_panel = panel.CenterDrawButtonListPanel()
        """ 属性列表的控制面板 """
        self.handle_panel.set(
            [f"[{text}]" for text in self.draw_data.keys()],
            list(self.draw_data.keys()),
            width,
            4,
            f"[{self.now_panel}]",
            self.change_panel,
        )

    def change_panel(self, panel_id: str):
        """
        切换当前面板
        Keyword arguments:
        panel_id -- 要切换的面板id
        """
        self.now_panel = panel_id
        self.handle_panel.set(
            [f"[{text}]" for text in self.draw_data.keys()],
            list(self.draw_data.keys()),
            self.width,
            4,
            f"[{self.now_panel}]",
            self.change_panel,
        )

    def draw(self):
        """绘制面板"""
        if self.now_panel == "玩家能力" and "玩家能力" not in self.draw_data:
            self.now_panel = "肉体情况"
        elif self.now_panel == "肉体情况" and "肉体情况" not in self.draw_data:
            self.now_panel = "玩家能力"
        self.draw_data[self.now_panel].draw()
        self.return_list = []
        self.return_list.extend(self.draw_data[self.now_panel].return_list)
        line_feed.draw()
        line = draw.LineDraw("=", self.width)
        line.draw()
        self.handle_panel.draw()
        self.return_list.extend(self.handle_panel.return_list)


class SeeCharacterFirstPanel:
    """
    显示角色属性面板第一页对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        image_draw = CharacterImage(character_id, width)
        Talent_draw = CharacterTalentText(character_id, width, 8, 0)
        self.draw_list: List[draw.NormalDraw] = [
            head_draw,
            image_draw,
            Talent_draw,
        ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()


class SeeCharacterSecondPanel:
    """
    显示角色属性面板第二页对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        abi_draw = CharacterabiText(character_id, width)
        experience_draw = CharacterExperienceText(character_id, width, 8, 0)
        juel_draw = CharacterJuelText(character_id, width, 8, 0)
        self.draw_list: List[draw.NormalDraw] = [
            head_draw,
            abi_draw,
            experience_draw,
            juel_draw,
        ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()


class SeeCharacterThirdPanel:
    """
    显示角色属性面板第三页对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        body_draw = CharacterBodyText(character_id, width, 8, 0)
        ability_draw = PlayerAbilityText(character_id, width, 8, 0)
        if character_id == 0:
            self.draw_list: List[draw.NormalDraw] = [
                head_draw,
                ability_draw,
            ]
        else:
            self.draw_list: List[draw.NormalDraw] = [
                head_draw,
                body_draw,
            ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()


class SeeCharacterDailyPanel:
    """
    显示角色属性面板中的日程与喜好面板
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        daily_draw = CharacterInfoHead(character_id, width)
        preference_draw = CharacterInfoHead(character_id, width)
        self.draw_list: List[draw.NormalDraw] = [
            head_draw,
            daily_draw,
        ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()


class SeeCharacterMainAttrPanel:
    """
    显示角色主属性面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        # stature_draw = CharacterStatureText(character_id, width)
        room_draw = CharacterRoomText(character_id, width)
        birthday_draw = CharacterBirthdayText(character_id, width)
        # sture_info_draw = CharacterStatureInfoText(character_id, width)
        # measurement_draw = CharacterMeasurementsText(character_id, width)
        # sex_experience_draw = CharacterSexExperienceText(character_id, width)
        self.draw_list: List[draw.NormalDraw] = [
            head_draw,
            # stature_draw,
            room_draw,
            birthday_draw,
            # sture_info_draw,
            # measurement_draw,
            # sex_experience_draw,
        ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()


class SeeCharacterStatusPanel:
    """
    显示角色状态面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, type_number: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        self.type_number = type_number
        """ 显示的状态类型 """
        character_data = cache.character_data[character_id]
        # print("game_config.config_character_state_type :",game_config.config_character_state_type)
        # print("game_config.config_character_state_type_data :",game_config.config_character_state_type_data)
        for status_type in game_config.config_character_state_type_data:
            if status_type == type_number:
                type_data = game_config.config_character_state_type[status_type]
                type_line = draw.LittleTitleLineDraw(type_data.name, width, ":")
                # print("type_data.name :",type_data.name)
                self.draw_list.append(type_line)
                type_set = game_config.config_character_state_type_data[status_type]
                status_text_list = []
                for status_id in type_set:
                    # print("status_type :",status_type)
                    # print("status_id :",status_id)
                    # print("game_config.config_character_state[status_id] :",game_config.config_character_state[status_id])
                    # print("game_config.config_character_state[status_id].name :",game_config.config_character_state[status_id].name)
                    if status_type == 0:
                        if character_data.sex == 0:
                            if status_id in {2, 4, 7}:
                                continue
                        elif character_data.sex == 1:
                            if status_id == 3:
                                continue
                    status_text = game_config.config_character_state[status_id].name
                    status_value = 0
                    if status_id in character_data.status_data:
                        status_value = character_data.status_data[status_id]
                    # if status_id in character_data.status:
                    #     status_value = character_data.status[status_id]
                    status_value = round(status_value)
                    # status_value = int(attr_text.get_value_text(status_value))
                    status_level = attr_calculation.get_status_level(status_value)
                    now_text = f"  {status_text}:lv{status_level} {status_value}"
                    # print("status_value :",status_value)
                    status_text_list.append(now_text)
                    # print("status_text_list :",status_text_list)
                if self.center_status:
                    now_draw = panel.CenterDrawTextListPanel()
                else:
                    now_draw = panel.LeftDrawTextListPanel()
                now_draw.set(status_text_list, self.width, self.column)
                self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        # title_draw = draw.TitleLineDraw(_("人物状态"), self.width)
        # title_draw.draw()
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class SeeCharacterClothPanel:
    """
    显示角色服装面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, type_number: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        self.type_number = type_number
        """ 显示的状态类型 """
        character_data = cache.character_data[0]
        target_character_data = cache.character_data[character_data.target_character_id]

        type_line = draw.LittleTitleLineDraw("服装", width, ":")
        self.draw_list.append(type_line)

        # cloth_text_list = []
        now_text = ""
        # 遍历全部衣服类型
        for clothing_type in game_config.config_clothing_type:
            type_name = game_config.config_clothing_type[clothing_type].name
            # 当该类型里有衣服存在的时候才显示
            if len(target_character_data.cloth.cloth_wear[clothing_type]):
                # 正常情况下不显示胸部和内裤的服装,debug或该部位可以显示则显示
                if clothing_type in {6, 9} and not cache.debug_mode:
                    # print(f"debug {target_character_data.name}.cloth_see[clothing_type] = {target_character_data.cloth_see[clothing_type]}")
                    # 如果有内衣透视素质，则自动变为显示
                    if (
                            character_data.talent[307]
                            or len(target_character_data.cloth.cloth_wear[clothing_type - 1]) == 0
                    ):
                        target_character_data.cloth.cloth_see[clothing_type] = True
                    else:
                        target_character_data.cloth.cloth_see[clothing_type] = False
                    # 如果不显示，则不显示（废话
                    if not target_character_data.cloth.cloth_see[clothing_type]:
                        continue
                # 当显示到下衣8的时候，换行
                if clothing_type == 8 and now_text != "":
                    now_text += "\n"
                now_text += f"  [{type_name}]:"
                # 如果有多个衣服，则依次显示
                for cloth_id in target_character_data.cloth.cloth_wear[clothing_type]:
                    cloth_name = game_config.config_clothing_tem[cloth_id].name
                    now_text += f" {cloth_name}"
                    # 如果该部位有精液，则显示精液信息
                    if target_character_data.dirty.cloth_semen[clothing_type][1] != 0:
                        now_text += f"<semen>(精液)</semen>"
            # 当显示到下衣8的时候，换行
            if clothing_type == 8 and len(target_character_data.cloth.cloth_wear[8]) == 0:
                now_text += "\n"
            # 真空的胸衣和内裤单独显示
            if clothing_type in {6, 9} and not len(target_character_data.cloth.cloth_wear[clothing_type]):
                if not cache.debug_mode:
                    # print(f"debug {target_character_data.name}.cloth.cloth_see[clothing_type] = {target_character_data.cloth.cloth_see[clothing_type]}")
                    if not target_character_data.cloth.cloth_see[clothing_type]:
                        continue
                now_text += f"  [{type_name}]: 真空"
        now_text += "\n"
        # cloth_text_list.append(now_text)

        no_cloth_flag = True
        for clothing_type in game_config.config_clothing_type:
            if len(target_character_data.cloth.cloth_wear[clothing_type]):
                no_cloth_flag = False
                break
        if no_cloth_flag:
            now_text = "  全裸\n"
            # cloth_text_list.append(now_text)

        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()

        # 富文本模组
        now_style_list = rich_text.get_rich_text_print(now_text, "standard")
        new_x_list = rich_text.remove_rich_cache(now_text)
        # test_flag = False
        # if 'emoji' in now_style_list:
        #     test_flag = True
        #     print(f"debug 总：now_style_list = {now_style_list}")
        #     print(f"debug 总：new_x_list = {new_x_list}")
        while 1:
            if not len(new_x_list):
                break
            # now_rich_draw = game_type.MapDrawText()
            now_rich_draw = draw.NormalDraw()
            now_rich_draw.text = new_x_list[0]
            now_rich_draw.style = now_style_list[0]
            now_style_list = now_style_list[1:]
            new_x_list = new_x_list[1:]
            # if test_flag:
            #     print(f"debug now_rich_draw.style = {now_rich_draw.style}")
            while 1:
                if not len(new_x_list):
                    break
                if now_style_list[0] != now_rich_draw.style:
                    break
                now_rich_draw.text += new_x_list[0]
                now_style_list = now_style_list[1:]
                new_x_list = new_x_list[1:]
                # if test_flag:
                #     print(f"debug 分：now_rich_draw.text = {now_rich_draw.text}")
                #     print(f"debug 分：now_style_list = {now_style_list}")
                #     print(f"debug 分：new_x_list = {new_x_list}")
            now_draw.draw_list.append(now_rich_draw)
            now_draw.width += len(now_rich_draw.text)

        # now_draw.set(cloth_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class SeeCharacterHStatePanel:
    """
    显示角色H状态面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, type_number: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        self.type_number = type_number
        """ 显示的状态类型 """
        character_data = cache.character_data[0]
        target_character_data = cache.character_data[character_data.target_character_id]
        # print("game_config.config_character_state_type :",game_config.config_character_state_type)
        # print("game_config.config_character_state_type_data :",game_config.config_character_state_type_data)

        type_line = draw.LittleTitleLineDraw("H状态", width, ":")
        # print("type_data.name :",type_data.name)
        self.draw_list.append(type_line)

        status_text_list = []
        bondage_text_list = ["未捆绑", "后高手缚", "直立缚", "驷马捆绑", "直臂缚", "双手缚", "菱绳缚", "龟甲缚", "团缚",
                             "逆团缚", "吊缚", "后手吊缚", "单足吊缚", "后手观音", "苏秦背剑", "五花大绑"]
        enemas_text_list = ["脏污", "灌肠中", "已灌肠", "精液灌肠中", "已精液灌肠"]
        insert_text_list = ["发交中", "阴茎蹭脸中", "口交中", "乳交中", "腋交中", "手交中", "抽插阴道中", "抽插子宫中",
                            "抽插后穴中", "抽插尿道中", "腿交中", "足交中", "尾交中", "阴茎蹭角中", "阴茎蹭耳朵中"]
        body_item_set = target_character_data.h_state.body_item

        # 指令文本
        now_text = ""
        insert_index = target_character_data.h_state.insert_position
        if insert_index == -1:
            now_text += f""
        else:
            now_text += f"   <{insert_text_list[insert_index]}>"
        status_text_list.append(now_text)

        # 道具文本
        for i in range(10):
            # print("status_type :",status_type)
            if body_item_set[i][1]:
                status_text = body_item_set[i][0]

                now_text = f"   <{status_text}>"
                status_text_list.append(now_text)
            # print("status_text_list :",status_text_list)

        # 绳子文本
        if target_character_data.h_state.bondage:
            now_text = f"   <{bondage_text_list[target_character_data.h_state.bondage]}>"
            status_text_list.append(now_text)

        # 灌肠文本
        if target_character_data.dirty.a_clean:
            now_text = f"   <{enemas_text_list[target_character_data.dirty.a_clean]}>"
            status_text_list.append(now_text)

        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(status_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class CharacterInfoHead:
    """
    角色信息面板头部面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.draw_title: bool = True
        """ 是否绘制面板标题 """
        character_data: game_type.Character = cache.character_data[character_id]
        sex_text = game_config.config_sex_tem[character_data.sex].name

        # 非清醒时输出当前状态
        sleep_text_list = [" <清醒>", " <疲劳>", " <昏昏欲睡>", " <随时睡着>"]
        sleep_text = sleep_text_list[attr_calculation.get_sleep_level(character_data.sleep_point)]
        status_text = game_config.config_status[character_data.state].name

        # if character_id != 0:
        #     print("debug character_id = ",character_id,"    character_data.sleep_point = ",character_data.sleep_point,"   sleep_text = ",sleep_text)
        sleep_text = "" if sleep_text == " <清醒>" else sleep_text
        sleep_text = " <睡眠中>" if status_text == "睡觉" else sleep_text

        # 非普通时输出当前心情
        angry_text = attr_calculation.get_angry_text(character_data.angry_point)
        angry_text = "" if angry_text == "普通" else angry_text

        # 有尿意时进行提示
        urinate_text = " <尿>" if character_data.urinate_point >= 192 else ""

        # 饥饿时进行提示
        hunger_text = " <饿>" if character_data.hunger_point >= 192 else ""
        start_time = character_data.behavior.start_time
        hunger_text = hunger_text if start_time in {6, 7, 8, 11, 12, 13, 16, 17, 18} else ""

        if character_id:
            message = _(
                "{character_name}（好感度： {favorability}，信赖度： {trust}% {angry}）{sleep}{urinate}{hunger}").format(
                character_name=character_data.name,
                favorability=int(character_data.favorability[0]),
                trust=round(character_data.trust, 1),
                angry=angry_text,
                sleep=sleep_text,
                urinate=urinate_text,
                hunger=hunger_text,
            )
        else:
            message = _(
                "{character_name}{character_nick_name}{sleep}{urinate}"
            ).format(
                # character_id=character_id,
                character_name=character_data.name,
                character_nick_name=character_data.nick_name,
                # sex_text=sex_text,
                sleep=sleep_text,
                urinate=urinate_text,
            )
        message_draw = draw.CenterDraw()
        message_draw.width = width / 3
        message_draw.text = message
        hp_draw = draw.InfoBarDraw()
        hp_draw.width = width / 6
        hp_draw.scale = 0.8
        hp_draw.set(
            "HitPointbar",
            int(character_data.hit_point_max),
            int(character_data.hit_point),
            _("体力"),
        )
        mp_draw = draw.InfoBarDraw()
        mp_draw.width = width / 6
        mp_draw.scale = 0.8
        mp_draw.set(
            "ManaPointbar",
            int(character_data.mana_point_max),
            int(character_data.mana_point),
            _("气力"),
        )
        if character_id == 0:
            ep_draw = draw.InfoBarDraw()
            ep_draw.width = width / 6
            ep_draw.scale = 0.8
            ep_draw.set(
                "EjaPointbar",
                int(character_data.eja_point_max),
                int(character_data.eja_point),
                _("射精"),
            )
        # status_text = game_config.config_status[character_data.state].name
        # status_draw = draw.CenterDraw()
        # status_draw.width = width / 4
        # status_draw.text = _(" ").format(status_text=status_text)
        None_draw = draw.CenterDraw()
        None_draw.width = 1
        None_draw.text = (" ")
        if character_id == 0:
            self.draw_list: List[Tuple[draw.NormalDraw, draw.NormalDraw]] = [
                (message_draw, hp_draw, None_draw, mp_draw, ep_draw),
                # (status_draw),
            ]
        else:
            self.draw_list: List[Tuple[draw.NormalDraw, draw.NormalDraw]] = [
                (message_draw, hp_draw, None_draw, mp_draw),
                # (status_draw),
            ]
        """ 要绘制的面板列表 """

    def draw(self):
        """绘制面板"""
        if self.draw_title:
            title_draw = draw.TitleLineDraw(_("人物属性"), self.width)
            title_draw.draw()
        for draw_tuple in self.draw_list:
            for label in draw_tuple:
                label.draw()
            line_feed.draw()


class CharacterWearClothingList:
    """
    角色已穿戴服装列表
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    column -- 每行服装最大个数
    """

    def __init__(self, character_id: int, width: int, column: int):
        """初始化绘制对象"""
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.width: int = width
        """ 当前最大可绘制宽度 """
        self.column: int = column
        """ 每行服装最大个数 """
        character_data: game_type.Character = cache.character_data[character_id]
        describe_list = [_("可爱的"), _("性感的"), _("帅气的"), _("清新的"), _("典雅的"), _("清洁的"), _("保暖的")]
        clothing_info_list = []
        title_draw = draw.LittleTitleLineDraw(_("衣着"), width, ":")
        self.draw_list = [title_draw]
        """ 绘制的对象列表 """
        for clothing_type in game_config.config_clothing_type:
            if clothing_type in character_data.put_on and isinstance(
                    character_data.put_on[clothing_type], UUID
            ):
                now_id = character_data.put_on[clothing_type]
                now_clothing: game_type.Clothing = character_data.clothing[clothing_type][now_id]
                value_list = [
                    now_clothing.sweet,
                    now_clothing.sexy,
                    now_clothing.handsome,
                    now_clothing.fresh,
                    now_clothing.elegant,
                    now_clothing.cleanliness,
                    now_clothing.warm,
                ]
                describe_id = value_list.index(max(value_list))
                describe = describe_list[describe_id]
                now_clothing_config = game_config.config_clothing_tem[now_clothing.tem_id]
                clothing_name = f"[{now_clothing.evaluation}{describe}{now_clothing_config.name}]"
                clothing_info_list.append(clothing_name)
        now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(clothing_info_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制对象"""
        for draw_list in self.draw_list:
            for now_draw in draw_list:
                now_draw.draw()
            line_feed.draw()


class CharacterStatureText:
    """
    身材描述信息面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        player_data = cache.character_data[0]
        description = attr_text.get_stature_text(character_id)
        description = description.format(
            Name=player_data.name,
            NickName=player_data.nick_name,
        )
        self.description = description
        """ 身材描述文本 """

    def draw(self):
        """绘制面板"""
        line = draw.LineDraw(":", self.width)
        line.draw()
        info_draw = draw.CenterDraw()
        info_draw.text = self.description
        info_draw.width = self.width
        info_draw.draw()
        line_feed.draw()


class CharacterRoomText:
    """
    角色宿舍/教室和办公室地址显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        character_data: game_type.Character = cache.character_data[self.character_id]
        dormitory = character_data.dormitory
        dormitory_text = ""
        if dormitory == "":
            dormitory_text = _("暂无")
        else:
            dormitory_path = map_handle.get_map_system_path_for_str(dormitory)
            dormitory_text = attr_text.get_scene_path_text(dormitory_path)
        self.dormitory_text = _("宿舍位置:") + dormitory_text
        """ 宿舍位置文本 """
        # classroom = character_data.classroom
        # now_classroom_text = _("教室位置:")
        # if classroom != "":
        #     classroom_path = map_handle.get_map_system_path_for_str(classroom)
        #     classroom_text = attr_text.get_scene_path_text(classroom_path)
        #     now_classroom_text += classroom_text
        # else:
        #     now_classroom_text += _("暂无")
        # self.classroom_text = now_classroom_text
        # """ 教室位置文本 """
        officeroom = character_data.officeroom
        now_officeroom_text = _("办公室位置:")
        if len(officeroom):
            officeroom_text = attr_text.get_scene_path_text(officeroom)
            now_officeroom_text += officeroom_text
        else:
            now_officeroom_text += _("暂无")
        self.officeroom_text = now_officeroom_text
        """ 办公室位置文本 """

    def draw(self):
        """绘制面板"""
        line = draw.LineDraw(".", self.width)
        line.draw()
        info_draw = panel.CenterDrawTextListPanel()
        # info_draw.set([self.dormitory_text, self.classroom_text, self.officeroom_text], self.width, 3)
        info_draw.draw()


class CharacterBirthdayText:
    """
    角色年龄/生日信息显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        character_data = cache.character_data[self.character_id]
        # age_text = _("年龄:{character_age}岁").format(character_age=character_data.age)
        birthday_text = _("生日:{birthday_month}月{birthday_day}日").format(
            birthday_month=character_data.birthday.month, birthday_day=character_data.birthday.day
        )
        # self.info_list = [age_text, birthday_text]
        self.info_list = [birthday_text]
        """ 绘制的文本列表 """

    def draw(self):
        """绘制面板"""
        line = draw.LineDraw(".", self.width)
        line.draw()
        info_draw = panel.CenterDrawTextListPanel()
        info_draw.set(self.info_list, self.width, 2)
        info_draw.draw()


class CharacterStatureInfoText:
    """
    角色身高体重罩杯信息显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        character_data: game_type.Character = cache.character_data[self.character_id]
        now_height = str(round(character_data.height.now_height, 2))
        now_height_text = _("身高:") + now_height + "cm"
        now_weight = str(round(character_data.weight, 2))
        now_weight_text = _("体重:") + now_weight + "kg"
        now_chest_tem_id = attr_calculation.judge_chest_group(character_data.chest.now_chest)
        now_chest_tem = game_config.config_chest[now_chest_tem_id]
        body_fat = str(round(character_data.bodyfat, 2))
        body_fat_text = _("体脂率:") + body_fat + "%"
        now_chest_text = _("罩杯:") + now_chest_tem.info
        self.info_list = [now_height_text, now_weight_text, now_chest_text, body_fat_text]
        """ 绘制的文本列表 """

    def draw(self):
        """绘制面板"""
        line = draw.LineDraw(".", self.width)
        line.draw()
        info_draw = panel.CenterDrawTextListPanel()
        info_draw.set(self.info_list, self.width, 4)
        info_draw.draw()


class CharacterMeasurementsText:
    """
    角色三围信息显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        character_data = cache.character_data[self.character_id]
        character_data.measurements.bust
        character_data.measurements.hip
        character_data.measurements.waist
        now_bust = str(round(character_data.measurements.bust, 2))
        now_hip = str(round(character_data.measurements.hip, 2))
        now_waist = str(round(character_data.measurements.waist, 2))
        now_bust_text = _("胸围:") + now_bust + "cm"
        now_waist_text = _("腰围:") + now_waist + "cm"
        now_hip_text = _("臀围") + now_hip + "cm"
        self.info_list = [now_bust_text, now_waist_text, now_hip_text]
        """ 绘制的文本列表 """

    def draw(self):
        """绘制面板"""
        line = draw.LineDraw(".", self.width)
        line.draw()
        info_draw = panel.CenterDrawTextListPanel()
        info_draw.set(self.info_list, self.width, 3)
        info_draw.draw()


class CharacterSexExperienceText:
    """
    角色性经验信息面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        character_data = cache.character_data[self.character_id]
        self.experience_text_data = {
            0: _("Ｎ感觉:"),
            1: _("Ｂ感觉:"),
            2: _("Ｃ感觉:"),
            3: _("Ｐ感觉:"),
            4: _("Ｖ感觉:"),
            5: _("Ａ感觉:"),
            6: _("Ｕ感觉:"),
            7: _("Ｗ感觉:"),
        }
        """ 性器官开发度描述 """
        self.draw_list: List[draw.NormalDraw()] = []
        """ 绘制对象列表 """
        sex_tem = character_data.sex in (0, 3)
        organ_list = game_config.config_organ_data[sex_tem] | game_config.config_organ_data[2]
        for organ in organ_list:
            if organ != 8:
                now_draw = draw.NormalDraw()
                now_draw_1 = draw.NormalDraw()
                now_draw_2 = draw.NormalDraw()
                now_draw_value = draw.NormalDraw()
                now_draw.text = self.experience_text_data[organ]
                now_draw_1.text = " "
                now_draw_2.text = "  "
                now_draw.width = width / len(organ_list)
                now_exp = 0
                if organ in character_data.sex_experience:
                    now_exp = character_data.sex_experience[organ]
                now_draw_value.text = str(now_exp)
                level_draw = draw.ExpLevelDraw(now_exp)
                new_draw = draw.CenterMergeDraw(width / len(organ_list))
                # print("width :",width)
                # print("len(organ_list) :",len(organ_list))
                new_draw.draw_list.append(now_draw)
                new_draw.draw_list.append(now_draw_1)
                new_draw.draw_list.append(level_draw)
                new_draw.draw_list.append(now_draw_2)
                new_draw.draw_list.append(now_draw_value)
                self.draw_list.append(new_draw)

    def draw(self):
        """绘制对象"""
        line = draw.LineDraw(".", self.width)
        line.draw()
        for value in self.draw_list:
            value.draw()


class CharacterabiText:
    """
    角色能力面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        self.type = type
        """ 当前绘制类型 """
        # self.column = column
        # """ 每行状态最大个数 """
        character_data = cache.character_data[self.character_id]
        """ 角色数据 """
        self.draw_list: List[draw.NormalDraw()] = []
        """ 绘制对象列表 """
        self.title_list: List[draw.NormalDraw()] = []
        """ 绘制标题列表 """
        ability_list = game_config.config_ability_type_data
        title_text = "能力"
        type_line = draw.LittleTitleLineDraw(title_text, width, ":")
        self.draw_list.append(type_line)
        # 进入能力大类#
        for anility_type in ability_list:
            # if anility_type == type:
            type_set = ability_list[anility_type]
            # 去掉玩家的若干能力#
            if self.character_id == 0:
                if anility_type in {0, 1, 2, 6}:
                    continue
            for ability_id in type_set:
                # 去掉与性别不符的能力#
                if character_data.sex == 0:
                    if ability_id in {2, 4, 7, 9, 12, 33, 34, 39}:
                        continue
                elif character_data.sex == 1:
                    if ability_id == 3:
                        continue
                now_draw = draw.NormalDraw()
                now_draw_value = draw.NormalDraw()
                now_draw.text = game_config.config_ability[ability_id].name
                # 这个_1是为了补空格让格式对齐#
                now_draw_1 = draw.NormalDraw()
                now_draw_1.text = " "
                now_draw_1.width = 1
                now_draw.width = width / len(type_set)
                now_exp = 0
                now_exp = character_data.ability[ability_id]
                now_draw_value.text = str(now_exp)
                level_draw = draw.ExpLevelDraw(now_exp)
                new_draw = draw.LeftMergeDraw(width / 10)
                new_draw.draw_list.append(now_draw_1)
                new_draw.draw_list.append(now_draw)
                new_draw.draw_list.append(now_draw_1)
                # 根据不同的类型补不同数量的空格#
                if anility_type != 2 and anility_type != 4 and anility_type != 6:
                    new_draw.draw_list.append(now_draw_1)
                    new_draw.draw_list.append(now_draw_1)
                    if anility_type == 3 or anility_type == 5:
                        new_draw.draw_list.append(now_draw_1)
                        new_draw.draw_list.append(now_draw_1)
                new_draw.draw_list.append(level_draw)
                new_draw.draw_list.append(now_draw_1)
                new_draw.draw_list.append(now_draw_value)
                self.draw_list.append(new_draw)
            # 只有不是最后一个类型就补个换行#
            if anility_type != 6:
                new_draw_n = draw.NormalDraw()
                new_draw_n.text = "\n"
                new_draw_n.width = 1
                self.draw_list.append(new_draw_n)

    def draw(self):
        """绘制对象"""
        line_feed.draw()
        for value in self.draw_list:
            value.draw()


class Characterabi_show_Text:
    """
    角色能力升级显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        # self.column = column
        # """ 每行状态最大个数 """
        self.character_data = cache.character_data[self.character_id]
        """ 角色数据 """

    def draw(self):
        """绘制对象"""
        self.return_list = []
        # 绘制标题#
        line_feed.draw()
        title_text = "能力"
        type_line = draw.LittleTitleLineDraw(title_text, self.width, ":")
        type_line.draw()
        ability_list = game_config.config_ability_type_data
        for anility_type in ability_list:
            type_set = ability_list[anility_type]
            # 去掉刻印
            # print("anility_type : ",anility_type)
            if anility_type == 2:
                continue
            for ability_id in type_set:
                # 去掉与性别不符的感度与扩张
                if self.character_data.sex == 0:
                    if ability_id in {2, 4, 7, 9, 12, 34, 39}:
                        continue
                elif self.character_data.sex == 1:
                    if ability_id == 3:
                        continue
                # 这个_1是为了补空格让格式对齐#
                now_exp = 0
                now_exp = self.character_data.ability[ability_id]
                button_text = " "
                button_text += game_config.config_ability[ability_id].name
                button_text += " "
                # 根据不同的类型补不同数量的空格#
                if anility_type != 2 and anility_type != 4 and anility_type != 6:
                    button_text += "  "
                    if anility_type == 3 or anility_type == 5:
                        button_text += "  "
                button_text += attr_calculation.judge_grade(now_exp)
                button_text += " "
                button_text += str(now_exp)
                now_abi_up_panel = Characterabi_cmd_Text(self.character_id, self.width, ability_id)
                button_draw = draw.LeftButton(
                    _(button_text),
                    _(game_config.config_ability[ability_id].name),
                    self.width / 10,
                    cmd_func=now_abi_up_panel.draw)
                self.return_list.append(button_draw.return_text)
                button_draw.draw()
                # py_cmd.clr_cmd()
                # if yrn == self.back_draw.return_text:
                #     break
            # 只有不是最后一个类型就补个换行#
            if anility_type != 6:
                new_draw_n = draw.NormalDraw()
                new_draw_n.text = "\n"
                new_draw_n.width = 1
                new_draw_n.draw()
        # yrn = flow_handle.askfor_all(self.return_list)


class Characterabi_cmd_Text:
    """
    角色能力升级指令面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int, ability_id: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        self.ability_id = ability_id
        """ 当前的能力id """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        self.character_data = cache.character_data[self.character_id]
        """ 角色数据 """
        self.ability_level = self.character_data.ability[ability_id]
        """ 能力等级 """

    def draw(self):
        """绘制对象"""
        self.return_list = []
        self.jule_dict = {}
        judge = 1
        # 绘制标题#
        while 1:

            # 读取该能力在对应等级下的升级需求
            need_list = game_config.config_ability_up_data[self.ability_id][self.ability_level]
            line = draw.LineDraw(".", self.width)
            line.draw()
            line_feed.draw()

            # 遍历升级需求，并输出信息
            for need_text in need_list:
                # print(f"debug need_text = {need_text}")
                need_type = need_text.split('|')[0][0]
                need_type_id = int(need_text.split('|')[0][1:])
                need_value = int(need_text.split('|')[1])
                if need_type == "A":
                    abi_name = game_config.config_ability[need_type_id].name
                    button_text = "需要能力 : " + abi_name + " 至少为" + str(need_value) + "\n"
                    if self.character_data.ability[need_type_id] < need_value:
                        judge = 0
                elif need_type == "J":
                    juel_name = game_config.config_juel[need_type_id].name
                    button_text = "需要宝珠 : " + juel_name + " 至少为" + str(need_value) + "\n"
                    if self.character_data.juel[need_type_id] < need_value:
                        judge = 0
                    self.jule_dict[need_type_id] = need_value
                elif need_type == "E":
                    experience_name = game_config.config_experience[need_type_id].name
                    button_text = "需要经验 : " + experience_name + " 至少为" + str(need_value) + "\n"
                    if self.character_data.experience[need_type_id] < need_value:
                        judge = 0
                now_draw = draw.NormalDraw()
                now_draw.text = button_text
                now_draw.draw()

            # 判断是否可以升级
            if judge:
                now_draw_succed = draw.NormalDraw()
                now_draw_succed.text = "满足条件，要升级吗？\n"
                now_draw_succed.draw()
            else:
                now_draw_failed = draw.NormalDraw()
                now_draw_failed.text = "不满足条件，无法升级\n"
                now_draw_failed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width / 3)
            back_draw.draw()
            self.return_list.append(back_draw.return_text)
            if judge:
                yes_draw = draw.CenterButton(_("[确定]"), _("确定"), self.width / 3, cmd_func=self.level_up)
                yes_draw.draw()
                self.return_list.append(yes_draw.return_text)
            yrn = flow_handle.askfor_all(self.return_list)
            py_cmd.clr_cmd()
            line_feed.draw()
            if yrn == back_draw.return_text:
                break

    def level_up(self):
        for need_type_id in self.jule_dict:
            cache.character_data[self.character_id].juel[need_type_id] -= self.jule_dict[need_type_id]
        cache.character_data[self.character_id].ability[self.ability_id] += 1


class Character_talent_show_Text:
    """
    角色素质升级显示面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        # self.column = column
        # """ 每行状态最大个数 """
        self.character_data = cache.character_data[self.character_id]
        """ 角色数据 """

    def draw(self):
        """绘制对象"""
        self.return_list = []
        # 绘制标题#
        line_feed.draw()
        title_text = "素质"
        type_line = draw.LittleTitleLineDraw(title_text, self.width, ":")
        type_line.draw()
        # 前提说明#
        text_draw_introduce = draw.NormalDraw()
        text_draw_introduce.text = "基础前提条件： 好感度500以上 信任度50%以上 反发刻印0\n分为爱情系与隶属系两条路线\n"
        text_draw_introduce.width = 1
        text_draw_introduce.draw()
        line = draw.LineDraw("-", self.width)
        line.draw()
        love = 0
        obey = 0
        # 恋慕分支#
        if game_config.config_talent[10] == 1:
            love = 11
            button_text_love = game_config.config_talent[11].name
        elif game_config.config_talent[11] == 1:
            love = 12
            button_text_love = game_config.config_talent[12].name
        elif game_config.config_talent[12] == 1:
            love = 13
            button_text_love = game_config.config_talent[13].name
        elif game_config.config_talent[13] == 1:
            love = 14
        else:
            love = 10
            button_text_love = game_config.config_talent[10].name
        # 隶属分支#
        if game_config.config_talent[15] == 1:
            obey = 16
            button_text_obey = game_config.config_talent[16].name
        elif game_config.config_talent[16] == 1:
            obey = 17
            button_text_obey = game_config.config_talent[17].name
        elif game_config.config_talent[17] == 1:
            obey = 18
            button_text_obey = game_config.config_talent[18].name
        elif game_config.config_talent[18] == 1:
            obey = 19
        else:
            obey = 15
            button_text_obey = game_config.config_talent[15].name
        # 爱情文本#
        text_draw_love = draw.NormalDraw()
        text_draw_love.text = "爱情路线前提： 苦痛刻印0 恐怖刻印0 亲密等级高于顺从等级\n"
        text_draw_love.width = 1
        text_draw_love.draw()
        # 没进入隶属路线则触发#
        if obey == 15:
            if love == 14:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "已达到最高级-爱侣\n"
                text_draw_love.width = 1
                text_draw_love.draw()
            elif self.character_data.favorability[0] < 500 or self.character_data.trust < 50 or \
                    self.character_data.ability[18] != 0:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "未满足基础前提\n"
                text_draw_love.width = 1
                text_draw_love.draw()
            elif self.character_data.ability[15] != 0 or self.character_data.ability[17] != 0 or \
                    self.character_data.ability[32] <= self.character_data.ability[31]:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "未满足爱情路线前提\n"
                text_draw_love.width = 1
                text_draw_love.draw()
            else:
                now_abi_up_panel = Charactertal_cmd_Text(self.character_id, self.width, love)
                button_draw = draw.LeftButton(
                    _(button_text_love),
                    _(button_text_love),
                    self.width / 10,
                    cmd_func=now_abi_up_panel.draw)
                self.return_list.append(button_draw.return_text)
                button_draw.draw()
        line = draw.LineDraw("-", self.width)
        line.draw()
        # 隶属文本#
        text_draw_love = draw.NormalDraw()
        text_draw_love.text = "隶属路线前提： 快乐刻印>=1 屈服刻印>=1 顺从等级高于亲密等级\n"
        text_draw_love.width = 1
        text_draw_love.draw()
        # 没进入爱情路线则触发#
        if love == 10:
            if obey == 19:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "已达到最高级-奴隶"
                text_draw_love.width = 1
                text_draw_love.draw()
            elif self.character_data.favorability[0] < 500 or self.character_data.trust < 50 or \
                    self.character_data.ability[18] != 0:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "未满足基础前提"
                text_draw_love.width = 1
                text_draw_love.draw()
            elif self.character_data.ability[13] == 0 or self.character_data.ability[14] == 0 or \
                    self.character_data.ability[31] <= self.character_data.ability[32]:
                text_draw_love = draw.NormalDraw()
                text_draw_love.text = "未满足隶属路线前提"
                text_draw_love.width = 1
                text_draw_love.draw()
            else:
                now_abi_up_panel = Charactertal_cmd_Text(self.character_id, self.width, obey)
                button_draw = draw.LeftButton(
                    _(button_text_obey),
                    _(button_text_obey),
                    self.width / 10,
                    cmd_func=now_abi_up_panel.draw)
                self.return_list.append(button_draw.return_text)
                button_draw.draw()


class Charactertal_cmd_Text:
    """
    角色素质升级指令面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int, talent_id: int, ):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        self.talent_id = talent_id
        """ 当前的能力id """
        self.return_list: List[str] = []
        """ 监听的按钮列表 """
        self.character_data = cache.character_data[self.character_id]
        """ 角色数据 """

    def draw(self):
        """绘制对象"""
        self.return_list = []
        self.jule_dict = {}
        judge = 1
        # 绘制标题#
        while 1:
            need_list = game_config.config_talent_up_data[self.talent_id]
            for need_id in need_list:
                need_type = need_list[need_id].need_type
                need_type_id = need_list[need_id].need_type_id
                need_value = need_list[need_id].value
                if need_type == "A":
                    abi_name = game_config.config_ability[need_type_id].name
                    button_text = "需要能力 :" + abi_name + "至少为" + str(need_value) + "\n"
                    if self.character_data.ability[need_type_id] < need_value:
                        judge = 0
                elif need_type == "E":
                    experience_name = game_config.config_experience[need_type_id].name
                    button_text = "需要经验 :" + experience_name + "至少为" + str(need_value) + "\n"
                    if self.character_data.experience[need_type_id] < need_value:
                        judge = 0
                elif need_type == "F":
                    button_text = "需要好感至少为" + str(need_value) + "\n"
                    if self.character_data.favorability[0] < need_value:
                        judge = 0
                elif need_type == "F":
                    button_text = "需要信赖至少为" + str(need_value) + "%\n"
                    if self.character_data.trust < need_value:
                        judge = 0
                now_draw = draw.NormalDraw()
                now_draw.text = button_text
                now_draw.draw()
            if judge:
                now_draw_succed = draw.NormalDraw()
                now_draw_succed.text = "满足条件，要升级吗？\n"
                now_draw_succed.draw()
            else:
                now_draw_failed = draw.NormalDraw()
                now_draw_failed.text = "不满足条件，无法升级\n"
                now_draw_failed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width / 3)
            back_draw.draw()
            self.return_list.append(back_draw.return_text)
            if judge:
                yes_draw = draw.CenterButton(_("[确定]"), _("确定"), self.width / 3, cmd_func=self.level_up)
                yes_draw.draw()
                self.return_list.append(yes_draw.return_text)
            yrn = flow_handle.askfor_all(self.return_list)
            py_cmd.clr_cmd()
            line_feed.draw()
            if yrn == back_draw.return_text:
                break

    def level_up(self):
        cache.character_data[self.character_id].talent[self.talent_id] = 1


class CharacterImage:
    """
    角色立绘面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 绘制的角色id """
        self.width = width
        """ 当前最大可绘制宽度 """
        # self.type = type
        # """ 当前绘制类型 """
        character_data = cache.character_data[self.character_id]
        """ 角色属性 """
        self.draw_list: List[draw.NormalDraw()] = []
        """ 绘制对象列表 """
        self.title_list: List[draw.NormalDraw()] = []
        """ 绘制标题列表 """
        title_text = "立绘"
        type_line = draw.LittleTitleLineDraw(title_text, width, ":")
        self.title_list.append(type_line)
        self.image_name = character_data.name
        now_draw_1 = draw.NormalDraw()
        now_draw_1.text = "  "
        now_draw_1.width = 2
        self.draw_list.append(now_draw_1)

    def draw(self):
        """绘制对象"""
        if self.character_id != 0:
            for value in self.title_list:
                value.draw()
            # for value in self.draw_list:
            #     value.draw()
            flow_handle.print_image_cmd(self.image_name, "立绘按钮")


class CharacterExperienceText:
    """
    显示角色经验面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        type_data = "经验"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        experience_text_list = []
        for experience_id in game_config.config_experience:
            if character_data.sex == 0:
                if experience_id in {2, 4, 7, 12, 14, 17, 20, 22, 26, 51, 54, 55, 58, 72, 74, 77, 86, 100, 101, 102,
                                     103, 104, 105, 106}:
                    continue
            elif character_data.sex == 1:
                if experience_id == {3, 13, 21, 73}:
                    continue
            experience_text = game_config.config_experience[experience_id].name
            experience_value = 0
            if experience_id in character_data.experience:
                experience_value = character_data.experience[experience_id]
                now_text = f" {experience_text}:{experience_value}"
            if experience_value > 0:
                experience_text_list.append(now_text)
        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(experience_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        # title_draw = draw.TitleLineDraw(_("人物状态"), self.width)
        # title_draw.draw()
        line_feed.draw()
        count = 0
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                    count += 1
                line_feed.draw()
            else:
                label.draw()
        if count <= 8:
            line_feed.draw()
            if count == 0:
                line_feed.draw()


class CharacterTalentText:
    """
    显示角色素质面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        profession_text = game_config.config_profession[character_data.profession].name
        race_text = game_config.config_race[character_data.race].name
        type_data = "素质"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        talent_list = game_config.config_talent_type_data
        # print("进入for之前")
        conut = 0
        for talent_type in talent_list:
            type_data = game_config.config_talent_type[talent_type]
            type_line = draw.LittleTitleLineDraw(type_data.name, width, ":")
            # print("type_data.name :",type_data.name)
            type_set = talent_list[talent_type]
            talent_text_list = []
            if conut == 0:
                message_profession = _(" 职业    ：[{profession_text}]").format(
                    profession_text=profession_text,
                )
                talent_text_list.append(message_profession)
                message_race = _("\n 种族    ：[{race_text}]").format(
                    race_text=race_text,
                )
                talent_text_list.append(message_race)
                conut = 1
            race_type = type_data.name
            if talent_type == 0:
                message_race = f"\n {race_type}  ："
            else:
                message_race = f"\n {race_type}："
            for talent_id in type_set:
                talent_text = game_config.config_talent[talent_id].name
                if character_data.talent[talent_id]:
                    now_text = f"[{talent_text}]"
                    message_race += now_text
            talent_text_list.append(message_race)
            if self.center_status:
                now_draw = panel.CenterDrawTextListPanel()
            else:
                now_draw = panel.LeftDrawTextListPanel()
            now_draw.set(talent_text_list, self.width, self.column)
            self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                # line_feed.draw()
            else:
                label.draw()


class CharacterWorkText:
    """
    显示角色工作面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        work_type = character_data.work.work_type

        work_cid = game_config.config_work_type[work_type].cid
        work_name = game_config.config_work_type[work_type].name
        work_place = game_config.config_work_type[work_type].department
        work_describe = game_config.config_work_type[work_type].describe

        f"[{work_cid}]{work_name}({work_place})：{work_describe}",

        profession_text = game_config.config_profession[character_data.profession].name
        race_text = game_config.config_race[character_data.race].name
        type_data = "工作"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        talent_list = game_config.config_talent_type_data
        # print("进入for之前")
        conut = 0
        for talent_type in talent_list:
            type_data = game_config.config_talent_type[talent_type]
            type_line = draw.LittleTitleLineDraw(type_data.name, width, ":")
            # print("type_data.name :",type_data.name)
            type_set = talent_list[talent_type]
            talent_text_list = []
            if conut == 0:
                message_profession = _(" 职业    ：[{profession_text}]").format(
                    profession_text=profession_text,
                )
                talent_text_list.append(message_profession)
                message_race = _("\n 种族    ：[{race_text}]").format(
                    race_text=race_text,
                )
                talent_text_list.append(message_race)
                conut = 1
            race_type = type_data.name
            if talent_type == 0:
                message_race = f"\n {race_type}  ："
            else:
                message_race = f"\n {race_type}："
            for talent_id in type_set:
                talent_text = game_config.config_talent[talent_id].name
                if character_data.talent[talent_id]:
                    now_text = f"[{talent_text}]"
                    message_race += now_text
            talent_text_list.append(message_race)
            if self.center_status:
                now_draw = panel.CenterDrawTextListPanel()
            else:
                now_draw = panel.LeftDrawTextListPanel()
            now_draw.set(talent_text_list, self.width, self.column)
            self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                # line_feed.draw()
            else:
                label.draw()


class CharacterJuelText:
    """
    显示角色宝珠面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        type_data = "宝珠"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        juel_text_list = []
        for juel_id in game_config.config_juel:
            if character_data.sex == 0:
                if juel_id in {2, 4, 7}:
                    continue
            elif character_data.sex == 1:
                if juel_id == {3}:
                    continue
            juel_text = game_config.config_juel[juel_id].name
            juel_value = 0
            if juel_id in character_data.juel:
                juel_value = character_data.juel[juel_id]
            now_text = f" {juel_text}:{juel_value}"
            juel_text_list.append(now_text)
        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(juel_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class CharacterTokenText:
    """
    显示角色信物面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        type_data = "信物"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        token_text_list = []
        for token_id in range(len(character_data.pl_collection.token_list)):
            if token_id == 0:
                continue
            if character_data.pl_collection.token_list[token_id] == 1:
                target_character_data = cache.character_data[token_id]
                character_name = target_character_data.name
                token_text = target_character_data.token_text
                now_text = f" 已拥有{character_name}的信物:{token_text}"
                token_text_list.append(now_text)
        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(token_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class CharacterBodyText:
    """
    显示角色肉体面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        type_data = "肉体情况"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        body_text_list = []
        if character_id != 0:
            # 尿道信息#
            now_text = f"\n 【总】\n"
            semen_count = 0
            for body_part in game_config.config_body_part:
                semen_count += character_data.dirty.body_semen[body_part][3]
            if semen_count == 0:
                now_text += "  未接触过精液\n"
            else:
                now_text += f"  全身总共被射上过{semen_count}ml精液\n"
            body_text_list.append(now_text)
            # 口部信息#
            now_text = f"\n 【口】\n"
            now_text += "  初吻情况："
            if character_data.talent[4]:
                now_text += "保有初吻\n"
            else:
                kiss_id = character_data.first_record.first_kiss_id
                kiss_time = character_data.first_record.first_kiss_time
                now_text += _("于{kiss_time}在{kiss_palce}，向{character_name}博士献上了初吻\n").format(
                    character_name=cache.character_data[kiss_id].name,
                    kiss_time=str(kiss_time.month) + "月" + str(kiss_time.day) + "日",
                    kiss_palce=attr_text.get_scene_path_text(character_data.first_record.first_kiss_place),
                )
            if character_data.ability[71] == 0:
                now_text += "  普普通通的舌头\n"
            if character_data.dirty.body_semen[2][3] == 0:
                now_text += "  未品尝过精液\n"
            else:
                now_text += f"  总共喝过{character_data.dirty.body_semen[2][3]}ml精液\n"
            body_text_list.append(now_text)
            # 胸部信息#
            now_text = f"\n 【胸】\n"
            if character_data.dirty.body_semen[3][3] == 0:
                now_text += "  未淋上过精液\n"
            else:
                now_text += f"  总共被淋上过{character_data.dirty.body_semen[3][3]}ml精液\n"
            body_text_list.append(now_text)
            # 指部信息#
            now_text = f"\n 【指】\n"
            if character_data.dirty.body_semen[5][3] == 0:
                now_text += "  未淋上过精液\n"
            else:
                now_text += f"  总共被淋上过{character_data.dirty.body_semen[5][3]}ml精液\n"
            body_text_list.append(now_text)
            # 足部信息#
            now_text = f"\n 【足】\n"
            if character_data.dirty.body_semen[11][3] == 0:
                now_text += "  未淋上过精液\n"
            else:
                now_text += f"  总共被淋上过{character_data.dirty.body_semen[11][3]}ml精液\n"
            body_text_list.append(now_text)
            # 膣部信息#
            now_text = f"\n 【膣】\n"
            now_text += "  处女情况："
            if character_data.talent[0]:
                now_text += "保有处女\n"
            else:
                sex_id = character_data.first_record.first_sex_id
                sex_time = character_data.first_record.first_sex_time
                sex_posture = character_data.first_record.first_sex_posture

                now_text += _("于{time}在{palce}，被{character_name}博士以{posture}夺走了处女\n").format(
                    character_name=cache.character_data[sex_id].name,
                    time=str(sex_time.month) + "月" + str(sex_time.day) + "日",
                    palce=attr_text.get_scene_path_text(character_data.first_record.first_sex_place),
                    posture=sex_posture,
                )
            if character_data.dirty.body_semen[7][3] == 0:
                now_text += "  未射入过精液\n"
            else:
                now_text += f"  总共被射入过{character_data.dirty.body_semen[7][3]}ml精液\n"
            body_text_list.append(now_text)
            # 肛部信息#
            now_text = f"\n 【肛】\n"
            now_text += "  后庭处女情况："
            if character_data.talent[1]:
                now_text += "保有后庭处女\n"
            else:
                a_sex_id = character_data.first_record.first_a_sex_id
                a_sex_time = character_data.first_record.first_a_sex_time
                a_sex_posture = character_data.first_record.first_a_sex_posture

                now_text += _("于{time}在{palce}，被{character_name}博士以{posture}夺走了A处女\n").format(
                    character_name=cache.character_data[a_sex_id].name,
                    time=str(a_sex_time.month) + "月" + str(a_sex_time.day) + "日",
                    palce=attr_text.get_scene_path_text(character_data.first_record.first_a_sex_place),
                    posture=a_sex_posture,
                )
            if character_data.dirty.body_semen[8][3] == 0:
                now_text += "  未射入过精液\n"
            else:
                now_text += f"  总共被射入过{character_data.dirty.body_semen[8][3]}ml精液\n"
            body_text_list.append(now_text)
            # 子宫信息#
            now_text = f"\n 【宫】\n"
            if character_data.experience[86] == 0:
                now_text += "  未怀孕过\n"
            body_text_list.append(now_text)
            # 尿道信息#
            now_text = f"\n 【尿】\n"
            if character_data.dirty.body_semen[9][3] == 0:
                now_text += "  未射入过精液\n"
            else:
                now_text += f"  总共被射入过{character_data.dirty.body_semen[9][3]}ml精液\n"
            body_text_list.append(now_text)
        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(body_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


class PlayerAbilityText:
    """
    显示玩家能力面板对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    column -- 每行状态最大个数
    type_number -- 显示的状态类型
    """

    def __init__(self, character_id: int, width: int, column: int, center_status: bool = True):
        """初始化绘制对象"""
        self.character_id = character_id
        """ 要绘制的角色id """
        self.width = width
        """ 面板最大宽度 """
        self.column = column
        """ 每行状态最大个数 """
        self.draw_list: List[draw.NormalDraw] = []
        """ 绘制的文本列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.center_status: bool = center_status
        """ 居中绘制状态文本 """
        character_data = cache.character_data[character_id]
        type_data = "玩家能力"
        type_line = draw.LittleTitleLineDraw(type_data, width, ":")
        self.draw_list.append(type_line)
        ability_text_list = []

        # 视觉能力#
        now_text = f"\n 【视觉系】\n"
        for i in {307, 308, 309}:
            if character_data.talent[i]:
                ability_name = game_config.config_talent[i].name
                ability_info = game_config.config_talent[i].info
                now_text += f"  {ability_name}：{ability_info}\n"
        ability_text_list.append(now_text)

        # 触觉能力#
        now_text = f"\n 【触觉系】\n"
        for i in {310, 311, 312}:
            if character_data.talent[i]:
                ability_name = game_config.config_talent[i].name
                ability_info = game_config.config_talent[i].info
                now_text += f"  {ability_name}：{ability_info}\n"
        ability_text_list.append(now_text)

        # 激素能力#
        now_text = f"\n 【激素系】\n"
        for i in {304, 305, 306}:
            if character_data.talent[i]:
                ability_name = game_config.config_talent[i].name
                ability_info = game_config.config_talent[i].info
                now_text += f"  {ability_name}：{ability_info}\n"
        ability_text_list.append(now_text)

        if self.center_status:
            now_draw = panel.CenterDrawTextListPanel()
        else:
            now_draw = panel.LeftDrawTextListPanel()
        now_draw.set(ability_text_list, self.width, self.column)
        self.draw_list.extend(now_draw.draw_list)

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        for label in self.draw_list:
            if isinstance(label, list):
                for value in label:
                    value.draw()
                line_feed.draw()
            else:
                label.draw()


# class SeeCharacterSocialContact:
#     """
#     显示角色社交关系面板对象
#     Keyword arguments:
#     character_id -- 角色id
#     width -- 绘制宽度
#     """

#     def __init__(self, character_id: int, width: int):
#         """初始化绘制对象"""
#         self.character_id: int = character_id
#         """ 要绘制的角色id """
#         self.width: int = width
#         """ 面板最大宽度 """
#         self.draw_list: List[draw.NormalDraw] = []
#         """ 绘制的文本列表 """
#         self.return_list: List[str] = []
#         """ 当前面板监听的按钮列表 """
#         character_data = cache.character_data[self.character_id]
#         for social_type in game_config.config_social_type:
#             if not social_type:
#                 continue
#             type_config = game_config.config_social_type[social_type]
#             type_draw = draw.LittleTitleLineDraw(type_config.name, self.width, ":")
#             self.draw_list.append(type_draw)
#             now_draw = draw.CenterDraw()
#             if social_type in character_data.social_contact and len(
#                 character_data.social_contact[social_type]
#             ):
#                 character_list = list(character_data.social_contact[social_type])
#                 now_draw = panel.PageHandlePanel(
#                     character_list, SeeCharacterInfoByNameDraw, 10, 5, self.width, 1, 1, 0
#                 )
#             else:
#                 now_draw.text = _("空无一人")
#                 now_draw.width = self.width
#             self.draw_list.append(now_draw)
#             self.draw_list.append(line_feed)

#     def draw(self):
#         title_draw = draw.TitleLineDraw(_("人物社交"), self.width)
#         title_draw.draw()
#         self.return_list = []
#         now_start_id = 0
#         for value in self.draw_list:
#             if isinstance(value, panel.PageHandlePanel):
#                 value.button_start_id = now_start_id
#                 value.update()
#                 value.draw()
#                 self.return_list.extend(value.return_list)
#                 now_start_id = len(self.return_list)
#             else:
#                 value.draw()


class SeeCharacterInfoByNameDraw:
    """
    点击后可查看角色属性的角色名字按钮对象
    Keyword arguments:
    text -- 角色id
    width -- 最大宽度
    is_button -- 绘制按钮
    num_button -- 绘制数字按钮
    button_id -- 数字按钮的id
    """

    def __init__(self, text: str, width: int, is_button: bool, num_button: bool, button_id: int):
        """初始化绘制对象"""
        self.character_id: int = int(text)
        """ 角色id """
        self.draw_text: str = ""
        """ 角色名绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.is_button: bool = is_button
        """ 绘制按钮 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        character_data = cache.character_data[self.character_id]
        character_name = character_data.name
        name_draw = draw.NormalDraw()
        if is_button:
            if num_button:
                index_text = text_handle.id_index(button_id)
                button_text = f"{index_text} {character_name}"
                name_draw = draw.CenterButton(
                    button_text, self.button_return, self.width, cmd_func=self.see_character
                )
            else:
                button_text = f"[{character_name}]"
                name_draw = draw.CenterButton(
                    button_text, character_name, self.width, cmd_func=self.see_character
                )
                self.button_return = character_name
            self.draw_text = button_text
        else:
            character_name = f"[{character_name}]"
            character_name = text_handle.align(character_name, "center", 0, 1, self.width)
            name_draw.text = character_name
            self.draw_text = character_name
        name_draw.width = self.width
        self.now_draw = name_draw
        """ 绘制的对象 """

    def draw(self):
        """绘制对象"""
        self.now_draw.draw()

    def see_character(self):
        """绘制角色信息"""
        py_cmd.clr_cmd()
        now_draw = SeeCharacterInfoOnSocialPanel(self.character_id, window_width)
        now_draw.draw()


class SeeCharacterInfoByNameDrawInScene:
    """场景中点击后切换目标角色的角色名字按钮对象"""

    def __init__(self, text: str, width: int, is_button: bool, num_button: bool, button_id: int):
        """初始化绘制对象"""
        self.character_id: int = int(text)
        """ 角色id """
        self.draw_text: str = ""
        """ 角色名绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.is_button: bool = is_button
        """ 绘制按钮 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        character_data: game_type.Character = cache.character_data[self.character_id]
        sex_text = game_config.config_sex_tem[character_data.sex].name
        character_name = character_data.name
        # character_name = character_data.name + f"({sex_text})"
        name_draw = draw.NormalDraw()
        if is_button:
            if num_button:
                index_text = text_handle.id_index(button_id)
                button_text = f"{index_text} {character_name}"
                name_draw = draw.CenterButton(
                    button_text, self.button_return, self.width, cmd_func=self.see_character
                )
            else:
                button_text = f"[{character_name}]"
                name_draw = draw.CenterButton(
                    button_text, character_name, self.width, cmd_func=self.see_character
                )
                self.button_return = character_name
            self.draw_text = button_text
        else:
            character_name = f"[{character_name}]"
            character_name = text_handle.align(character_name, "center", 0, 1, self.width)
            name_draw.text = character_name
            self.draw_text = character_name
        name_draw.width = self.width
        self.now_draw = name_draw
        """ 绘制的对象 """

    def draw(self):
        """绘制对象"""
        if isinstance(self.now_draw, draw.NormalDraw):
            self.now_draw.style = "onbutton"
        self.now_draw.draw()

    def see_character(self):
        """切换目标角色"""
        cache.character_data[0].target_character_id = self.character_id
        py_cmd.clr_cmd()


class SeeCharacterInfoByimageDrawInScene:
    """场景中点击后切换目标角色的角色立绘按钮对象"""

    def __init__(self, text: str, width: int, is_button: bool, num_button: bool, button_id: int):
        """初始化绘制对象"""
        self.character_id: int = int(text)
        """ 角色id """
        self.draw_text: str = ""
        """ 角色名绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.is_button: bool = is_button
        """ 绘制按钮 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        character_data: game_type.Character = cache.character_data[self.character_id]
        # sex_text = game_config.config_sex_tem[character_data.sex].name
        character_name = character_data.name
        # character_name = character_data.name + f"({sex_text})"
        button_text = f"{character_name}"
        name_draw = draw.ImageButton(
            button_text, self.button_return, self.width, cmd_func=self.see_character
        )
        character_name = f"[{character_name}]"
        character_name = text_handle.align(character_name, "center", 0, 1, self.width)
        name_draw.text = character_name
        self.draw_text = character_name
        name_draw.width = self.width
        self.now_draw = name_draw
        """ 绘制的对象 """

    def draw(self):
        """绘制对象"""
        if isinstance(self.now_draw, draw.NormalDraw):
            self.now_draw.style = "onbutton"
        self.now_draw.draw()

    def see_character(self):
        """切换目标角色"""
        cache.character_data[0].target_character_id = self.character_id
        py_cmd.clr_cmd()


class SeeCharacterInfoOnSocialPanel:
    """
    在社交面板里查看角色属性
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.width: int = width
        """ 面板最大宽度 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.now_draw: SeeCharacterInfoPanel = SeeCharacterInfoHandle(
            character_id, width, list(cache.character_data.keys())
        )
        """ 角色属性面板 """

    def draw(self):
        """绘制面板"""
        line_feed.draw()
        self.now_draw.draw()


class SeeCharacterInfoHandle:
    """
    带切换控制的查看角色属性面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    character_list -- 角色id列表
    """

    def __init__(self, character_id: int, width: int, character_list: List[int]):
        """初始化绘制对象"""
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.width: int = width
        """ 面板最大宽度 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        self.character_list: List[int] = character_list
        """ 当前面板所属的角色id列表 """

    def draw(self):
        """绘制面板"""
        old_button_draw = draw.CenterButton(
            _("[上一人]"), _("上一人"), self.width / 3, cmd_func=self.old_character
        )
        next_button_draw = draw.CenterButton(
            _("[下一人]"), _("下一人"), self.width / 3, cmd_func=self.next_character
        )
        back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width / 3)
        now_panel_id = _("基础属性")
        while 1:
            self.return_list = []
            now_character_panel = SeeCharacterInfoPanel(self.character_id, self.width)
            now_character_panel.change_panel(now_panel_id)
            now_character_panel.draw()
            old_button_draw.draw()
            back_draw.draw()
            next_button_draw.draw()
            line_feed.draw()
            self.return_list.extend(now_character_panel.return_list)
            self.return_list.append(old_button_draw.return_text)
            self.return_list.append(back_draw.return_text)
            self.return_list.append(next_button_draw.return_text)
            yrn = flow_handle.askfor_all(self.return_list)
            py_cmd.clr_cmd()
            line_feed.draw()
            if yrn == back_draw.return_text:
                break
            elif yrn in now_character_panel.draw_data:
                now_panel_id = yrn

    def old_character(self):
        """切换显示上一人"""
        now_index = self.character_list.index(self.character_id)
        self.character_id = self.character_list[now_index - 1]

    def next_character(self):
        """切换显示下一人"""
        now_index = self.character_list.index(self.character_id) + 1
        if now_index > len(self.character_list) - 1:
            now_index = 0
        self.character_id = self.character_list[now_index]


class GetUpCharacterInfoDraw:
    """
    起床面板按角色id绘制角色缩略信息
    Keyword arguments:
    text -- 角色id
    width -- 最大宽度
    is_button -- 绘制按钮
    num_button -- 绘制数字按钮
    button_id -- 数字按钮的id
    """

    def __init__(self, text: int, width: int, is_button: bool, num_button: bool, button_id: int):
        """初始化绘制对象"""
        self.text: int = text
        """ 角色id """
        self.draw_text: str = ""
        """ 角色缩略信息绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.is_button: bool = is_button
        """ 绘制按钮 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        character_data = cache.character_data[self.text]
        character_name = character_data.name
        # id_text = f"No.{self.text}"
        sex_config = game_config.config_sex_tem[character_data.sex]
        # sex_text = _(f"性别:{sex_config.name}")
        # age_text = _(f"年龄:{character_data.age}岁")
        hit_point_text = _(f"体力:({character_data.hit_point}/{character_data.hit_point_max})")
        mana_point_text = _(f"气力:({character_data.mana_point}/{character_data.mana_point_max})")
        now_text = f" {character_name} {hit_point_text} {mana_point_text}"
        if is_button:
            if num_button:
                index_text = text_handle.id_index(self.button_id)
                now_text_width = self.width - len(index_text)
                new_text = text_handle.align(now_text, "center", text_width=now_text_width)
                self.draw_text = f"{index_text}{new_text}"
                self.button_return = str(button_id)
            else:
                new_text = text_handle.align(now_text, "center", text_width=self.width)
                self.draw_text = new_text
                self.button_return = character_name
        else:
            new_text = text_handle.align(now_text, "center", text_width=self.width)
            self.draw_text = new_text

    def draw(self):
        """绘制对象"""
        if self.is_button:
            now_draw = draw.Button(self.draw_text, self.button_return, cmd_func=self.draw_character_info)
        else:
            now_draw = draw.NormalDraw()
            now_draw.text = self.draw_text
        now_draw.width = self.width
        now_draw.draw()

    def draw_character_info(self):
        """绘制角色信息"""
        line_feed.draw()
        py_cmd.clr_cmd()
        now_draw = SeeCharacterInfoHandle(self.text, window_width, list(cache.character_data.keys()))
        now_draw.draw()


class SeeCharacterInfoHandleInScene(SeeCharacterInfoHandle):
    """在场景中带切换控制的查看角色属性面板"""

    def old_character(self):
        """切换显示上一人"""
        if len(self.character_list):
            if self.character_id:
                now_index = self.character_list.index(self.character_id)
                if now_index:
                    now_index -= 1
                    self.character_id = self.character_list[now_index]
                else:
                    self.character_id = 0
            else:
                self.character_id = self.character_list[len(self.character_list) - 1]

    def next_character(self):
        """切换显示上一人"""
        if len(self.character_list):
            if self.character_id:
                now_index = self.character_list.index(self.character_id)
                if now_index == len(self.character_list) - 1:
                    self.character_id = 0
                else:
                    self.character_id = self.character_list[now_index + 1]
            else:
                self.character_id = self.character_list[0]


class SeeCharacterInfoInScenePanel:
    """
    在场景中查看角色属性的控制对象
    Keyword arguments:
    target_id -- 目标id
    width -- 绘制宽度
    """

    def __init__(self, target_id: int, width: int):
        """初始化绘制对象"""
        self.target_id: int = target_id
        """ 查看属性的目标 """
        self.width: int = width
        """ 绘制宽度 """
        position = cache.character_data[0].position
        position_str = map_handle.get_map_system_path_str_for_list(position)
        scene_data: game_type.Scene = cache.scene_data[position_str]
        if cache.is_collection:
            character_data: game_type.Character = cache.character_data[0]
            now_list = [i for i in scene_data.character_list if i in character_data.collection_character]
        else:
            now_list = list(scene_data.character_list)
            now_list.remove(0)
        self.handle_panel = SeeCharacterInfoHandleInScene(target_id, width, now_list)
        """ 绘制控制面板 """

    def draw(self):
        """绘制对象"""
        self.handle_panel.draw()
        cache.now_panel_id = constant.Panel.IN_SCENE


class Character_abi_up_main_Handle:
    """
    带返回的角色能力上升主面板
    Keyword arguments:
    character_id -- 角色id
    width -- 最大宽度
    character_list -- 角色id列表
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.width: int = width
        """ 面板最大宽度 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        back_draw = draw.CenterButton(_("[返回]"), _("返回"), self.width / 3)
        now_panel_id = _("属性升级")
        while 1:
            self.return_list = []
            now_character_panel = Character_abi_up_sub_Handle(self.character_id, self.width)
            now_character_panel.change_panel(now_panel_id)
            now_character_panel.draw()
            back_draw.draw()
            line_feed.draw()
            self.return_list.extend(now_character_panel.return_list)
            self.return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(self.return_list)
            py_cmd.clr_cmd()
            line_feed.draw()
            if yrn == back_draw.return_text:
                break
            elif yrn in now_character_panel.draw_data:
                now_panel_id = yrn


class Character_abi_up_sub_Handle:
    """
    角色能力上升子面板
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel: str = _("属性升级")
        """ 当前的属性页id """
        self.character_id: int = character_id
        """ 要绘制的角色id """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """
        main_first_draw = Character_abi_up_frist_Handle(character_id, width)
        self.draw_data = {
            _("属性升级"): main_first_draw,
        }
        """ 按钮文本对应属性面板 """
        self.handle_panel = panel.CenterDrawButtonListPanel()
        """ 属性列表的控制面板 """
        self.handle_panel.set(
            [f"[{text}]" for text in self.draw_data.keys()],
            list(self.draw_data.keys()),
            width,
            4,
            f"[{self.now_panel}]",
            self.change_panel,
        )

    def change_panel(self, panel_id: str):
        """
        切换当前面板
        Keyword arguments:
        panel_id -- 要切换的面板id
        """
        self.now_panel = panel_id
        self.handle_panel.set(
            [f"[{text}]" for text in self.draw_data.keys()],
            list(self.draw_data.keys()),
            self.width,
            4,
            f"[{self.now_panel}]",
            self.change_panel,
        )

    def draw(self):
        """绘制面板"""
        self.draw_data[self.now_panel].draw()
        self.return_list = []
        self.return_list.extend(self.draw_data[self.now_panel].return_list)
        line_feed.draw()
        line = draw.LineDraw("=", self.width)
        line.draw()
        self.handle_panel.draw()
        self.return_list.extend(self.handle_panel.return_list)


class Character_abi_up_frist_Handle:
    """
    角色能力升级面板第一页对象
    Keyword arguments:
    character_id -- 角色id
    width -- 绘制宽度
    """

    def __init__(self, character_id: int, width: int):
        """初始化绘制对象"""
        head_draw = CharacterInfoHead(character_id, width)
        Juel_draw = CharacterJuelText(character_id, width, 8, 0)
        Experience_draw = CharacterExperienceText(character_id, width, 8, 0)
        abi_draw = Characterabi_show_Text(character_id, width)
        tal_draw = Character_talent_show_Text(character_id, width)
        if character_id == 0:
            self.draw_list: List[draw.NormalDraw] = [
                head_draw,
                Juel_draw,
                Experience_draw,
                abi_draw,
            ]
        else:
            self.draw_list: List[draw.NormalDraw] = [
                head_draw,
                Juel_draw,
                Experience_draw,
                abi_draw,
                tal_draw,
            ]
        """ 绘制的面板列表 """
        self.return_list: List[str] = []
        """ 当前面板监听的按钮列表 """

    def draw(self):
        """绘制面板"""
        for label in self.draw_list:
            label.draw()
            if "return_list" in label.__dict__:
                self.return_list.extend(label.return_list)
