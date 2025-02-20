import datetime
import random
from typing import List
from Script.Config import game_config
from Script.Design import handle_state_machine, character_move, map_handle, clothing, handle_instruct, basement
from Script.Core import cache_control, game_type, constant
from Script.UI.Moudle import draw

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1


@handle_state_machine.add_state_machine(constant.StateMachine.WAIT_5_MIN)
def character_wait_5_min(character_id: int):
    """
    等待5分钟
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.WAIT
    character_data.behavior.duration = 5
    character_data.state = constant.CharacterStatus.STATUS_WAIT
    character_data.wait_flag = 0


@handle_state_machine.add_state_machine(constant.StateMachine.WAIT_10_MIN)
def character_wait_10_min(character_id: int):
    """
    等待10分钟
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.WAIT
    character_data.behavior.duration = 10
    character_data.state = constant.CharacterStatus.STATUS_WAIT


@handle_state_machine.add_state_machine(constant.StateMachine.WAIT_30_MIN)
def character_wait_30_min(character_id: int):
    """
    等待30分钟，并取消跟随状态
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.WAIT
    character_data.behavior.duration = 30
    character_data.state = constant.CharacterStatus.STATUS_WAIT
    character_data.is_follow = 0


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_DORMITORY)
def character_move_to_dormitory(character_id: int):
    """
    移动至所在宿舍
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    _, _, move_path, move_time = character_move.character_move(
        character_id,
        map_handle.get_map_system_path_for_str(character_data.dormitory),
    )
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.SLEEP)
def character_sleep(character_id: int):
    """
    睡觉
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    clothing.get_sleep_cloth(character_id)
    character_data.behavior.behavior_id = constant.Behavior.SLEEP
    character_data.behavior.duration = 480
    character_data.state = constant.CharacterStatus.STATUS_SLEEP
    character_data.tired = 0

# @handle_state_machine.add_state_machine(constant.StateMachine.FOLLOW)
# def character_follow(character_id: int):
#     """
#     跟随玩家
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.talent[400] = 1

@handle_state_machine.add_state_machine(constant.StateMachine.REST)
def character_rest(character_id: int):
    """
    休息
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.REST
    character_data.behavior.duration = 30
    character_data.state = constant.CharacterStatus.STATUS_REST


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_RAND_SCENE)
def character_move_to_rand_scene(character_id: int):
    """
    移动至随机场景
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    scene_list = list(cache.scene_data.keys())
    now_scene_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_list.remove(now_scene_str)
    target_scene = random.choice(scene_list)
    _, _, move_path, move_time = character_move.character_move(
        character_id,
        map_handle.get_map_system_path_for_str(target_scene),
    )
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_MODERN_MUSIC_ROOM)
def character_move_to_modern_music_room(character_id: int):
    """
    移动至现代音乐室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    to_cafeteria = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Modern_Musicroom"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_cafeteria)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_DR_OFFICE)
def character_move_to_dr_office(character_id: int):
    """
    移动至博士办公室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    to_dr_office = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Dr_office"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_dr_office)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_TOILET)
def character_move_to_toilet(character_id: int):
    """
    移动至洗手间
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    # 检索当前角色所在的大场景里有没有厕所，没有的话再随机选择其他厕所
    now_position = character_data.position[0]
    find_flag = False
    if character_data.sex == 0:
        to_toilet = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Toilet_Male"])
    )
    elif character_data.sex == 1:
        for place in constant.place_data["Toilet_Female"]:
            if place.split("\\")[0] == now_position:
                to_toilet = map_handle.get_map_system_path_for_str(place)
                find_flag = True
                break
        if not find_flag:
            to_toilet = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Toilet_Female"])
    )
    # print(f"debug constant.place_data[\"Toilet_Female\"] = ",constant.place_data["Toilet_Female"])
    _, _, move_path, move_time = character_move.character_move(character_id, to_toilet)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去洗手间"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_FOODSHOP)
def character_move_to_foodshop(character_id: int):
    """
    移动至食物商店（取餐区）
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    to_foodshop = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Food_Shop"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_foodshop)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去吃饭"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_DINING_HALL)
def character_move_to_dining_hall(character_id: int):
    """
    移动至食堂
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    to_dining_hall = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Dining_hall"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_dining_hall)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_CLINIC)
def character_move_to_clinic(character_id: int):
    """
    随机移动到门诊室（含急诊室）
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    # 判断是否存在没有人的门诊室，存在的话优先去没有人的
    empty_flag = False
    for Clinic_place in constant.place_data["Clinic"]:
        if list(cache.scene_data[Clinic_place].character_list) == []:
            empty_flag = True
            to_clinic = map_handle.get_map_system_path_for_str(Clinic_place)
            break
    if not empty_flag:
        to_clinic = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Clinic"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_clinic)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_HR_OFFICE)
def character_move_to_hr_office(character_id: int):
    """
    移动到人事部办公室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    to_hr_office = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["HR_office"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_hr_office)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_LIBRARY_OFFICE)
def character_move_to_library_office(character_id: int):
    """
    移动到图书馆办公室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    to_library_office = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Library_office"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_library_office)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_LIBRARY)
def character_move_to_library(character_id: int):
    """
    移动到图书馆
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    to_library = map_handle.get_map_system_path_for_str(
        random.choice(constant.place_data["Library"])
    )
    _, _, move_path, move_time = character_move.character_move(character_id, to_library)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_REST_ROOM)
def character_move_to_rest_room(character_id: int):
    """
    移动至休息室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    # 检索当前角色所在的大场景里有没有休息室，没有的话再随机选择其他区块
    now_position = character_data.position[0]
    find_flag = False
    for place in constant.place_data["Rest_Room"]:
        if place.split("\\")[0] == now_position:
            to_rest_room = map_handle.get_map_system_path_for_str(place)
            find_flag = True
            break
    if not find_flag:
        to_rest_room = map_handle.get_map_system_path_for_str(
    random.choice(constant.place_data["Rest_Room"])
    )

    _, _, move_path, move_time = character_move.character_move(character_id, to_rest_room)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去休息"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_BATHZONE_LOCKER_ROOM)
def character_move_to_bathzone_locker_room(character_id: int):
    """
    移动至大浴场的更衣室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    # 直接检索大浴场的更衣室
    for place in constant.place_data["Locker_Room"]:
        if place.split("\\")[0] == "大浴场":
            to_locker_room = map_handle.get_map_system_path_for_str(place)
            break

    _, _, move_path, move_time = character_move.character_move(character_id, to_locker_room)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去大浴场的更衣室"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_BATH_ROOM)
def character_move_to_bath_room(character_id: int):
    """
    移动至淋浴室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id

    # 检索当前角色所在的大场景里有没有淋浴室，没有的话再随机选择其他区块
    now_position = character_data.position[0]
    find_flag = False
    for place in constant.place_data["Bathroom"]:
        if place.split("\\")[0] == now_position:
            to_bath_room = map_handle.get_map_system_path_for_str(place)
            find_flag = True
            break
    if not find_flag:
        to_bath_room = map_handle.get_map_system_path_for_str(
    random.choice(constant.place_data["Bathroom"])
    )

    _, _, move_path, move_time = character_move.character_move(character_id, to_bath_room)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去淋浴"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_TRAINING_ROOM)
def character_move_to_training_room(character_id: int):
    """
    根据职业自动移动至对应训练室
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    if character_data.profession in {1,5,6,8}:
        room_name = "Fight_Room"
    else:
        room_name = "Shoot_Room"

    to_training_room = map_handle.get_map_system_path_for_str(
    random.choice(constant.place_data[room_name])
    )

    _, _, move_path, move_time = character_move.character_move(character_id, to_training_room)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 如果和玩家位于同一地点，则输出提示信息
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "打算去进行战斗训练\n"
        now_draw.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_PLAYER)
def character_move_to_player(character_id: int):
    """
    移动至玩家位置
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    to_dr = cache.character_data[0].position
    _, _, move_path, move_time = character_move.character_move(character_id, to_dr)
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE
    # if character_data.is_follow:
    #     print(f"debug {character_id}号角色向玩家移动，当前跟随={character_data.is_follow}")


@handle_state_machine.add_state_machine(constant.StateMachine.CHAT_RAND_CHARACTER)
def character_chat_rand_character(character_id: int):
    """
    角色和场景内随机角色聊天
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    character_set = scene_data.character_list.copy()
    character_set.remove(character_id)
    character_list = list(character_set)
    if len(character_list):
        target_id = random.choice(character_list)
        character_data.behavior.behavior_id = constant.Behavior.CHAT
        character_data.behavior.duration = 10
        character_data.target_character_id = target_id
        character_data.state = constant.CharacterStatus.STATUS_CHAT


@handle_state_machine.add_state_machine(constant.StateMachine.STROKE_RAND_CHARACTER)
def character_stroke_rand_character(character_id: int):
    """
    角色和场景内随机角色身体接触
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    character_set = scene_data.character_list.copy()
    character_set.remove(character_id)
    character_list = list(character_set)
    if len(character_list):
        target_id = random.choice(character_list)
        character_data.behavior.behavior_id = constant.Behavior.STROKE
        character_data.behavior.duration = 10
        character_data.target_character_id = target_id
        character_data.state = constant.CharacterStatus.STATUS_STROKE


@handle_state_machine.add_state_machine(constant.StateMachine.CHAT_TO_DR)
def character_chat_to_dr(character_id: int):
    """
    角色和玩家聊天
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_id = 0
    character_data.behavior.behavior_id = constant.Behavior.CHAT
    character_data.behavior.duration = 5
    character_data.target_character_id = target_id
    character_data.state = constant.CharacterStatus.STATUS_CHAT


@handle_state_machine.add_state_machine(constant.StateMachine.STROKE_TO_DR)
def character_stroke_to_dr(character_id: int):
    """
    角色和玩家身体接触
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_id = 0
    character_data.behavior.behavior_id = constant.Behavior.STROKE
    character_data.behavior.duration = 10
    character_data.target_character_id = target_id
    character_data.state = constant.CharacterStatus.STATUS_STROKE


@handle_state_machine.add_state_machine(constant.StateMachine.MAKE_COFFEE_TO_DR)
def character_make_coffee_to_dr(character_id: int):
    """
    角色给玩家泡咖啡
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_id = 0
    character_data.behavior.behavior_id = constant.Behavior.MAKE_COFFEE
    character_data.behavior.duration = 15
    character_data.target_character_id = target_id
    character_data.state = constant.CharacterStatus.STATUS_MAKE_COFFEE


@handle_state_machine.add_state_machine(constant.StateMachine.MAKE_COFFEE_ADD_TO_DR)
def character_make_coffee_Add_to_dr(character_id: int):
    """
    角色给玩家泡咖啡（加料）
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_id = 0
    character_data.behavior.behavior_id = constant.Behavior.MAKE_COFFEE_ADD
    character_data.behavior.duration = 15
    character_data.target_character_id = target_id
    character_data.state = constant.CharacterStatus.STATUS_MAKE_COFFEE_ADD


@handle_state_machine.add_state_machine(constant.StateMachine.SEE_H_AND_MOVE_TO_DORMITORY)
def character_see_h_and_move_to_dormitory(character_id: int):
    """
    目睹玩家和其他角色H
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    _, _, move_path, move_time = character_move.character_move(
        character_id,
        map_handle.get_map_system_path_for_str(character_data.dormitory),
    )
    character_data.behavior.behavior_id = constant.Behavior.MOVE
    character_data.behavior.move_target = move_path
    character_data.behavior.duration = move_time
    character_data.state = constant.CharacterStatus.STATUS_MOVE

    # 输出提示信息，并结算把柄
    now_draw = draw.NormalDraw()
    now_draw.text = f"被{character_data.name}看到了情事现场\n"
    if character_data.talent[222]:
        now_draw.text += f"{character_data.name}还不懂这是什么意义，被你随口糊弄走了"
    else:
        character_data.talent[401] = 1
        now_draw.text += f"{character_data.name}获得了[持有博士把柄]\n"
        now_draw.text += f"{character_data.name}红着脸跑走了"
    now_draw.draw()
    line_feed.draw()

    # 中断H
    pl_data: game_type.Character = cache.character_data[0]
    target_data = cache.character_data[pl_data.target_character_id]
    target_data.action_info.h_interrupt = 1
    # 原地待机10分钟
    target_data.behavior.behavior_id = constant.Behavior.WAIT
    target_data.state = constant.CharacterStatus.STATUS_WAIT
    target_data.behavior.duration = 10
    pl_data.behavior.behavior_id = constant.Behavior.H_INTERRUPT
    pl_data.state = constant.CharacterStatus.STATUS_H_INTERRUPT
    handle_instruct.handle_end_h()


@handle_state_machine.add_state_machine(constant.StateMachine.SINGING)
def character_singing(character_id: int):
    """
    唱歌
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.SINGING
    character_data.behavior.duration = 10
    character_data.state = constant.CharacterStatus.STATUS_SINGING


@handle_state_machine.add_state_machine(constant.StateMachine.PLAY_INSTRUMENT)
def character_play_instrument(character_id: int):
    """
    角色演奏乐器
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.PLAY_INSTRUMENT
    character_data.behavior.duration = 30
    character_data.state = constant.CharacterStatus.STATUS_PLAY_INSTRUMENT


@handle_state_machine.add_state_machine(constant.StateMachine.ENTERTAIN_TRAINING)
def character_training(character_id: int):
    """
    角色战斗训练
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.TRAINING
    character_data.behavior.duration = 120
    character_data.state = constant.CharacterStatus.STATUS_TRAINING


@handle_state_machine.add_state_machine(constant.StateMachine.SINGING_RAND_CHARACTER)
def character_singing_to_rand_character(character_id: int):
    """
    唱歌给房间里随机角色听
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_list = list(
        cache.scene_data[
            map_handle.get_map_system_path_str_for_list(character_data.position)
        ].character_list
    )
    character_list.remove(character_id)
    if len(character_list):
        target_id = random.choice(character_list)
        character_data.behavior.behavior_id = constant.Behavior.SINGING
        character_data.behavior.duration = 10
        character_data.target_character_id = target_id
        character_data.state = constant.CharacterStatus.STATUS_SINGING


@handle_state_machine.add_state_machine(constant.StateMachine.PLAY_INSTRUMENT_RAND_CHARACTER)
def character_play_instrument_to_rand_character(character_id: int):
    """
    演奏乐器给房间里随机角色听
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_list = list(
        cache.scene_data[
            map_handle.get_map_system_path_str_for_list(character_data.position)
        ].character_list
    )
    character_list.remove(character_id)
    if len(character_list):
        target_id = random.choice(character_list)
        character_data.behavior.behavior_id = constant.Behavior.PLAY_INSTRUMENT
        character_data.behavior.duration = 30
        character_data.target_character_id = target_id
        character_data.state = constant.CharacterStatus.STATUS_PLAY_INSTRUMENT


@handle_state_machine.add_state_machine(constant.StateMachine.PEE)
def character_pee(character_id: int):
    """
    角色解手
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.PEE
    character_data.state = constant.CharacterStatus.STATUS_PEE
    character_data.behavior.duration = 5


@handle_state_machine.add_state_machine(constant.StateMachine.TAKE_SHOWER)
def character_take_shower(character_id: int):
    """
    角色淋浴
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.TAKE_SHOWER
    character_data.state = constant.CharacterStatus.STATUS_TAKE_SHOWER
    character_data.behavior.duration = 30


@handle_state_machine.add_state_machine(constant.StateMachine.WEAR_TO_LOCKER)
def character_wear_to_locker(character_id: int):
    """
    当前身上衣服转移到衣柜里
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.WEAR_TO_LOCKER
    character_data.state = constant.CharacterStatus.STATUS_WEAR_TO_LOCKER
    character_data.behavior.duration = 10
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "脱成全裸了"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.GET_SHOWER_CLOTH)
def character_get_shower_cloth(character_id: int):
    """
    角色换上浴帽和浴巾
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.PUT_SHOWER_CLOTH
    character_data.state = constant.CharacterStatus.STATUS_PUT_SHOWER_CLOTH
    character_data.behavior.duration = 10
    if character_data.position == cache.character_data[0].position:
        now_draw = draw.NormalDraw()
        now_draw.text = character_data.name + "换上了浴帽和浴巾"
        now_draw.draw()
        line_feed.draw()


@handle_state_machine.add_state_machine(constant.StateMachine.BUY_RAND_FOOD_AT_FOODSHOP)
def character_buy_rand_food_at_foodshop(character_id: int):
    """
    在取餐区购买随机食物
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    new_food_list = []
    for food_id in cache.restaurant_data:
        if not len(cache.restaurant_data[food_id]):
            continue
        for food_uid in cache.restaurant_data[food_id]:
            now_food: game_type.Food = cache.restaurant_data[food_id][food_uid]
            # if now_food.eat:
            new_food_list.append(food_id)
            break
    if not len(new_food_list):
        return
    now_food_id = random.choice(new_food_list)
    now_food = cache.restaurant_data[now_food_id][
        random.choice(list(cache.restaurant_data[now_food_id].keys()))
    ]
    character_data.food_bag[now_food.uid] = now_food
    del cache.restaurant_data[now_food_id][now_food.uid]

    # 记录食物名字
    food_recipe: game_type.Recipes = cache.recipe_data[now_food.recipe]
    food_name = food_recipe.name
    character_data.behavior.behavior_id = constant.Behavior.BUY_FOOD
    character_data.state = constant.CharacterStatus.STATUS_BUY_FOOD
    character_data.behavior.duration = 5
    character_data.behavior.food_name = food_name


@handle_state_machine.add_state_machine(constant.StateMachine.EAT_BAG_RAND_FOOD)
def character_eat_rand_food(character_id: int):
    """
    角色随机食用背包中的食物
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.EAT
    now_food_list = []
    for food_id in character_data.food_bag:
        # now_food: game_type.Food = character_data.food_bag[food_id]
        # if 27 in now_food.feel and now_food.eat:
        now_food_list.append(food_id)
    choice_food_id = random.choice(now_food_list)
    character_data.behavior.eat_food = character_data.food_bag[choice_food_id]
    character_data.state = constant.CharacterStatus.STATUS_EAT

    # 记录食物名字
    food_data: game_type.Food = character_data.food_bag[choice_food_id]
    food_recipe: game_type.Recipes = cache.recipe_data[food_data.recipe]
    food_name = food_recipe.name
    character_data.behavior.food_name = food_name
    character_data.behavior.duration = 30


@handle_state_machine.add_state_machine(constant.StateMachine.WORK_CURE_PATIENT)
def character_work_cure_patient(character_id: int):
    """
    角色工作：治疗病人
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.CURE_PATIENT
    character_data.behavior.duration = 30
    character_data.state = constant.CharacterStatus.STATUS_CURE_PATIENT


@handle_state_machine.add_state_machine(constant.StateMachine.WORK_RECRUIT)
def character_work_recruit(character_id: int):
    """
    角色工作：招募干员
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    character_data.target_character_id = character_id
    character_data.behavior.behavior_id = constant.Behavior.RECRUIT
    character_data.behavior.duration = 60
    character_data.state = constant.CharacterStatus.STATUS_RECRUIT


@handle_state_machine.add_state_machine(constant.StateMachine.ENTERTAIN_READ)
def character_entertain_read(character_id: int):
    """
    角色娱乐：读书
    Keyword arguments:
    character_id -- 角色id
    """
    character_data: game_type.Character = cache.character_data[character_id]
    # 检查是否要借书
    basement.check_random_borrow_book(character_id)

    for book_id_all in character_data.entertainment.borrow_book_id_set:
        book_id = book_id_all
    book_data = game_config.config_book[book_id]
    character_data.behavior.behavior_id = constant.Behavior.READ_BOOK
    character_data.state = constant.CharacterStatus.STATUS_READ_BOOK
    character_data.behavior.book_id = book_id
    character_data.behavior.book_name = book_data.name
    character_data.behavior.duration = 30


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_CLASS)
# def character_move_to_classroom(character_id: int):
#     """
#     移动至所属教室
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     _, _, move_path, move_time = character_move.character_move(
#         character_id,
#         map_handle.get_map_system_path_for_str(character_data.classroom),
#     )
#     character_data.behavior.behavior_id = constant.Behavior.MOVE
#     character_data.behavior.move_target = move_path
#     character_data.behavior.duration = move_time
#     character_data.state = constant.CharacterStatus.STATUS_MOVE


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_RAND_CAFETERIA)
# def character_move_to_rand_cafeteria(character_id: int):
#     """
#     移动至随机取餐区
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     to_cafeteria = map_handle.get_map_system_path_for_str(random.choice(constant.place_data["Cafeteria"]))
#     _, _, move_path, move_time = character_move.character_move(character_id, to_cafeteria)
#     character_data.behavior.behavior_id = constant.Behavior.MOVE
#     character_data.behavior.move_target = move_path
#     character_data.behavior.duration = move_time
#     character_data.state = constant.CharacterStatus.STATUS_MOVE



# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_RAND_RESTAURANT)
# def character_move_to_rand_restaurant(character_id: int):
#     """
#     设置角色状态为向随机就餐区移动
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     to_restaurant = map_handle.get_map_system_path_for_str(random.choice(constant.place_data["Restaurant"]))
#     _, _, move_path, move_time = character_move.character_move(
#         character_id,
#         to_restaurant,
#     )
#     character_data.behavior.behavior_id = constant.Behavior.MOVE
#     character_data.behavior.move_target = move_path
#     character_data.behavior.duration = move_time
#     character_data.state = constant.CharacterStatus.STATUS_MOVE



# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_UNDERWEAR)
# def character_wear_clean_underwear(character_id: int):
#     """
#     角色穿着干净的上衣
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 1 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[1]:
#             clothing_data: game_type.Clothing = character_data.clothing[1][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[1] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_UNDERPANTS)
# def character_wear_clean_underpants(character_id: int):
#     """
#     角色穿着干净的内裤
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 7 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[7]:
#             clothing_data: game_type.Clothing = character_data.clothing[7][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[7] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_BRA)
# def character_wear_clean_bra(character_id: int):
#     """
#     角色穿着干净的胸罩
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 6 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[6]:
#             clothing_data: game_type.Clothing = character_data.clothing[6][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[6] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_PANTS)
# def character_wear_clean_pants(character_id: int):
#     """
#     角色穿着干净的裤子
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 2 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[2]:
#             clothing_data: game_type.Clothing = character_data.clothing[2][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[2] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_SKIRT)
# def character_wear_clean_skirt(character_id: int):
#     """
#     角色穿着干净的短裙
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 3 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[3]:
#             clothing_data: game_type.Clothing = character_data.clothing[3][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[3] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_SHOES)
# def character_wear_clean_shoes(character_id: int):
#     """
#     角色穿着干净的鞋子
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 4 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[4]:
#             clothing_data: game_type.Clothing = character_data.clothing[4][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[4] = value_dict[now_value]


# @handle_state_machine.add_state_machine(constant.StateMachine.WEAR_CLEAN_SOCKS)
# def character_wear_clean_socks(character_id: int):
#     """
#     角色穿着干净的袜子
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     if 5 in character_data.clothing:
#         value_dict = {}
#         for clothing in character_data.clothing[5]:
#             clothing_data: game_type.Clothing = character_data.clothing[5][clothing]
#             value_dict[clothing_data.cleanliness] = clothing
#         now_value = max(value_dict.keys())
#         character_data.put_on[5] = value_dict[now_value]



# @handle_state_machine.add_state_machine(
#     constant.StateMachine.TOUCH_HEAD_TO_BEYOND_FRIENDSHIP_TARGET_IN_SCENE
# )
# def character_touch_head_to_beyond_friendship_target_in_scene(character_id: int):
#     """
#     对场景中抱有超越友谊想法的随机对象摸头
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
#     scene_data: game_type.Scene = cache.scene_data[scene_path_str]
#     character_list = []
#     for i in {3, 4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             if c in scene_data.character_list:
#                 character_list.append(c)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         character_data.behavior.behavior_id = constant.Behavior.TOUCH_HEAD
#         character_data.target_character_id = target_id
#         character_data.behavior.duration = 2
#         character_data.state = constant.CharacterStatus.STATUS_TOUCH_HEAD



# @handle_state_machine.add_state_machine(constant.StateMachine.EMBRACE_TO_BEYOND_FRIENDSHIP_TARGET_IN_SCENE)
# def character_embrace_to_beyond_friendship_target_in_scene(character_id: int):
#     """
#     对场景中抱有超越友谊想法的随机对象拥抱
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
#     scene_data: game_type.Scene = cache.scene_data[scene_path_str]
#     character_list = []
#     for i in {3, 4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             if c in scene_data.character_list:
#                 character_list.append(c)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         character_data.behavior.behavior_id = constant.Behavior.EMBRACE
#         character_data.target_character_id = target_id
#         character_data.behavior.duration = 3
#         character_data.state = constant.CharacterStatus.STATUS_EMBRACE


# @handle_state_machine.add_state_machine(constant.StateMachine.KISS_TO_LIKE_TARGET_IN_SCENE)
# def character_kiss_to_like_target_in_scene(character_id: int):
#     """
#     和场景中自己喜欢的随机对象接吻
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
#     scene_data: game_type.Scene = cache.scene_data[scene_path_str]
#     character_list = []
#     for i in {4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             if c in scene_data.character_list:
#                 character_list.append(c)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         character_data.behavior.behavior_id = constant.Behavior.KISS
#         character_data.target_character_id = target_id
#         character_data.behavior.duration = 2
#         character_data.state = constant.CharacterStatus.STATUS_KISS


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_LIKE_TARGET_SCENE)
# def character_move_to_like_target_scene(character_id: int):
#     """
#     移动至随机某个自己喜欢的人所在场景
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_list = []
#     for i in {4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             character_list.append(i)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         target_data: game_type.Character = cache.character_data[target_id]
#         _, _, move_path, move_time = character_move.character_move(character_id, target_data.position)
#         character_data.behavior.behavior_id = constant.Behavior.MOVE
#         character_data.behavior.move_target = move_path
#         character_data.behavior.duration = move_time
#         character_data.state = constant.CharacterStatus.STATUS_MOVE


# @handle_state_machine.add_state_machine(constant.StateMachine.HAND_IN_HAND_TO_LIKE_TARGET_IN_SCENE)
# def character_hand_in_hand_to_like_target_in_scene(character_id: int):
#     """
#     牵住场景中自己喜欢的随机对象的手
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
#     scene_data: game_type.Scene = cache.scene_data[scene_path_str]
#     character_list = []
#     for i in {4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             if c in scene_data.character_list:
#                 character_list.append(c)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         character_data.behavior.behavior_id = constant.Behavior.HAND_IN_HAND
#         character_data.target_character_id = target_id
#         character_data.behavior.duration = 10
#         character_data.state = constant.CharacterStatus.STATUS_HAND_IN_HAND


# @handle_state_machine.add_state_machine(constant.StateMachine.KISS_TO_NO_FIRST_KISS_TARGET_IN_SCENE)
# def character_kiss_to_no_first_kiss_like_target_in_scene(character_id: int):
#     """
#     和场景中自己喜欢的还是初吻的随机对象接吻
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
#     scene_data: game_type.Scene = cache.scene_data[scene_path_str]
#     character_list = []
#     for i in {4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             if c in scene_data.character_list:
#                 c_data: game_type.Character = cache.character_data[c]
#                 if c_data.first_kiss == -1:
#                     character_list.append(c)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         character_data.behavior.behavior_id = constant.Behavior.KISS
#         character_data.target_character_id = target_id
#         character_data.behavior.duration = 2
#         character_data.state = constant.CharacterStatus.STATUS_KISS


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_NO_FIRST_KISS_LIKE_TARGET_SCENE)
# def character_move_to_no_first_kiss_like_target_scene(character_id: int):
#     """
#     移动至随机某个自己喜欢的还是初吻的人所在场景
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_list = []
#     for i in {4, 5}:
#         character_data.social_contact.setdefault(i, set())
#         for c in character_data.social_contact[i]:
#             c_data: game_type.Character = cache.character_data[c]
#             if c_data.first_kiss == -1:
#                 character_list.append(i)
#     if len(character_list):
#         target_id = random.choice(character_list)
#         target_data: game_type.Character = cache.character_data[target_id]
#         _, _, move_path, move_time = character_move.character_move(character_id, target_data.position)
#         character_data.behavior.behavior_id = constant.Behavior.MOVE
#         character_data.behavior.move_target = move_path
#         character_data.behavior.duration = move_time
#         character_data.state = constant.CharacterStatus.STATUS_MOVE


# @handle_state_machine.add_state_machine(constant.StateMachine.BUY_RAND_DRINKS_AT_CAFETERIA)
# def character_buy_rand_drinks_at_restaurant(character_id: int):
#     """
#     在取餐区购买随机饮料
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     new_food_list = []
#     for food_id in cache.restaurant_data:
#         if not len(cache.restaurant_data[food_id]):
#             continue
#         for food_uid in cache.restaurant_data[food_id]:
#             now_food: game_type.Food = cache.restaurant_data[food_id][food_uid]
#             if now_food.eat and 28 in now_food.feel:
#                 new_food_list.append(food_id)
#             break
#     if not len(new_food_list):
#         return
#     now_food_id = random.choice(new_food_list)
#     now_food = cache.restaurant_data[now_food_id][
#         random.choice(list(cache.restaurant_data[now_food_id].keys()))
#     ]
#     character_data.food_bag[now_food.uid] = now_food
#     del cache.restaurant_data[now_food_id][now_food.uid]


# @handle_state_machine.add_state_machine(constant.StateMachine.DRINK_RAND_DRINKS)
# def character_drink_rand_drinks(character_id: int):
#     """
#     角色饮用背包内的随机饮料
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.behavior.behavior_id = constant.Behavior.EAT
#     drink_list = []
#     food_list = []
#     for food_id in character_data.food_bag:
#         now_food: game_type.Food = character_data.food_bag[food_id]
#         if 28 in now_food.feel and now_food.eat:
#             if 27 in now_food.feel and now_food.feel[27] > now_food.feel[28]:
#                 food_list.append(food_id)
#             else:
#                 drink_list.append(food_id)
#     if len(drink_list):
#         now_list = drink_list
#     else:
#         now_list = food_list
#     character_data.behavior.eat_food = character_data.food_bag[random.choice(now_list)]
#     character_data.behavior.duration = 1
#     character_data.state = constant.CharacterStatus.STATUS_EAT


# @handle_state_machine.add_state_machine(constant.StateMachine.ATTEND_CLASS)
# def character_attend_class(character_id: int):
#     """
#     角色在教室上课
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.behavior.behavior_id = constant.Behavior.ATTEND_CLASS
#     end_time = 0
#     school_id, phase = course.get_character_school_phase(character_id)
#     now_time_value = cache.game_time.hour * 100 + cache.game_time.minute
#     now_course_index = 0
#     for session_id in game_config.config_school_session_data[school_id]:
#         session_config = game_config.config_school_session[session_id]
#         if session_config.start_time <= now_time_value and session_config.end_time >= now_time_value:
#             now_value = int(now_time_value / 100) * 60 + now_time_value % 100
#             end_value = int(session_config.end_time / 100) * 60 + session_config.end_time % 100
#             end_time = end_value - now_value + 1
#             now_course_index = session_config.session
#             break
#     now_week = cache.game_time.weekday()
#     if not now_course_index:
#         now_course = random.choice(list(game_config.config_school_phase_course_data[school_id][phase]))
#     else:
#         now_course = cache.course_time_table_data[school_id][phase][now_week][now_course_index]
#     character_data.behavior.duration = end_time
#     character_data.behavior.behavior_id = constant.Behavior.ATTEND_CLASS
#     character_data.state = constant.CharacterStatus.STATUS_ATTEND_CLASS
#     character_data.behavior.course_id = now_course


# @handle_state_machine.add_state_machine(constant.StateMachine.TEACH_A_LESSON)
# def character_teach_lesson(character_id: int):
#     """
#     角色在教室教课
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.behavior.behavior_id = constant.Behavior.TEACHING
#     end_time = 0
#     now_week = cache.game_time.weekday()
#     now_time_value = cache.game_time.hour * 100 + cache.game_time.minute
#     timetable_list: List[game_type.TeacherTimeTable] = cache.teacher_school_timetable[character_id]
#     course = 0
#     end_time = 0
#     for timetable in timetable_list:
#         if timetable.week_day != now_week:
#             continue
#         if timetable.time <= now_time_value and timetable.end_time <= now_time_value:
#             now_value = int(now_time_value / 100) * 60 + now_time_value % 100
#             end_value = int(timetable.end_time / 100) * 60 + timetable.end_time % 100
#             end_time = end_value - now_value + 1
#             course = timetable.course
#             break
#     character_data.behavior.duration = end_time
#     character_data.behavior.behavior_id = constant.Behavior.TEACHING
#     character_data.state = constant.CharacterStatus.STATUS_TEACHING
#     character_data.behavior.course_id = course


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_GROVE)
# def character_move_to_grove(character_id: int):
#     """
#     移动至加工站入口场景
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     _, _, move_path, move_time = character_move.character_move(character_id, ["7"])
#     character_data.behavior.behavior_id = constant.Behavior.MOVE
#     character_data.behavior.move_target = move_path
#     character_data.behavior.duration = move_time
#     character_data.state = constant.CharacterStatus.STATUS_MOVE


# @handle_state_machine.add_state_machine(constant.StateMachine.MOVE_TO_ITEM_SHOP)
# def character_move_to_item_shop(character_id: int):
#     """
#     移动至训练场入口场景
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     _, _, move_path, move_time = character_move.character_move(character_id, ["11"])
#     character_data.behavior.behavior_id = constant.Behavior.MOVE
#     character_data.behavior.move_target = move_path
#     character_data.behavior.duration = move_time
#     character_data.state = constant.CharacterStatus.STATUS_MOVE


# @handle_state_machine.add_state_machine(constant.StateMachine.BUY_GUITAR)
# def character_buy_guitar(character_id: int):
#     """
#     购买吉他
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.item.add(4)


# @handle_state_machine.add_state_machine(constant.StateMachine.PLAY_GUITAR)
# def character_play_guitar(character_id: int):
#     """
#     弹吉他
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.behavior.behavior_id = constant.Behavior.PLAY_GUITAR
#     character_data.behavior.duration = 10
#     character_data.state = constant.CharacterStatus.STATUS_PLAY_GUITAR


# @handle_state_machine.add_state_machine(constant.StateMachine.SELF_STUDY)
# def character_self_study(character_id: int):
#     """
#     角色在自习
#     Keyword arguments:
#     character_id -- 角色id
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     character_data.behavior.behavior_id = constant.Behavior.SELF_STUDY
#     school_id, phase = course.get_character_school_phase(character_id)
#     now_course_list = list(game_config.config_school_phase_course_data[school_id][phase])
#     now_course_id = random.choice(now_course_list)
#     character_data.behavior.duration = 10
#     character_data.behavior.course_id = now_course_id
#     character_data.state = constant.CharacterStatus.STATUS_SELF_STUDY

