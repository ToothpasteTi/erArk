import math
import datetime
from typing import List
from uuid import UUID
from functools import wraps
from types import FunctionType
from Script.Core import cache_control, constant, constant_promise, game_type
from Script.Design import map_handle, game_time, attr_calculation, character
from Script.Config import game_config

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """


def add_premise(premise: str) -> FunctionType:
    """
    添加前提
    Keyword arguments:
    premise -- 前提id
    Return arguments:
    FunctionType -- 前提处理函数对象
    """

    def decoraror(func):
        @wraps(func)
        def return_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        constant.handle_premise_data[premise] = return_wrapper
        return return_wrapper

    return decoraror


def handle_premise(premise: str, character_id: int) -> int:
    """
    调用前提id对应的前提处理函数
    Keyword arguments:
    premise -- 前提id
    character_id -- 角色id
    Return arguments:
    int -- 前提权重加成
    """
    if premise in constant.handle_premise_data:
        return constant.handle_premise_data[premise](character_id)
    else:
        return 0


@add_premise(constant_promise.Premise.EAT_TIME)
def handle_eat_time(character_id: int) -> int:
    """
    校验当前时间是否处于饭点（早上7~8点、中午12~13点、晚上17~18点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_time = game_time.get_sun_time(character_data.behavior.start_time)
    # return (now_time == 4) * 100
    # print(f"debug start_time = {character_data.behavior.start_time}，now_time = {now_time}")
    if character_data.behavior.start_time.hour in {7,8,12,13,17,18}:
        # print(f"debug 当前为饭点={character_data.behavior.start_time.hour}")
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOWER_TIME)
def handle_shower_time(character_id: int) -> int:
    """
    淋浴时间（晚上9点到晚上12点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.behavior.start_time.hour in {21,22,23}:
        now_hour = character_data.behavior.start_time.hour
        return (now_hour-20) *200
    return 0


@add_premise(constant_promise.Premise.SLEEP_TIME)
def handle_sleep_time(character_id: int) -> int:
    """
    睡觉时间（晚上10点到早上6点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_time = game_time.get_sun_time(character_data.behavior.start_time)
    # return (now_time == 4) * 100
    if character_data.behavior.start_time.hour in {0,1,2,3,4,5,22,23}:
        now_hour = character_data.behavior.start_time.hour if character_data.behavior.start_time.hour>20 else character_data.behavior.start_time.hour+24
        return (now_hour-21) *100
    return 0


@add_premise(constant_promise.Premise.SLEEP_GE_75_OR_SLEEP_TIME)
def handle_sleep_ge_75_or_sleep_time(character_id: int) -> int:
    """
    困倦条≥75%或到了睡觉的时间
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    # now_time = game_time.get_sun_time(character_data.behavior.start_time)
    # return (now_time == 4) * 100
    if character_data.behavior.start_time != None:
        if character_data.behavior.start_time.hour in {0,1,2,3,4,5,22,23}:
            now_hour = character_data.behavior.start_time.hour if character_data.behavior.start_time.hour>20 else character_data.behavior.start_time.hour+24
            return (now_hour-21) *100
    value = character_data.sleep_point / 160
    if value > 0.74:
        return 1
    return 0


@add_premise(constant_promise.Premise.WORK_TIME)
def handle_work_time(character_id: int) -> int:
    """
    工作时间（早上9:00~下午4:59）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_time = game_time.get_sun_time(character_data.behavior.start_time)
    # return (now_time == 4) * 100
    if character_data.behavior.start_time.hour >= 9 and character_data.behavior.start_time.hour < 17:
        return 50
    return 0


@add_premise(constant_promise.Premise.HAVE_FOOD)
def handle_have_food(character_id: int) -> int:
    """
    校验角色是否拥有食物
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    food_index = 0
    for food_id in character_data.food_bag:
        if character_data.food_bag[food_id]:
            food_index += 1
    return food_index


@add_premise(constant_promise.Premise.NOT_HAVE_FOOD)
def handle_not_have_food(character_id: int) -> int:
    """
    校验角色是否没有食物
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    food_index = 1
    for food_id in character_data.food_bag:
        if character_data.food_bag[food_id]:
            return 0
    return food_index


@add_premise(constant_promise.Premise.HAVE_TARGET)
def handle_have_target(character_id: int) -> int:
    """
    校验角色是否有交互对象
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.target_character_id == character_id:
        return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_NO_PLAYER)
def handle_target_no_player(character_id: int) -> int:
    """
    校验角色目标对像是否不是玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.target_character_id > 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.PLACE_EXPOSED)
def handle_place_exposed(character_id: int) -> int:
    """
    校验角色当前地点暴露
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if now_scene_data.exposed:
        return 1
    return 0


@add_premise(constant_promise.Premise.PLACE_COVERT)
def handle_place_covert(character_id: int) -> int:
    """
    校验角色当前地点隐蔽
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if now_scene_data.exposed:
        return 0
    return 1


@add_premise(constant_promise.Premise.PLACE_HAVE_FURNITURE)
def handle_place_have_furniture(character_id: int) -> int:
    """
    校验角色当前地点有家具
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if now_scene_data.have_furniture:
        return 1
    return 0


@add_premise(constant_promise.Premise.PLACE_NOT_FURNITURE)
def handle_place_not_furniture(character_id: int) -> int:
    """
    校验角色当前地点没家具
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if now_scene_data.have_furniture:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_KITCHEN)
def handle_in_kitchen(character_id: int) -> int:
    """
    校验角色是否在厨房中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if  "Kitchen" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_DINING_HALL)
def handle_in_dining_hall(character_id: int) -> int:
    """
    校验角色是否在食堂中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Dining_hall" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_DINING_HALL)
def handle_not_in_dining_hall(character_id: int) -> int:
    """
    校验角色是否不在食堂中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Dining_hall" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_FOOD_SHOP)
def handle_in_food_shop(character_id: int) -> int:
    """
    校验角色是否在食物商店（取餐区）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Food_Shop" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_FOOD_SHOP)
def handle_not_in_food_shop(character_id: int) -> int:
    """
    校验角色是否不在食物商店（取餐区）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Food_Shop" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_DR_OFFICE)
def handle_in_dr_office(character_id: int) -> int:
    """
    校验角色是否在博士办公室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Dr_office" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_DR_OFFICE)
def handle_not_in_dr_office(character_id: int) -> int:
    """
    校验角色是否不在博士办公室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Dr_office" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_DR_OFFICE_OR_DEBUG)
def handle_in_dr_office_or_debug(character_id: int) -> int:
    """
    校验角色是否在博士办公室中或处于debug模式
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Dr_office" in now_scene_data.scene_tag or cache.debug_mode:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_COMMAND_ROOM)
def handle_in_command_room(character_id: int) -> int:
    """
    校验角色是否在指挥室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Command_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_DORMITORY)
def handle_in_dormitory(character_id: int) -> int:
    """
    校验角色是否在自己宿舍中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_position = map_handle.get_map_system_path_str_for_list(character_data.position)
    return now_position == character_data.dormitory


@add_premise(constant_promise.Premise.NOT_IN_DORMITORY)
def handle_not_in_dormitory(character_id: int) -> int:
    """
    校验角色是否不在自己宿舍中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    now_position = map_handle.get_map_system_path_str_for_list(character_data.position)
    return now_position != character_data.dormitory


@add_premise(constant_promise.Premise.IN_BATHROOM)
def handle_in_bathroom(character_id: int) -> int:
    """
    校验角色是否在浴室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Bathroom" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_TOILET_MAN)
def handle_in_toilet_man(character_id: int) -> int:
    """
    校验角色是否在男士洗手间
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Toilet_Male" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_TOILET_FEMALE)
def handle_in_toilet_female(character_id: int) -> int:
    """
    校验角色是否在女士洗手间
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Toilet_Female" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.MOVE_TO_TOILET_FEMALE)
def handle_move_to_toilet_female(character_id: int) -> int:
    """
    校验角色抵达女士洗手间
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if (
        character_data.behavior.move_target == character_data.position
        and "Toilet_Female" in now_scene_data.scene_tag
    ):
        return 1
    return 0


@add_premise(constant_promise.Premise.MOVE_TO_LOCKER_ROOM)
def handle_move_to_locker_room(character_id: int) -> int:
    """
    角色抵达更衣室
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if (
        character_data.behavior.move_target == character_data.position
        and "Locker_Room" in now_scene_data.scene_tag
    ):
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_TOILET)
def handle_not_in_toilet(character_id: int) -> int:
    """
    校验角色是否不在洗手间
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Toilet_Male" in now_scene_data.scene_tag:
        return 0
    if "Toilet_Female" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_REST_ROOM)
def handle_in_rest_room(character_id: int) -> int:
    """
    校验角色是否在休息室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Rest_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_REST_ROOM)
def handle_not_in_rest_room(character_id: int) -> int:
    """
    校验角色是否不在休息室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Rest_Room" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_MUSIC_ROOM)
def handle_in_music_room(character_id: int) -> int:
    """
    校验角色是否在音乐室中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Modern_Musicroom" in now_scene_data.scene_tag:
        return 1
    if "Classic_Musicroom" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_COLLECTION_ROOM)
def handle_in_collection_room(character_id: int) -> int:
    """
    校验角色是否在藏品馆中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Collection" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_GYM_ROOM)
def handle_in_gym_room(character_id: int) -> int:
    """
    校验角色是否在健身区中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Gym" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_TRAINING_ROOM)
def handle_in_training_room(character_id: int) -> int:
    """
    校验角色是否在训练室中（包括木桩房和射击房）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Training_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_TRAINING_ROOM)
def handle_not_in_training_room(character_id: int) -> int:
    """
    校验角色是否不在训练室中（包括木桩房和射击房）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Training_Room" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_FIGHT_ROOM)
def handle_in_fight_room(character_id: int) -> int:
    """
    校验角色是否在木桩房中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Fight_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_SHOOT_ROOM)
def handle_in_shoot_room(character_id: int) -> int:
    """
    校验角色是否在射击房中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Shoot_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_BUILDING_ROOM)
def handle_in_building_room(character_id: int) -> int:
    """
    校验角色是否在基建部中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Building_Room" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_CLINIC)
def handle_in_clinic(character_id: int) -> int:
    """
    校验角色是否在门诊室中（含急诊室）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Clinic" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_CLINIC)
def handle_not_in_clinic(character_id: int) -> int:
    """
    校验角色是否不在门诊室中（含急诊室）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Clinic" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.IN_BATHZONE_LOCKER_ROOM)
def handle_in_bathzone_locker_room(character_id: int) -> int:
    """
    校验角色是否在大浴场的更衣室
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Locker_Room" in now_scene_data.scene_tag and "大浴场" in now_scene_str:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_BATHZONE_LOCKER_ROOM)
def handle_not_in_bathzone_locker_room(character_id: int) -> int:
    """
    校验角色是否不在大浴场的更衣室
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Locker_Room" in now_scene_data.scene_tag and "大浴场" in now_scene_str:
        return 0
    return 1


@add_premise(constant_promise.Premise.PLACE_DOOR_OPEN)
def handle_place_door_open(character_id: int) -> int:
    """
    地点的门是开着的（不含内隔间关门）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if now_scene_data.close_flag == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.PLACE_LADIES_ONLY)
def handle_place_ladies_only(character_id: int) -> int:
    """
    该地点男士止步（女洗手间/更衣室/浴室等）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Ladies_Only" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_BATHROOM)
def handle_in_bathroom(character_id: int) -> int:
    """
    校验角色是否在淋浴区
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Bathroom" in now_scene_data.scene_tag:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_BATHROOM)
def handle_not_in_bathroom(character_id: int) -> int:
    """
    校验角色是否不在淋浴区
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_position = character_data.position
    now_scene_str = map_handle.get_map_system_path_str_for_list(now_position)
    now_scene_data = cache.scene_data[now_scene_str]
    if "Bathroom" in now_scene_data.scene_tag:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_MOVED)
def handle_have_moved(character_id: int) -> int:
    """
    NPC距离上次移动已经至少经过了1小时
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    move_flag = 0
    #同一天内过1小时则判定为1
    if now_time.day == character_data.action_info.last_move_time.day and now_time.hour > character_data.action_info.last_move_time.hour:
        character_data.action_info.last_move_time = now_time
        # print("过一小时判定,character_id :",character_id)
        move_flag = 1
    #非同一天也判定为1
    elif now_time.day != character_data.action_info.last_move_time.day:
        character_data.action_info.last_move_time = now_time
        move_flag = 1
        # print("非同一天判定")
    return move_flag


@add_premise(constant_promise.Premise.AI_WAIT)
def handle_ai_wait(character_id: int) -> int:
    """
    NPC需要进行一次5分钟的等待（wait_flag = 1)
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.wait_flag:
        # print("判断到需要进行等待，character_id = ",character_id)
        return 999
    else:
        return 0


@add_premise(constant_promise.Premise.HAVE_TRAINED)
def handle_have_trained(character_id: int) -> int:
    """
    NPC距离上次战斗训练已经超过两天了
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time = cache.game_time
    train_time = character_data.action_info.last_training_time
    add_day = int((now_time - train_time).days)
    if add_day >= 2:
        return (add_day - 1)*10
    return 0


@add_premise(constant_promise.Premise.NOT_SHOWER)
def handle_not_shower(character_id: int) -> int:
    """
    NPC今天还没有洗澡
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time = cache.game_time
    shower_time = character_data.action_info.last_shower_time
    if shower_time.day == now_time.day:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_SHOWERED)
def handle_have_showered(character_id: int) -> int:
    """
    NPC今天已经洗过澡了
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time = cache.game_time
    shower_time = character_data.action_info.last_shower_time
    if shower_time.day == now_time.day:
        return 1
    return 0


@add_premise(constant_promise.Premise.IS_MAN)
def handle_is_man(character_id: int) -> int:
    """
    校验角色是否是男性
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if not character_data.sex:
        return 1
    return 0


@add_premise(constant_promise.Premise.IS_WOMAN)
def handle_is_woman(character_id: int) -> int:
    """
    校验角色是否是女性
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.sex == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.HIGH_1)
def handle_high_1(character_id: int) -> int:
    """
    优先度为1的空白前提
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 1


@add_premise(constant_promise.Premise.HIGH_2)
def handle_high_2(character_id: int) -> int:
    """
    优先度为2的空白前提
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 2


@add_premise(constant_promise.Premise.HIGH_5)
def handle_high_5(character_id: int) -> int:
    """
    优先度为5的空白前提
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 5


@add_premise(constant_promise.Premise.HIGH_10)
def handle_high_10(character_id: int) -> int:
    """
    优先度为10的空白前提
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 10


@add_premise(constant_promise.Premise.HIGH_999)
def handle_high_999(character_id: int) -> int:
    """
    优先度为999的空白前提
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 999


@add_premise(constant_promise.Premise.INSTRUCT_JUDGE_LOW_OBSCENITY)
def handle_instruct_judge_low_obscenity(character_id: int) -> int:
    """
    当前实行值足以轻度性骚扰
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.target_character_id:
        if character.calculation_instuct_judege(0,character_data.target_character_id,"初级骚扰"):
            return 1
    return 0


@add_premise(constant_promise.Premise.INSTRUCT_JUDGE_HIGH_OBSCENITY)
def handle_instruct_judge_high_obscenity(character_id: int) -> int:
    """
    当前实行值足以重度性骚扰
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.target_character_id:
        if character.calculation_instuct_judege(0,character_data.target_character_id,"严重骚扰"):
            return 1
    return 0


@add_premise(constant_promise.Premise.INSTRUCT_JUDGE_H)
def handle_instruct_judge_h(character_id: int) -> int:
    """
    当前实行值足以H
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.target_character_id:
        if character.calculation_instuct_judege(0,character_data.target_character_id,"H模式"):
            return 1
    return 0


@add_premise(constant_promise.Premise.HP_1)
def handle_hp_1(character_id: int) -> int:
    """
    自身疲劳（体力=1）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.tired == 1:
        return 999
    else:
        return 0


@add_premise(constant_promise.Premise.HP_LOW)
def handle_hp_low(character_id: int) -> int:
    """
    角色体力低于30%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    value = character_data.hit_point / character_data.hit_point_max
    if value < 0.3:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.HP_HIGH)
def handle_hp_high(character_id: int) -> int:
    """
    角色体力高于70%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    value = character_data.hit_point / character_data.hit_point_max
    if value > 0.7:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.MP_0)
def handle_mp_0(character_id: int) -> int:
    """
    角色气力为0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    value = character_data.mana_point
    if value == 0:
        return character_data.hit_point_max - character_data.hit_point
    else:
        return 0

@add_premise(constant_promise.Premise.MP_LOW)
def handle_mp_low(character_id: int) -> int:
    """
    角色气力低于30%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    value = character_data.mana_point / character_data.mana_point_max
    if value < 0.3:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.MP_HIGH)
def handle_mp_high(character_id: int) -> int:
    """
    角色气力高于70%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    value = character_data.mana_point / character_data.mana_point_max
    if value > 0.7:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_HP_LOW)
def handle_target_hp_low(character_id: int) -> int:
    """
    交互对象体力低于30%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.hit_point / target_data.hit_point_max
    if value < 0.3:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_HP_HIGH)
def handle_target_hp_high(character_id: int) -> int:
    """
    交互对象体力高于70%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.hit_point / target_data.hit_point_max
    if value > 0.7:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_MP_0)
def handle_target_mp_0(character_id: int) -> int:
    """
    交互对象气力为0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.mana_point
    if value == 0:
        return 1
    else:
        return 0

@add_premise(constant_promise.Premise.TARGET_MP_LOW)
def handle_target_mp_low(character_id: int) -> int:
    """
    交互对象气力低于30%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.mana_point / target_data.mana_point_max
    if value < 0.3:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_MP_HIGH)
def handle_target_mp_high(character_id: int) -> int:
    """
    交互对象气力高于70%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.mana_point / target_data.mana_point_max
    if value > 0.7:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_GE_50)
def handle_sleep_ge_50(character_id: int) -> int:
    """
    困倦条≥50%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value >= 0.5:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_LE_74)
def handle_sleep_le_74(character_id: int) -> int:
    """
    困倦条≤74%，全指令自由
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value <= 0.74:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_GE_75)
def handle_sleep_ge_75(character_id: int) -> int:
    """
    困倦条≥75%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value > 0.74:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_LE_89)
def handle_sleep_le_89(character_id: int) -> int:
    """
    困倦条≤89%，自由活动的极限
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value <= 0.89:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_GE_90)
def handle_sleep_ge_90(character_id: int) -> int:
    """
    困倦条≥90%
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value > 0.89:
        return character_data.sleep_point * 5
    else:
        return 0


@add_premise(constant_promise.Premise.SLEEP_100)
def handle_sleep_100(character_id: int) -> int:
    """
    困倦条100%，当场爆睡
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.sleep_point / 160
    if value >= 1:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_GOOD_MOOD)
def handle_target_good_mood(character_id: int) -> int:
    """
    交互对象心情愉快
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.angry_point
    if value <= 5:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_NORMAL_MOOD)
def handle_target_normal_mood(character_id: int) -> int:
    """
    交互对象心情普通
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.angry_point
    if 5 < value and value <= 30:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_BAD_MOOD)
def handle_target_bad_mood(character_id: int) -> int:
    """
    交互对象心情不好
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.angry_point
    if 30 < value and value <=50:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_ANGRY_MOOD)
def handle_target_angry_mood(character_id: int) -> int:
    """
    交互对象心情愤怒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.angry_point
    if value > 50:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_ABD_OR_ANGRY_MOOD)
def handle_bad_or_angry_mood(character_id: int) -> int:
    """
    交互对象心情不好或愤怒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    value = target_data.angry_point
    if value > 30:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_ANGRY_WITH_PLAYER)
def handle_target_angry_with_player(character_id: int) -> int:
    """
    交互对象被玩家惹火了
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.angry_with_player:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_NOT_ANGRY_WITH_PLAYER)
def handle_target_not_angry_with_player(character_id: int) -> int:
    """
    交互对象没有被玩家惹火
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.angry_with_player:
        return 0
    else:
        return 1


@add_premise(constant_promise.Premise.COLLECT_BONUS_103)
def handle_collect_bonus_103(character_id: int) -> int:
    """
    校验收藏奖励_103_解锁索要内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[0]
    if character_data.pl_collection.collection_bonus[103]:
        return 1
    return 0


@add_premise(constant_promise.Premise.COLLECT_BONUS_203)
def handle_collect_bonus_203(character_id: int) -> int:
    """
    校验收藏奖励_203_解锁索要袜子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[0]
    if character_data.pl_collection.collection_bonus[203]:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_1)
def handle_cook_1(character_id: int) -> int:
    """
    校验角色是否料理技能==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_2)
def handle_cook_2(character_id: int) -> int:
    """
    校验角色是否料理技能==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_3)
def handle_cook_3(character_id: int) -> int:
    """
    校验角色是否料理技能==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_4)
def handle_cook_4(character_id: int) -> int:
    """
    校验角色是否料理技能==4
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_LE_1)
def handle_cook_le_1(character_id: int) -> int:
    """
    校验角色是否料理技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_GE_3)
def handle_cook_ge_3(character_id: int) -> int:
    """
    校验角色是否料理技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.COOK_GE_5)
def handle_cook_ge_3(character_id: int) -> int:
    """
    校验角色是否料理技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[43] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_1)
def handle_music_1(character_id: int) -> int:
    """
    校验角色是否音乐技能==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_2)
def handle_music_2(character_id: int) -> int:
    """
    校验角色是否音乐技能==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_3)
def handle_music_3(character_id: int) -> int:
    """
    校验角色是否音乐技能==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_4)
def handle_music_4(character_id: int) -> int:
    """
    校验角色是否音乐技能==4
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_LE_1)
def handle_music_le_1(character_id: int) -> int:
    """
    校验角色是否音乐技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_GE_3)
def handle_music_ge_3(character_id: int) -> int:
    """
    校验角色是否音乐技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.MUSIC_GE_5)
def handle_music_ge_3(character_id: int) -> int:
    """
    校验角色是否音乐技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[44] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.TECHNIQUE_GE_3)
def handle_technique_ge_3(character_id: int) -> int:
    """
    校验角色是否技巧技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[19] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TECHNIQUE_GE_5)
def handle_technique_ge_3(character_id: int) -> int:
    """
    校验角色是否技巧技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[19] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_DESIRE_GE_5)
def handle_target_desire_ge_5(character_id: int) -> int:
    """
    校验交互对象是否欲望技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[22] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_DESIRE_GE_7)
def handle_target_desire_ge_7(character_id: int) -> int:
    """
    校验交互对象是否欲望技能>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[22] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.TALK_LE_1)
def handle_talk_le_1(character_id: int) -> int:
    """
    校验角色是否话术技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[40] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TALK_GE_3)
def handle_talk_ge_3(character_id: int) -> int:
    """
    校验角色是否话术技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[40] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TALK_GE_5)
def handle_talk_ge_5(character_id: int) -> int:
    """
    校验角色是否话术技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[40] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TALK_LE_1)
def handle_t_talk_le_1(character_id: int) -> int:
    """
    校验交互对象是否话术技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[40] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TALK_GE_3)
def handle_t_talk_ge_3(character_id: int) -> int:
    """
    校验交互对象是否话术技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[40] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TALK_GE_5)
def handle_t_talk_ge_5(character_id: int) -> int:
    """
    校验交互对象是否话术技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[40] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_1)
def handle_target_cook_1(character_id: int) -> int:
    """
    校验交互对象是否料理技能==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_2)
def handle_target_cook_2(character_id: int) -> int:
    """
    校验交互对象是否料理技能==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_3)
def handle_target_cook_3(character_id: int) -> int:
    """
    校验交互对象是否料理技能==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_4)
def handle_target_cook_4(character_id: int) -> int:
    """
    校验交互对象是否料理技能==4
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_LE_1)
def handle_target_cook_le_1(character_id: int) -> int:
    """
    校验交互对象是否料理技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_LE_3)
def handle_target_cook_le_3(character_id: int) -> int:
    """
    校验交互对象是否料理技能<=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] <= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_GE_3)
def handle_target_cook_ge_3(character_id: int) -> int:
    """
    校验交互对象是否料理技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_G_3)
def handle_target_cook_g_3(character_id: int) -> int:
    """
    校验交互对象是否料理技能>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_COOK_GE_5)
def handle_target_cook_ge_3(character_id: int) -> int:
    """
    校验交互对象是否料理技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[28] >= 5:
        return 1
    return 0



@add_premise(constant_promise.Premise.TARGET_MUSIC_1)
def handle_target_music_1(character_id: int) -> int:
    """
    校验交互对象是否音乐技能==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_2)
def handle_target_music_2(character_id: int) -> int:
    """
    校验交互对象是否音乐技能==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_3)
def handle_target_music_3(character_id: int) -> int:
    """
    校验交互对象是否音乐技能==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_4)
def handle_target_music_4(character_id: int) -> int:
    """
    校验交互对象是否音乐技能==4
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_LE_1)
def handle_target_music_le_1(character_id: int) -> int:
    """
    校验交互对象是否音乐技能<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_GE_3)
def handle_target_music_ge_3(character_id: int) -> int:
    """
    校验交互对象是否音乐技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_MUSIC_GE_5)
def handle_target_music_ge_3(character_id: int) -> int:
    """
    校验交互对象是否音乐技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[29] >= 5:
        return 1
    return 0

@add_premise(constant_promise.Premise.TARGET_INTIMACY_8)
def handle_target_intimacy_8(character_id: int) -> int:
    """
    校验交互对象是否亲密==8
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[21] == 8:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_INTIMACY_LE_1)
def handle_target_intimacy_le_1(character_id: int) -> int:
    """
    校验交互对象是否亲密<=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[21] <= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_INTIMACY_GE_3)
def handle_target_intimacy_ge_3(character_id: int) -> int:
    """
    校验交互对象是否亲密>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[21] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_INTIMACY_GE_5)
def handle_target_intimacy_ge_3(character_id: int) -> int:
    """
    校验交互对象是否亲密>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[21] >= 5:
        return 1
    return 0



@add_premise(constant_promise.Premise.TARGET_TECHNIQUE_GE_3)
def handle_t_technique_ge_3(character_id: int) -> int:
    """
    校验交互对象是否技巧技能>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[19] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_TECHNIQUE_GE_5)
def handle_t_technique_ge_3(character_id: int) -> int:
    """
    校验交互对象是否技巧技能>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[19] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_YIELD_MARK_1)
def handle_t_yield_mark_1(character_id: int) -> int:
    """
    校验交互对象是否屈服刻印==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[14] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_YIELD_MARK_2)
def handle_t_yield_mark_2(character_id: int) -> int:
    """
    校验交互对象是否屈服刻印==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[14] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_YIELD_MARK_3)
def handle_t_yield_mark_3(character_id: int) -> int:
    """
    校验交互对象是否屈服刻印==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[14] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_YIELD_MARK_GE_1)
def handle_t_yield_mark_ge_1(character_id: int) -> int:
    """
    校验交互对象是否屈服刻印>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[14] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_YIELD_MARK_LE_2)
def handle_t_yield_mark_le_2(character_id: int) -> int:
    """
    校验交互对象是否屈服刻印<=2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[14] <= 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_GE_1)
def handle_t_finger_tec_ge_1(character_id: int) -> int:
    """
    校验交互对象是否指技>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_GE_3)
def handle_t_finger_tec_ge_3(character_id: int) -> int:
    """
    校验交互对象是否指技>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_GE_5)
def handle_t_finger_tec_ge_5(character_id: int) -> int:
    """
    校验交互对象是否指技>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_GE_7)
def handle_t_finger_tec_ge_7(character_id: int) -> int:
    """
    校验交互对象是否指技>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_0)
def handle_t_finger_tec_0(character_id: int) -> int:
    """
    校验交互对象是否指技==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_FINGER_TEC_L_3)
def handle_t_finger_tec_l_3(character_id: int) -> int:
    """
    校验交互对象是否指技<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[70] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.KISS_0)
def handle_kiss_0(character_id: int) -> int:
    """
    校验自身亲吻经验==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.experience[40] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.KISS_GE_10)
def handle_kiss_ge_10(character_id: int) -> int:
    """
    校验自身亲吻经验>=10
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.experience[40] >= 10:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_KISS_0)
def handle_t_kiss_0(character_id: int) -> int:
    """
    校验交互对象亲吻经验==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.experience[40] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_KISS_GE_10)
def handle_t_kiss_ge_10(character_id: int) -> int:
    """
    校验交互对象亲吻经验>=10
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.experience[40] >= 10:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_FALL)
def handle_target_not_fall(character_id: int) -> int:
    """
    角色无陷落素质
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {10,11,12,13,15,16,17,18}:
        if target_data.talent[i]:
            return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_LOVE_1)
def handle_target_love_1(character_id: int) -> int:
    """
    校验交互对象是否是思慕,爱情系第一阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[10]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_2)
def handle_target_love_2(character_id: int) -> int:
    """
    校验交互对象是否是恋慕,爱情系第二阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[11]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_3)
def handle_target_love_3(character_id: int) -> int:
    """
    校验交互对象是否是恋人,爱情系第三阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[12]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_4)
def handle_target_love_4(character_id: int) -> int:
    """
    校验交互对象是否是爱侣,爱情系第四阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[13]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_GE_1)
def handle_target_love_ge_1(character_id: int) -> int:
    """
    交互对象爱情系>=思慕
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {10,11,12,13}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_GE_2)
def handle_target_love_ge_2(character_id: int) -> int:
    """
    交互对象爱情系>=恋慕
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {11,12,13}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_GE_3)
def handle_target_love_ge_3(character_id: int) -> int:
    """
    交互对象爱情系>=恋人
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {12,13}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_LOVE_LE_2)
def handle_target_love_le_2(character_id: int) -> int:
    """
    交互对象爱情系<=恋慕
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {12,13}:
        if target_data.talent[i]:
            return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_OBEY_1)
def handle_target_obey_1(character_id: int) -> int:
    """
    校验交互对象是否是屈从,隶属系第一阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[15]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_2)
def handle_target_obey_2(character_id: int) -> int:
    """
    校验交互对象是否是驯服,隶属系第二阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[16]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_3)
def handle_target_obey_3(character_id: int) -> int:
    """
    校验交互对象是否是宠物,隶属系第三阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[17]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_4)
def handle_target_obey_4(character_id: int) -> int:
    """
    校验交互对象是否是奴隶,隶属系第四阶段
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[18]:
        return 1
    return 0

@add_premise(constant_promise.Premise.TARGET_OBEY_GE_1)
def handle_target_obey_ge_1(character_id: int) -> int:
    """
    交互对象隶属系>=屈从
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {15,16,17,18}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_GE_2)
def handle_target_obey_ge_2(character_id: int) -> int:
    """
    交互对象隶属系>=驯服
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {16,17,18}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_GE_3)
def handle_target_obey_ge_3(character_id: int) -> int:
    """
    交互对象隶属系>=宠物
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {17,18}:
        if target_data.talent[i]:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_OBEY_LE_2)
def handle_target_obey_le_2(character_id: int) -> int:
    """
    交互对象隶属系<=驯服
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for i in {17,18}:
        if target_data.talent[i]:
            return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_FIRST_KISS)
def handle_have_first_kiss(character_id: int) -> int:
    """
    玩家保有初吻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[4]:
        return 1
    return 0


@add_premise(constant_promise.Premise.NO_FIRST_KISS)
def handle_no_first_kiss(character_id: int) -> int:
    """
    玩家未保有初吻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[4]:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_VIRGIN)
def handle_have_virgin(character_id: int) -> int:
    """
    校验玩家是否是童贞
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[5]:
        return 1
    return 0


@add_premise(constant_promise.Premise.NO_VIRGIN)
def handle_no_virgin(character_id: int) -> int:
    """
    玩家非童贞
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[5]:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_A_VIRGIN)
def handle_have_a_virgin(character_id: int) -> int:
    """
    校验玩家是否是A处
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.NO_A_VIRGIN)
def handle_no_a_virgin(character_id: int) -> int:
    """
    玩家非A处
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    if character_data.talent[1]:
        return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_NO_FIRST_KISS)
def handle_target_no_first_kiss(character_id: int) -> int:
    """
    校验交互对象是否初吻还在
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[4] == 1


@add_premise(constant_promise.Premise.TARGET_HAVE_FIRST_KISS)
def handle_target_have_first_kiss(character_id: int) -> int:
    """
    校验交互对象是否初吻不在了
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[4] == 1


@add_premise(constant_promise.Premise.TARGET_NO_VIRGIN)
def handle_target_no_virgin(character_id: int) -> int:
    """
    校验交互对象是否非处女
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[0] == 1

@add_premise(constant_promise.Premise.TARGET_HAVE_VIRGIN)
def handle_target_have_virgin(character_id: int) -> int:
    """
    校验交互对象是否是处女
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[0] == 1


@add_premise(constant_promise.Premise.TARGET_NO_A_VIRGIN)
def handle_target_no_a_virgin(character_id: int) -> int:
    """
    校验交互对象是否非A处女
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[1] == 1

@add_premise(constant_promise.Premise.TARGET_HAVE_A_VIRGIN)
def handle_target_have_a_virgin(character_id: int) -> int:
    """
    校验交互对象是否是A处女
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[1] == 1


@add_premise(constant_promise.Premise.IS_MEDICAL)
def handle_is_medical(character_id: int) -> int:
    """
    校验自己的职业为医疗
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return character_data.profession == 3


@add_premise(constant_promise.Premise.PATIENT_WAIT)
def handle_patient_wait(character_id: int) -> int:
    """
    有患者正等待就诊
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if cache.base_resouce.patient_now:
        return 1
    return 0


# @add_premise(constant_promise.Premise.TARGET_AGE_SIMILAR)
# def handle_target_age_similar(character_id: int) -> int:
#     """
#     校验角色目标对像是否与自己年龄相差不大
#     Keyword arguments:
#     character_id -- 角色id
#     Return arguments:
#     int -- 权重
#     """
#     character_data = cache.character_data[character_id]
#     target_data = cache.character_data[character_data.target_character_id]
#     if character_data.age >= target_data.age - 2 and character_data.age <= target_data.age + 2:
#         return 1
#     return 0


# @add_premise(constant_promise.Premise.TARGET_AVERAGE_HEIGHT_SIMILAR)
# def handle_target_average_height_similar(character_id: int) -> int:
#     """
#     校验角色目标身高是否与平均身高相差不大
#     Keyword arguments:
#     character_id -- 角色id
#     Return arguments:
#     int -- 权重
#     """
#     character_data = cache.character_data[character_id]
#     target_data = cache.character_data[character_data.target_character_id]
#     age_tem = attr_calculation.judge_age_group(target_data.age)
#     average_height = cache.average_height_by_age[age_tem][target_data.sex]
#     if (
#         target_data.height.now_height >= average_height * 0.95
#         and target_data.height.now_height <= average_height * 1.05
#     ):
#         return 1
#     return 0


# @add_premise(constant_promise.Premise.TARGET_AVERAGE_HEIGHT_LOW)
# def handle_target_average_height_low(character_id: int) -> int:
#     """
#     校验角色目标的身高是否低于平均身高
#     Keyword arguments:
#     character_id -- 角色id
#     Return arguments:
#     int -- 权重
#     """
#     character_data = cache.character_data[character_id]
#     target_data = cache.character_data[character_data.target_character_id]
#     age_tem = attr_calculation.judge_age_group(target_data.age)
#     average_height = cache.average_height_by_age[age_tem][target_data.sex]
#     if target_data.height.now_height <= average_height * 0.95:
#         return 1
#     return 0


@add_premise(constant_promise.Premise.TARGET_IS_PLAYER)
def handle_target_is_player(character_id: int) -> int:
    """
    校验角色目标是否是玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.target_character_id == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.DEBUG_MODE_ON)
def handle_idebug_mode_on(character_id: int) -> int:
    """
    校验当前是否已经是debug模式
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    if cache.debug_mode:
        return 1
    return 0


@add_premise(constant_promise.Premise.DEBUG_MODE_OFF)
def handle_idebug_mode_off(character_id: int) -> int:
    """
    校验当前不是debug模式
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    if cache.debug_mode:
        return 0
    return 1


@add_premise(constant_promise.Premise.TO_DO)
def handle_todo(character_id: int) -> int:
    """
    未实装
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    if cache.debug_mode:
        return 1
    return 0


@add_premise(constant_promise.Premise.IS_PLAYER)
def handle_is_player(character_id: int) -> int:
    """
    校验指令使用人是否是玩家角色
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    if not character_id:
        return 1
    return 0


@add_premise(constant_promise.Premise.NO_PLAYER)
def handle_no_player(character_id: int) -> int:
    """
    校验指令使用人是否不是玩家角色
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    if character_id:
        return 1
    return 0


@add_premise(constant_promise.Premise.IN_PLAYER_SCENE)
def handle_in_player_scene(character_id: int) -> int:
    """
    校验角色是否与玩家处于同场景中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    now_character_data: game_type.Character = cache.character_data[character_id]
    if now_character_data.position == cache.character_data[0].position:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_IN_PLAYER_SCENE)
def handle_not_in_player_scene(character_id: int) -> int:
    """
    校验角色是否不与玩家处于同场景中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    now_character_data: game_type.Character = cache.character_data[character_id]
    if now_character_data.position == cache.character_data[0].position:
        return 0
    return 1


@add_premise(constant_promise.Premise.SCENE_ONLY_TWO)
def handle_scene_only_two(character_id: int) -> int:
    """
    该地点仅有玩家和该角色
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    return len(scene_data.character_list) == 2


@add_premise(constant_promise.Premise.SCENE_OVER_TWO)
def handle_scene_over_two(character_id: int) -> int:
    """
    该地点里有除了玩家和该角色之外的人
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    return len(scene_data.character_list) > 2


@add_premise(constant_promise.Premise.SCENE_SOMEONE_IS_H)
def handle_scene_someone_is_h(character_id: int) -> int:
    """
    该地点有其他角色在和玩家H
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    #场景角色数大于2时进行检测
    if len(scene_data.character_list) > 2 and not (character_data.is_follow or character_data.is_h):
        #遍历当前角色列表
        for chara_id in scene_data.character_list:
            #遍历非自己且非玩家的角色
            if chara_id != character_id and chara_id != 0:
                other_character_data: game_type.Character = cache.character_data[chara_id]
                #检测是否在H
                if other_character_data.is_h:
                    return 999
    return 0


@add_premise(constant_promise.Premise.SCENE_SOMEONE_NO_FALL)
def handle_scene_someone_is_h(character_id: int) -> int:
    """
    该地点有未拥有陷落素质的角色
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path_str = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path_str]
    #场景角色数大于等于2时进行检测
    if len(scene_data.character_list) >= 2:
        #遍历当前角色列表
        for chara_id in scene_data.character_list:
            #遍历非玩家的角色
            if chara_id:
                other_character_data: game_type.Character = cache.character_data[chara_id]
                for i in {10,11,12,13,15,16,17,18}:
                    if other_character_data.talent[i]:
                        break
                    if i == 18:
                        return 999
    return 0


@add_premise(constant_promise.Premise.TATGET_LEAVE_SCENE)
def handle_target_leave_scene(character_id: int) -> int:
    """
    校验角色是否是从玩家场景离开
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    now_character_data: game_type.Character = cache.character_data[character_id]
    if (
        now_character_data.behavior.move_src == cache.character_data[0].position
        and now_character_data.behavior.move_target != cache.character_data[0].position
        and now_character_data.position != cache.character_data[0].position
    ):
        return 1
    return 0


@add_premise(constant_promise.Premise.TIME_DAY)
def handle_time_day(character_id: int) -> int:
    """
    时间:白天（6点~18点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time.hour >= 6 and now_time.hour <= 17:
        return 1
    return 0


@add_premise(constant_promise.Premise.TIME_NIGHT)
def handle_time_night(character_id: int) -> int:
    """
    时间:夜晚（18点~6点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time.hour <= 5 or now_time.hour >= 18:
        return 1
    return 0


@add_premise(constant_promise.Premise.TIME_MIDNIGHT)
def handle_time_midnight(character_id: int) -> int:
    """
    时间:深夜（22点~2点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time.hour <= 1 or now_time.hour >= 22:
        return 1
    return 0


@add_premise(constant_promise.Premise.TIME_MORNING)
def handle_time_morning(character_id: int) -> int:
    """
    时间:清晨（4点~8点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time.hour >= 4 and now_time.hour <= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.TIME_MOON)
def handle_time_moon(character_id: int) -> int:
    """
    时间:中午（10点~14点）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    now_time: datetime.datetime = character_data.behavior.start_time
    if now_time.hour >= 10 and now_time.hour <= 13:
        return 1
    return 0


@add_premise(constant_promise.Premise.SCENE_ONLY_ONE)
def handle_scene_only_one(character_id: int) -> int:
    """
    该地点里没有自己外的其他角色
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    scene_path = map_handle.get_map_system_path_str_for_list(character_data.position)
    scene_data: game_type.Scene = cache.scene_data[scene_path]
    return len(scene_data.character_list) == 1


@add_premise(constant_promise.Premise.TARGET_CHEST_IS_CLIFF)
def handle_target_chest_is_cliff(character_id: int) -> int:
    """
    交互对象胸部大小是绝壁
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[80]


@add_premise(constant_promise.Premise.TARGET_CHEST_IS_SMALL)
def handle_target_chest_is_small(character_id: int) -> int:
    """
    交互对象胸部大小是贫乳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[81]


@add_premise(constant_promise.Premise.TARGET_CHEST_IS_NORMAL)
def handle_target_chest_is_normal(character_id: int) -> int:
    """
    交互对象胸部大小是普乳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[82]


@add_premise(constant_promise.Premise.TARGET_CHEST_IS_BIG)
def handle_target_chest_is_big(character_id: int) -> int:
    """
    交互对象胸部大小是巨乳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[83]


@add_premise(constant_promise.Premise.TARGET_CHEST_IS_SUPER)
def handle_target_chest_is_super(character_id: int) -> int:
    """
    交互对象胸部大小是爆乳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[84]


@add_premise(constant_promise.Premise.TARGET_BUTTOCKS_IS_SMALL)
def handle_target_buttock_is_small(character_id: int) -> int:
    """
    交互对象屁股大小是小尻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[85]


@add_premise(constant_promise.Premise.TARGET_BUTTOCKS_IS_NORMAL)
def handle_target_buttock_is_normal(character_id: int) -> int:
    """
    交互对象胸部大小是普尻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[86]


@add_premise(constant_promise.Premise.TARGET_BUTTOCKS_IS_BIG)
def handle_target_buttock_is_big(character_id: int) -> int:
    """
    交互对象胸部大小是巨尻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[87]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_EARS)
def handle_target_have_no_eras(character_id: int) -> int:
    """
    交互对象没有兽耳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[70]


@add_premise(constant_promise.Premise.TARGET_HAVE_EARS)
def handle_target_have_eras(character_id: int) -> int:
    """
    交互对象有兽耳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[70]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_HORN)
def handle_target_have_no_horn(character_id: int) -> int:
    """
    交互对象没有兽角
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[71]


@add_premise(constant_promise.Premise.TARGET_HAVE_HORN)
def handle_target_have_horn(character_id: int) -> int:
    """
    交互对象有兽角
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[71]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_TAIL)
def handle_target_have_no_tail(character_id: int) -> int:
    """
    交互对象没有兽尾
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[72]


@add_premise(constant_promise.Premise.TARGET_HAVE_TAIL)
def handle_target_have_tail(character_id: int) -> int:
    """
    交互对象有兽尾
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[72]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_RING)
def handle_target_have_no_ring(character_id: int) -> int:
    """
    交互对象没有光环
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[73]


@add_premise(constant_promise.Premise.TARGET_HAVE_RING)
def handle_target_have_ring(character_id: int) -> int:
    """
    交互对象有光环
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[73]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_WING)
def handle_target_have_no_wing(character_id: int) -> int:
    """
    交互对象没有光翼
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[74]


@add_premise(constant_promise.Premise.TARGET_HAVE_WING)
def handle_target_have_wing(character_id: int) -> int:
    """
    交互对象有光翼
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[74]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_TENTACLE)
def handle_target_have_no_tentacle(character_id: int) -> int:
    """
    交互对象没有触手
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[75]


@add_premise(constant_promise.Premise.TARGET_HAVE_TENTACLE)
def handle_target_have_tentacle(character_id: int) -> int:
    """
    交互对象有触手
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[75]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_CAR)
def handle_target_have_no_car(character_id: int) -> int:
    """
    交互对象没有小车
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[76]


@add_premise(constant_promise.Premise.TARGET_HAVE_CAR)
def handle_target_have_car(character_id: int) -> int:
    """
    交互对象有小车
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[76]


@add_premise(constant_promise.Premise.TARGET_NOT_PATIENT)
def handle_target_not_patient(character_id: int) -> int:
    """
    交互对象不是源石病感染者
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[150]


@add_premise(constant_promise.Premise.TARGET_IS_PATIENT)
def handle_target_is_patient(character_id: int) -> int:
    """
    交互对象是源石病感染者
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[150]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_CRYSTAL)
def handle_target_have_no_crystal(character_id: int) -> int:
    """
    交互对象没有体表源石结晶
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[162]


@add_premise(constant_promise.Premise.TARGET_HAVE_CRYSTAL)
def handle_target_have_crystal(character_id: int) -> int:
    """
    交互对象有体表源石结晶
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[162]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_DILIGENT)
def handle_target_have_no_diligent(character_id: int) -> int:
    """
    交互对象非勤劳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[200]


@add_premise(constant_promise.Premise.TARGET_HAVE_DILIGENT)
def handle_target_have_diligent(character_id: int) -> int:
    """
    交互对象勤劳
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[200]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_LAZY)
def handle_target_have_no_lazy(character_id: int) -> int:
    """
    交互对象非懒散
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[201]


@add_premise(constant_promise.Premise.TARGET_HAVE_LAZY)
def handle_target_have_lazy(character_id: int) -> int:
    """
    交互对象懒散
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[201]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_FRAGILE)
def handle_target_have_no_fragile(character_id: int) -> int:
    """
    交互对象非脆弱
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[202]


@add_premise(constant_promise.Premise.TARGET_HAVE_FRAGILE)
def handle_target_have_fragile(character_id: int) -> int:
    """
    交互对象脆弱
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[202]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_FORCEFUL)
def handle_target_have_no_forceful(character_id: int) -> int:
    """
    交互对象非坚强
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[203]


@add_premise(constant_promise.Premise.TARGET_HAVE_FORCEFUL)
def handle_target_have_forceful(character_id: int) -> int:
    """
    交互对象坚强
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[203]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_ENTHUSIACTIC)
def handle_target_have_no_enthusiactic(character_id: int) -> int:
    """
    交互对象非热情
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[204]


@add_premise(constant_promise.Premise.TARGET_HAVE_ENTHUSIACTIC)
def handle_target_have_enthusiactic(character_id: int) -> int:
    """
    交互对象热情
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[204]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_ALONE)
def handle_target_have_no_alone(character_id: int) -> int:
    """
    交互对象非孤僻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[205]


@add_premise(constant_promise.Premise.TARGET_HAVE_ALONE)
def handle_target_have_alone(character_id: int) -> int:
    """
    交互对象孤僻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[205]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_SHAME)
def handle_target_have_no_shame(character_id: int) -> int:
    """
    交互对象非羞耻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[206]


@add_premise(constant_promise.Premise.TARGET_HAVE_SHAME)
def handle_target_have_shame(character_id: int) -> int:
    """
    交互对象羞耻
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[206]


@add_premise(constant_promise.Premise.TARGET_HAVE_NO_OPEN)
def handle_target_have_no_open(character_id: int) -> int:
    """
    交互对象非开放
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.talent[207]


@add_premise(constant_promise.Premise.TARGET_HAVE_OPEN)
def handle_target_have_open(character_id: int) -> int:
    """
    交互对象开放
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.talent[207]


@add_premise(constant_promise.Premise.LAST_CMD_BLOWJOB)
def handle_last_cmd_blowjob(character_id: int) -> int:
    """
    前一指令为口交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    if len_input and (last_cmd == str(constant.Instruct.BLOWJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_MAKING_OUT)
def handle_last_cmd_makeing_out(character_id: int) -> int:
    """
    前一指令为身体爱抚
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.MAKING_OUT)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_KISS_H)
def handle_last_cmd_kiss_h(character_id: int) -> int:
    """
    前一指令为接吻（H）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.KISS_H)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BREAST_CARESS)
def handle_last_cmd_breast_caress(character_id: int) -> int:
    """
    前一指令为胸爱抚
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.BREAST_CARESS)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_TWIDDLE_NIPPLES)
def handle_last_cmd_twiddle_nipples(character_id: int) -> int:
    """
    前一指令为玩弄乳头
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.TWIDDLE_NIPPLES)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BREAST_SUCKING)
def handle_last_cmd_breast_sucking(character_id: int) -> int:
    """
    前一指令为舔吸乳头
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.BREAST_SUCKING)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_CLIT_CARESS)
def handle_last_cmd_clit_caress(character_id: int) -> int:
    """
    前一指令为阴蒂爱抚
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.CLIT_CARESS)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_OPEN_LABIA)
def handle_last_cmd_open_labia(character_id: int) -> int:
    """
    前一指令为掰开阴唇观察
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.OPEN_LABIA)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_CUNNILINGUS)
def handle_last_cmd_cunnilingus(character_id: int) -> int:
    """
    前一指令为舔阴
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.CUNNILINGUS)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FINGER_INSERTION)
def handle_last_cmd_finger_insertion(character_id: int) -> int:
    """
    前一指令为手指插入(V)
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FINGER_INSERTION)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_ANAL_CARESS)
def handle_last_cmd_anal_caress(character_id: int) -> int:
    """
    前一指令为手指插入(A)
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.ANAL_CARESS)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_MAKE_MASTUREBATE)
def handle_last_cmd_make_masturebate(character_id: int) -> int:
    """
    前一指令为让对方自慰（H）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.MAKE_MASTUREBATE)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_HANDJOB)
def handle_last_cmd_handjob(character_id: int) -> int:
    """
    前一指令为手交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.HANDJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_PAIZURI)
def handle_last_cmd_paizuri(character_id: int) -> int:
    """
    前一指令为乳交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.PAIZURI)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FOOTJOB)
def handle_last_cmd_footjob(character_id: int) -> int:
    """
    前一指令为足交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FOOTJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_HAIRJOB)
def handle_last_cmd_hairjob(character_id: int) -> int:
    """
    前一指令为发交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.HAIRJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_AXILLAJOB)
def handle_last_cmd_axillajob(character_id: int) -> int:
    """
    前一指令为腋交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.AXILLAJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_RUB_BUTTOCK)
def handle_last_cmd_rub_buttock(character_id: int) -> int:
    """
    前一指令为素股
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.RUB_BUTTOCK)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_LEGJOB)
def handle_last_cmd_legjob(character_id: int) -> int:
    """
    前一指令为腿交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.LEGJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_TAILJOB)
def handle_last_cmd_tailjob(character_id: int) -> int:
    """
    前一指令为尾交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.TAILJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FACE_RUB)
def handle_last_cmd_face_rub(character_id: int) -> int:
    """
    前一指令为阴茎蹭脸
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FACE_RUB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_HORN_RUB)
def handle_last_cmd_horn_rub(character_id: int) -> int:
    """
    前一指令为阴茎蹭角
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.HORN_RUB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_EARS_RUB)
def handle_last_cmd_ears_rub(character_id: int) -> int:
    """
    前一指令为阴茎蹭耳朵
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.EARS_RUB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_HAND_BLOWJOB)
def handle_last_cmd_hand_blowjob(character_id: int) -> int:
    """
    前一指令为手交口交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.HAND_BLOWJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_TITS_BLOWJOB)
def handle_last_cmd_tits_blowjob(character_id: int) -> int:
    """
    前一指令为乳交口交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.TITS_BLOWJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_DEEP_THROAT)
def handle_last_cmd_deep_throat(character_id: int) -> int:
    """
    前一指令为深喉插入
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.DEEP_THROAT)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FOCUS_BLOWJOB)
def handle_last_cmd_focus_blowjob(character_id: int) -> int:
    """
    前一指令为真空口交
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FOCUS_BLOWJOB)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_NORMAL_SEX)
def handle_last_cmd_normal_sex(character_id: int) -> int:
    """
    前一指令为正常位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.NORMAL_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BACK_SEX)
def handle_last_cmd_back_sex(character_id: int) -> int:
    """
    前一指令为背后位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.BACK_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_RIDING_SEX)
def handle_last_cmd_riding_sex(character_id: int) -> int:
    """
    前一指令为骑乘位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.RIDING_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FACE_SEAT_SEX)
def handle_last_cmd_face_seat_sex(character_id: int) -> int:
    """
    前一指令为对面座位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FACE_SEAT_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BACK_SEAT_SEX)
def handle_last_cmd_back_seat_sex(character_id: int) -> int:
    """
    前一指令为背面座位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.BACK_SEAT_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_FACE_STAND_SEX)
def handle_last_cmd_face_stand_sex(character_id: int) -> int:
    """
    前一指令为对面立位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.FACE_STAND_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BACK_STAND_SEX)
def handle_last_cmd_back_stand_sex(character_id: int) -> int:
    """
    前一指令为背面立位
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.BACK_STAND_SEX)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_STIMULATE_G_POINT)
def handle_last_cmd_stimulate_g_point(character_id: int) -> int:
    """
    前一指令为刺激G点
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.STIMULATE_G_POINT)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_WOMB_OS_CARESS)
def handle_last_cmd_womb_os_caress(character_id: int) -> int:
    """
    前一指令为玩弄子宫口
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-2]
    if len_input and (last_cmd == str(constant.Instruct.WOMB_OS_CARESS)):
        return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_PENIS_POSITION)
def handle_last_cmd_penis_position(character_id: int) -> int:
    """
    前一指令为阴茎位置相关指令_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.NORMAL_SEX),str(constant.Instruct.BACK_SEX),str(constant.Instruct.RIDING_SEX),
        str(constant.Instruct.FACE_SEAT_SEX),str(constant.Instruct.BACK_SEAT_SEX),
        str(constant.Instruct.FACE_STAND_SEX),str(constant.Instruct.BACK_STAND_SEX),
        str(constant.Instruct.STIMULATE_G_POINT),str(constant.Instruct.WOMB_OS_CARESS),str(constant.Instruct.WOMB_INSERTION),
        str(constant.Instruct.NORMAL_ANAL_SEX),str(constant.Instruct.BACK_ANAL_SEX),str(constant.Instruct.RIDING_ANAL_SEX),
        str(constant.Instruct.FACE_SEAT_ANAL_SEX),str(constant.Instruct.BACK_SEAT_ANAL_SEX),
        str(constant.Instruct.FACE_STAND_ANAL_SEX),str(constant.Instruct.BACK_STAND_ANAL_SEX),
        str(constant.Instruct.STIMULATE_SIGMOID_COLON),str(constant.Instruct.STIMULATE_VAGINA),
        str(constant.Instruct.URETHRAL_INSERTION),
        str(constant.Instruct.HANDJOB),str(constant.Instruct.HAND_BLOWJOB),
        str(constant.Instruct.BLOWJOB),str(constant.Instruct.PAIZURI),
        str(constant.Instruct.TITS_BLOWJOB),str(constant.Instruct.FOCUS_BLOWJOB),
        str(constant.Instruct.DEEP_THROAT),str(constant.Instruct.SIXTY_NINE),
        str(constant.Instruct.FOOTJOB),str(constant.Instruct.HAIRJOB),
        str(constant.Instruct.AXILLAJOB),str(constant.Instruct.RUB_BUTTOCK),
        str(constant.Instruct.LEGJOB),str(constant.Instruct.TAILJOB),
        str(constant.Instruct.FACE_RUB),str(constant.Instruct.HORN_RUB),
        str(constant.Instruct.EARS_RUB),
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BLOWJOB_OR_HANDJOB)
def handle_last_cmd_blowjob_or_handjob(character_id: int) -> int:
    """
    前一指令为口交或手交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    if len_input:
        if (last_cmd == str(constant.Instruct.BLOWJOB)) or (last_cmd == str(constant.Instruct.HANDJOB)):
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BLOWJOB_OR_PAIZURI)
def handle_last_cmd_blowjob_or_paizuri(character_id: int) -> int:
    """
    前一指令为口交或乳交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    if len_input:
        if (last_cmd == str(constant.Instruct.BLOWJOB)) or (last_cmd == str(constant.Instruct.PAIZURI)):
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BLOWJOB_OR_CUNNILINGUS)
def handle_last_cmd_blowjob_or_cunnilingus(character_id: int) -> int:
    """
    前一指令为口交或舔阴_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    if len_input:
        if (last_cmd == str(constant.Instruct.BLOWJOB)) or (last_cmd == str(constant.Instruct.CUNNILINGUS)):
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_SEX)
def handle_last_cmd_sex(character_id: int) -> int:
    """
    前一指令为V性交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.NORMAL_SEX),str(constant.Instruct.BACK_SEX),str(constant.Instruct.RIDING_SEX),
        str(constant.Instruct.FACE_SEAT_SEX),str(constant.Instruct.BACK_SEAT_SEX),
        str(constant.Instruct.FACE_STAND_SEX),str(constant.Instruct.BACK_STAND_SEX),
        str(constant.Instruct.STIMULATE_G_POINT),str(constant.Instruct.WOMB_OS_CARESS),str(constant.Instruct.WOMB_INSERTION)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_W_SEX)
def handle_last_cmd_w_sex(character_id: int) -> int:
    """
    前一指令为W性交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.WOMB_OS_CARESS),str(constant.Instruct.WOMB_INSERTION)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_A_SEX)
def handle_last_cmd_a_sex(character_id: int) -> int:
    """
    前一指令为A性交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.NORMAL_ANAL_SEX),str(constant.Instruct.BACK_ANAL_SEX),str(constant.Instruct.RIDING_ANAL_SEX),
        str(constant.Instruct.FACE_SEAT_ANAL_SEX),str(constant.Instruct.BACK_SEAT_ANAL_SEX),
        str(constant.Instruct.FACE_STAND_ANAL_SEX),str(constant.Instruct.BACK_STAND_ANAL_SEX),
        str(constant.Instruct.STIMULATE_SIGMOID_COLON),str(constant.Instruct.STIMULATE_VAGINA)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_U_SEX)
def handle_last_cmd_u_sex(character_id: int) -> int:
    """
    前一指令为U性交_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.URETHRAL_INSERTION)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BREAST_CARESS_TYPE)
def handle_last_cmd_breast_caress_type(character_id: int) -> int:
    """
    前一指令为胸部爱抚类_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.BREAST_CARESS),str(constant.Instruct.TWIDDLE_NIPPLES),
        str(constant.Instruct.BREAST_SUCKING)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_HANDJOB_TYPE)
def handle_last_cmd_handjob_type(character_id: int) -> int:
    """
    前一指令为手交类_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.HANDJOB),str(constant.Instruct.HAND_BLOWJOB)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_BLOWJOB_TYPE)
def handle_last_cmd_blowjob_type(character_id: int) -> int:
    """
    前一指令为口交类_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.BLOWJOB),str(constant.Instruct.HAND_BLOWJOB),
        str(constant.Instruct.TITS_BLOWJOB),str(constant.Instruct.FOCUS_BLOWJOB),
        str(constant.Instruct.DEEP_THROAT),str(constant.Instruct.SIXTY_NINE)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.LAST_CMD_PAIZURI_TYPE)
def handle_last_cmd_paizuri_type(character_id: int) -> int:
    """
    前一指令为乳交类_指令触发用
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    len_input = cache.input_cache
    len_input = len(len_input)
    last_cmd = cache.input_cache[len(cache.input_cache)-1]
    sex = {
        str(constant.Instruct.PAIZURI),str(constant.Instruct.TITS_BLOWJOB)
        }
    if len_input:
        if last_cmd in sex:
            return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_HAIR)
def handle_penis_in_t_hair(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_发交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_FACE)
def handle_penis_in_t_face(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_阴茎蹭脸中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_MOUSE)
def handle_penis_in_t_mouse(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_口交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_BREAST)
def handle_penis_in_t_breast(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_乳交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_AXILLA)
def handle_penis_in_t_axilla(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_腋交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_HAND)
def handle_penis_in_t_hand(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_手交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_VAGINA)
def handle_penis_in_t_vagina(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_V插入中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 6:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_WOMB)
def handle_penis_in_t_womb(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_W插入中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_ANAL)
def handle_penis_in_t_anal(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_A插入中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 8:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_URETHRAL)
def handle_penis_in_t_nrethral(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_U插入中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 9:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_LEG)
def handle_penis_in_t_leg(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_腿交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 10:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_FOOT)
def handle_penis_in_t_foot(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_足交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 11:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_TAIL)
def handle_penis_in_t_tail(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_尾交中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 12:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_HORN)
def handle_penis_in_t_horn(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_阴茎蹭角中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 13:
        return 1
    return 0


@add_premise(constant_promise.Premise.PENIS_IN_T_EARS)
def handle_penis_in_t_ears(character_id: int) -> int:
    """
    当前阴茎位置为交互对象_阴茎蹭耳朵中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.insert_position == 14:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_BODY)
def handle_shoot_in_t_body(character_id: int) -> int:
    """
    在交互对象的身体上射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body != -1:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_HAIR)
def handle_shoot_in_t_hair(character_id: int) -> int:
    """
    在交互对象的头发射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_FACE)
def handle_shoot_in_t_face(character_id: int) -> int:
    """
    在交互对象的脸部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_MOUSE)
def handle_shoot_in_t_mouse(character_id: int) -> int:
    """
    在交互对象的口腔射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_BREAST)
def handle_shoot_in_t_breast(character_id: int) -> int:
    """
    在交互对象的胸部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_AXILLA)
def handle_shoot_in_t_axilla(character_id: int) -> int:
    """
    在交互对象的腋部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 4:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_HAND)
def handle_shoot_in_t_hand(character_id: int) -> int:
    """
    在交互对象的手部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_VAGINA)
def handle_shoot_in_t_vagina(character_id: int) -> int:
    """
    在交互对象的小穴射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 6:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_WOMB)
def handle_shoot_in_t_womb(character_id: int) -> int:
    """
    在交互对象的子宫射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_ANAL)
def handle_shoot_in_t_anal(character_id: int) -> int:
    """
    在交互对象的后穴射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 8:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_URETHRAL)
def handle_shoot_in_t_nrethral(character_id: int) -> int:
    """
    在交互对象的尿道射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 9:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_LEG)
def handle_shoot_in_t_leg(character_id: int) -> int:
    """
    在交互对象的腿部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 10:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_FOOT)
def handle_shoot_in_t_foot(character_id: int) -> int:
    """
    在交互对象的脚部射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 11:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_TAIL)
def handle_shoot_in_t_tail(character_id: int) -> int:
    """
    在交互对象的尾巴射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 12:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_HORN)
def handle_shoot_in_t_horn(character_id: int) -> int:
    """
    在交互对象的兽角射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 13:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_EARS)
def handle_shoot_in_t_ears(character_id: int) -> int:
    """
    在交互对象的兽耳射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_body == 14:
        return 1
    return 0


@add_premise(constant_promise.Premise.SHOOT_IN_T_CLOTH)
def handle_shoot_in_t_cloth(character_id: int) -> int:
    """
    在交互对象的衣服上射精
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.shoot_position_cloth != -1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_ORGASM_0)
def handle_t_turn_orgasm_0(character_id: int) -> int:
    """
    交互对象本次H中还没有绝顶
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    for body_part in game_config.config_body_part:
        if target_data.h_state.orgasm_count[body_part][1]:
            return 0
    return 1


@add_premise(constant_promise.Premise.T_TURN_ORGASM_G_1)
def handle_t_turn_orgasm_g_1(character_id: int) -> int:
    """
    交互对象本次H中绝顶次数>1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    count = 0
    for body_part in game_config.config_body_part:
        count += target_data.h_state.orgasm_count[body_part][1]
        if count > 1:
            return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_ORGASM_G_5)
def handle_t_turn_orgasm_g_5(character_id: int) -> int:
    """
    交互对象本次H中绝顶次数>5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    count = 0
    for body_part in game_config.config_body_part:
        count += target_data.h_state.orgasm_count[body_part][1]
        if count > 5:
            return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_ORGASM_G_10)
def handle_t_turn_orgasm_g_10(character_id: int) -> int:
    """
    交互对象本次H中绝顶次数>10
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    count = 0
    for body_part in game_config.config_body_part:
        count += target_data.h_state.orgasm_count[body_part][1]
        if count > 10:
            return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_N_ORGASM_G_3)
def handle_t_turn_n_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中N绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[0][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_B_ORGASM_G_3)
def handle_t_turn_b_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中B绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[1][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_C_ORGASM_G_3)
def handle_t_turn_c_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中C绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[2][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.TURN_P_ORGASM_G_1)
def handle_turn_p_orgasm_g_1(character_id: int) -> int:
    """
    玩家本次H中射精次数>1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[0]
    if character_data.h_state.orgasm_count[3][1] > 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.TURN_P_ORGASM_G_3)
def handle_turn_p_orgasm_g_3(character_id: int) -> int:
    """
    玩家本次H中射精次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[0]
    if character_data.h_state.orgasm_count[3][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_V_ORGASM_G_3)
def handle_t_turn_v_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中V绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[4][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_A_ORGASM_G_3)
def handle_t_turn_a_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中A绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[5][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_U_ORGASM_G_3)
def handle_t_turn_u_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中U绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[6][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_W_ORGASM_G_3)
def handle_t_turn_w_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中W绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[7][1] > 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_TURN_M_ORGASM_G_3)
def handle_t_turn_m_orgasm_g_3(character_id: int) -> int:
    """
    交互对象本次H中M绝顶次数>3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.h_state.orgasm_count[8][1] > 3:
        return 1
    return 0


# 以下为道具系前提

@add_premise(constant_promise.Premise.HAVE_CAMERA)
def handle_have_camera(character_id: int) -> int:
    """
    校验角色是否已持有相机
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[50]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_VIDEO_RECORDER)
def handle_have_video_recorder(character_id: int) -> int:
    """
    校验角色是否已持有录像机
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[51]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_INSTRUMENT)
def handle_have_instrument(character_id: int) -> int:
    """
    校验角色是否已持有乐器
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[52]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_NIPPLE_CLAMP)
def handle_have_nipple_clamp(character_id: int) -> int:
    """
    校验角色是否已持有乳头夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[122]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOW_NIPPLE_CLAMP)
def handle_target_now_nipple_clamp(character_id: int) -> int:
    """
    校验交互对象是否正在乳头夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[0][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_NIPPLE_CLAMP)
def handle_target_not_nipple_clamp(character_id: int) -> int:
    """
    校验交互对象是否没有在乳头夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[0][1]:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_LOVE_EGG)
def handle_have_love_egg(character_id: int) -> int:
    """
    校验角色是否已持有跳蛋
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[121]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_CLIT_CLAMP)
def handle_have_clit_clamp(character_id: int) -> int:
    """
    校验角色是否已持有阴蒂夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[123]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOW_CLIT_CLAMP)
def handle_target_now_clit_clamp(character_id: int) -> int:
    """
    校验交互对象是否正在阴蒂夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[1][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_CLIT_CLAMP)
def handle_target_not_clit_clamp(character_id: int) -> int:
    """
    校验交互对象是否没有在阴蒂夹
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[1][1]:
        return 0
    return 1

@add_premise(constant_promise.Premise.HAVE_ELECTRIC_MESSAGE_STICK)
def handle_have_electric_message_stick(character_id: int) -> int:
    """
    校验角色是否已持有电动按摩棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[124]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_VIBRATOR)
def handle_have_vibrator(character_id: int) -> int:
    """
    校验角色是否已持有震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[125]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOW_VIBRATOR_INSERTION)
def handle_target_now_vibrator_insertion(character_id: int) -> int:
    """
    校验交互对象V正插入震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[2][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_VIBRATOR_INSERTION)
def handle_target_not_vibrator_insertion(character_id: int) -> int:
    """
    校验交互对象V没有在插入震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[2][1]:
        return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_NOW_VIBRATOR_INSERTION_ANAL)
def handle_target_now_vibrator_insertion_anal(character_id: int) -> int:
    """
    校验交互对象A正插入震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[3][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_VIBRATOR_INSERTION_ANAL)
def handle_target_not_vibrator_insertion(character_id: int) -> int:
    """
    校验交互对象A没有在插入震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[3][1]:
        return 0
    return 1


@add_premise(constant_promise.Premise.HAVE_MILKING_MACHINE)
def handle_have_milking_machine(character_id: int) -> int:
    """
    校验角色是否已持有搾乳机
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[133]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_URINE_COLLECTOR)
def handle_have_urine_collector(character_id: int) -> int:
    """
    校验角色是否已持有采尿器
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[134]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_BONDAGE)
def handle_have_bondage(character_id: int) -> int:
    """
    校验角色是否已持有绳子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[135]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_PATCH)
def handle_have_patch(character_id: int) -> int:
    """
    校验角色是否已持有眼罩
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[132]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_BIG_VIBRATOR)
def handle_have_big_vibrator(character_id: int) -> int:
    """
    校验角色是否已持有加粗震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[126]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_HUGE_VIBRATOR)
def handle_have_huge_vibrator(character_id: int) -> int:
    """
    校验角色是否已持有巨型震动棒
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[127]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_CLYSTER_TOOLS)
def handle_have_clyster_tools(character_id: int) -> int:
    """
    校验角色是否已持有灌肠套装
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[128]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_ANAL_BEADS)
def handle_have_anal_beads(character_id: int) -> int:
    """
    校验角色是否已持有肛门拉珠
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[129]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOW_ANAL_BEADS)
def handle_target_now_anal_beads(character_id: int) -> int:
    """
    校验交互对象是否正在肛门拉珠
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[7][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_ANAL_BEADS)
def handle_target_not_anal_beads(character_id: int) -> int:
    """
    校验交互对象是否没有在肛门拉珠
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.h_state.body_item[7][1]:
        return 0
    return 1

@add_premise(constant_promise.Premise.HAVE_ANAL_PLUG)
def handle_have_anal_plug(character_id: int) -> int:
    """
    校验角色是否已持有肛塞
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    # if character_data.item[130]:
        # return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_WHIP)
def handle_have_whip(character_id: int) -> int:
    """
    校验角色是否已持有鞭子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[131]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_NEEDLE)
def handle_have_needle(character_id: int) -> int:
    """
    校验角色是否已持有针
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[137]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_COLLAR)
def handle_have_collar(character_id: int) -> int:
    """
    校验角色是否已持有项圈
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[138]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_CONDOM)
def handle_have_condom(character_id: int) -> int:
    """
    校验角色是否已持有避孕套
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[120]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_SAFE_CANDLES)
def handle_have_safe_candles(character_id: int) -> int:
    """
    校验角色是否已持有低温蜡烛
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[136]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_COTTON_STICK)
def handle_have_cotton_stick(character_id: int) -> int:
    """
    校验角色是否已持有无菌棉签
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[139]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_BIRTH_CONTROL_PILLS_BEFORE)
def handle_have_birth_control_pills_before(character_id: int) -> int:
    """
    校验角色是否已持有事前避孕药
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[101]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_BIRTH_CONTROL_PILLS_AFTER)
def handle_have_birth_control_pills_after(character_id: int) -> int:
    """
    校验角色是否已持有事后避孕药
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[102]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_BODY_LUBRICANT)
def handle_have_body_lubricant(character_id: int) -> int:
    """
    校验角色是否已持有润滑液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[100]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_PHILTER)
def handle_have_philter(character_id: int) -> int:
    """
    校验角色是否已持有媚药
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[103]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_ENEMAS)
def handle_have_enemas(character_id: int) -> int:
    """
    校验角色是否已持有灌肠液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[104]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_DIURETICS_ONCE)
def handle_have_diuretics_once(character_id: int) -> int:
    """
    校验角色是否已持有一次性利尿剂
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[105]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_DIURETICS_PERSISTENT)
def handle_have_diuretics_persistent(character_id: int) -> int:
    """
    校验角色是否已持有持续性利尿剂
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[106]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_SLEEPING_PILLS)
def handle_have_sleeping_pills(character_id: int) -> int:
    """
    校验角色是否已持有睡眠药
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[107]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_CLOMID)
def handle_have_clomid(character_id: int) -> int:
    """
    校验角色是否已持有排卵促进药
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.item[108]:
        return 1
    return 0

@add_premise(constant_promise.Premise.A_SHIT)
def handle_a_shit(character_id: int) -> int:
    """
    校验角色是否肠内脏污
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [1,3]:
        return 1
    return 0

@add_premise(constant_promise.Premise.ENEMA)
def handle_enema(character_id: int) -> int:
    """
    校验角色是否正在灌肠中（含全种类灌肠）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [1,3]:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_ENEMA)
def handle_not_enema(character_id: int) -> int:
    """
    校验角色是否非灌肠中（含全种类灌肠）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean not in [1,3]:
        return 1
    return 0

@add_premise(constant_promise.Premise.ENEMA_END)
def handle_enema_end(character_id: int) -> int:
    """
    校验角色是否已灌肠（含全种类灌肠）
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [2,4]:
        return 1
    return 0

@add_premise(constant_promise.Premise.NORMAL_ENEMA)
def handle_normal_enema(character_id: int) -> int:
    """
    校验角色是否普通灌肠中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [1]:
        return 1
    return 0

@add_premise(constant_promise.Premise.SEMEN_ENEMA)
def handle_semen_enema(character_id: int) -> int:
    """
    校验角色是否精液灌肠中
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [3]:
        return 1
    return 0

@add_premise(constant_promise.Premise.NORMAL_ENEMA_END)
def handle_normal_enema_end(character_id: int) -> int:
    """
    校验角色是否已普通灌肠
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [2]:
        return 1
    return 0

@add_premise(constant_promise.Premise.SEMEN_ENEMA_END)
def handle_semen_enema_end(character_id: int) -> int:
    """
    校验角色是否已精液灌肠
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.a_clean in [4]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAIR_SEMEN)
def handle_t_hair_semen(character_id: int) -> int:
    """
    交互对象当前头发有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.body_semen[0][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WOMB_SEMEN)
def handle_t_womb_semen(character_id: int) -> int:
    """
    交互对象当前子宫有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.body_semen[7][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.URINATE_LE_79)
def handle_urinate_le_79(character_id: int) -> int:
    """
    尿意条≤79%，不需要排尿
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.urinate_point / 240
    if value <= 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.URINATE_GE_80)
def handle_urinate_ge_80(character_id: int) -> int:
    """
    尿意条≥80%，需要排尿
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.urinate_point / 240
    if value > 0.79:
        return character_data.urinate_point * 4
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_URINATE_LE_79)
def handle_target_urinate_le_79(character_id: int) -> int:
    """
    交互对象尿意条≤79%，不需要排尿
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]

    value = target_data.urinate_point / 240
    if value <= 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_URINATE_GE_80)
def handle_target_urinate_ge_80(character_id: int) -> int:
    """
    交互对象尿意条≥80%，需要排尿
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]

    value = target_data.urinate_point / 240
    if value > 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.HUNGER_LE_79)
def handle_hunger_le_79(character_id: int) -> int:
    """
    饥饿值≤79%，不需要吃饭
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.hunger_point / 240
    if value <= 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.HUNGER_GE_80)
def handle_hunger_ge_80(character_id: int) -> int:
    """
    饥饿值≥80%，需要吃饭
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]

    value = character_data.hunger_point / 240
    if value > 0.79:
        # print(f"debug {character_id}角色饿了")
        return character_data.hunger_point * 4
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_HUNGER_LE_79)
def handle_target_hunger_le_79(character_id: int) -> int:
    """
    交互对象饥饿值≤79%，不需要吃饭
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]

    value = target_data.hunger_point / 240
    if value <= 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_HUNGER_GE_80)
def handle_target_hunger_ge_80(character_id: int) -> int:
    """
    交互对象饥饿值≥80%，需要吃饭
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]

    value = target_data.hunger_point / 240
    if value > 0.79:
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.WEAR_BRA)
def handle_wear_bra(character_id: int) -> int:
    """
    穿着胸衣
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if len(character_data.cloth[6]):
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_WEAR_BRA)
def handle_t_wear_bra(character_id: int) -> int:
    """
    交互对象穿着胸衣
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[6]):
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_WEAR_BRA)
def handle_t_not_wear_bra(character_id: int) -> int:
    """
    交互对象没有穿着胸衣
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[6]):
        return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_WEAR_GLOVES)
def handle_t_wear_gloves(character_id: int) -> int:
    """
    交互对象戴着手套
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[7]):
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_WEAR_GLOVES)
def handle_t_not_wear_gloves(character_id: int) -> int:
    """
    交互对象没有戴着手套
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[7]):
        return 0
    return 1


@add_premise(constant_promise.Premise.WEAR_SKIRT)
def handle_wear_skirt(character_id: int) -> int:
    """
    穿着裙子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if len(character_data.cloth[8]):
        cloth_id = character_data.cloth[8][0]
        if game_config.config_clothing_tem[cloth_id].tag == 5:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_WEAR_SKIRT)
def handle_t_wear_skirt(character_id: int) -> int:
    """
    交互对象穿着裙子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[8]):
        cloth_id = target_data.cloth[8][0]
        if game_config.config_clothing_tem[cloth_id].tag == 5:
            return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_WEAR_TROUSERS)
def handle_t_wear_trousers(character_id: int) -> int:
    """
    交互对象穿着裤子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[8]):
        cloth_id = target_data.cloth[8][0]
        if game_config.config_clothing_tem[cloth_id].tag == 4:
            return 1
    return 0


@add_premise(constant_promise.Premise.WEAR_PAN)
def handle_wear_pan(character_id: int) -> int:
    """
    穿着内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if len(character_data.cloth[9]):
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_WEAR_PAN)
def handle_t_wear_pan(character_id: int) -> int:
    """
    交互对象穿着内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[9]):
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_WEAR_PAN)
def handle_t_not_wear_pan(character_id: int) -> int:
    """
    交互对象没有穿着内裤
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[9]):
        return 0
    return 1


@add_premise(constant_promise.Premise.WEAR_SOCKS)
def handle_wear_socks(character_id: int) -> int:
    """
    穿着袜子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if len(character_data.cloth[10]):
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.TARGET_WEAR_SOCKS)
def handle_t_wear_socks(character_id: int) -> int:
    """
    交互对象穿着袜子
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if len(target_data.cloth[10]):
        return 1
    return 0


@add_premise(constant_promise.Premise.CLOTH_OFF)
def handle_cloth_off(character_id: int) -> int:
    """
    当前全裸
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    for clothing_type in game_config.config_clothing_type:
        if len(character_data.cloth[clothing_type]):
            return 0
    return 1


@add_premise(constant_promise.Premise.NOT_CLOTH_OFF)
def handle_not_cloth_off(character_id: int) -> int:
    """
    当前不是全裸
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    for clothing_type in game_config.config_clothing_type:
        if len(character_data.cloth[clothing_type]):
            return 1
    return 0


@add_premise(constant_promise.Premise.SHOWER_CLOTH)
def handle_shower_cloth(character_id: int) -> int:
    """
    围着浴巾
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if 551 in character_data.cloth[5]:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_SHOWER_CLOTH)
def handle_not_shower_cloth(character_id: int) -> int:
    """
    没有围着浴巾
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if 551 in character_data.cloth[5]:
        return 0
    return 1


@add_premise(constant_promise.Premise.T_UP_CLOTH_SEMEN)
def handle_t_up_cloth_semen(character_id: int) -> int:
    """
    交互对象当前上衣有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.cloth_semen[5][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_GLOVE_SEMEN)
def handle_t_glove_semen(character_id: int) -> int:
    """
    交互对象当前手套有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.cloth_semen[7][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BOTTOM_CLOTH_SEMEN)
def handle_t_botton_cloth_semen(character_id: int) -> int:
    """
    交互对象当前下衣有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.cloth_semen[8][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_PAN_SEMEN)
def handle_t_pan_semen(character_id: int) -> int:
    """
    交互对象当前内裤有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.cloth_semen[9][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SOCKS_SEMEN)
def handle_t_socks_semen(character_id: int) -> int:
    """
    交互对象当前袜子有精液
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    if target_data.dirty.cloth_semen[10][1]:
        return 1
    return 0


@add_premise(constant_promise.Premise.HAVE_COLLECTION)
def handle_have_collection(character_id: int) -> int:
    """
    持有藏品
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[0]
    if len(character_data.pl_collection.npc_panties_tem):
        return 1
    if len(character_data.pl_collection.npc_socks_tem):
        return 1
    else:
        return 0


@add_premise(constant_promise.Premise.NO_FIRST_KISS)
def handle_no_first_kiss(character_id: int) -> int:
    """
    校验是否初吻还在
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return character_data.talent[4] == 1


@add_premise(constant_promise.Premise.HAVE_FIRST_KISS)
def handle_have_first_kiss(character_id: int) -> int:
    """
    校验是否初吻不在了
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return character_data.first_kiss != -1


@add_premise(constant_promise.Premise.IS_H)
def handle_is_h(character_id: int) -> int:
    """
    玩家已启用H模式
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    target_data = cache.character_data[character_data.target_character_id]
    return target_data.is_h


@add_premise(constant_promise.Premise.NOT_H)
def handle_not_h(character_id: int) -> int:
    """
    玩家未启用H模式
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[0]
    target_data = cache.character_data[character_data.target_character_id]
    return not target_data.is_h


@add_premise(constant_promise.Premise.OPTION_SON)
def handle_option_son(character_id: int) -> int:
    """
    选项的子事件
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    return 0


@add_premise(constant_promise.Premise.IS_ASSISTANT)
def handle_is_assistant(character_id: int) -> int:
    """
    自己是当前的助理干员
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    pl_character_data: game_type.Character = cache.character_data[0]
    if pl_character_data.assistant_character_id == character_id:
        return 1
    return 0


@add_premise(constant_promise.Premise.NOT_ASSISTANT)
def handle_not_assistant(character_id: int) -> int:
    """
    自己不是当前的助理干员
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    pl_character_data: game_type.Character = cache.character_data[0]
    if pl_character_data.assistant_character_id == character_id:
        return 0
    return 1


@add_premise(constant_promise.Premise.TARGET_IS_ASSISTANT)
def handle_target_is_assistant(character_id: int) -> int:
    """
    交互对象是当前的助理干员
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    pl_character_data: game_type.Character = cache.character_data[0]
    if pl_character_data.assistant_character_id == character_data.target_character_id:
        return 1
    return 0


@add_premise(constant_promise.Premise.TARGET_NOT_ASSISTANT)
def handle_target_not_assistant(character_id: int) -> int:
    """
    交互对象不是当前的助理干员
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    pl_character_data: game_type.Character = cache.character_data[0]
    if pl_character_data.assistant_character_id == character_data.target_character_id:
        return 0
    return 1


@add_premise(constant_promise.Premise.IS_FOLLOW)
def handle_is_follow(character_id: int) -> int:
    """
    校验正在跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return character_data.is_follow


@add_premise(constant_promise.Premise.NOT_FOLLOW)
def handle_not_follow(character_id: int) -> int:
    """
    校验是否没有跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return not character_data.is_follow


@add_premise(constant_promise.Premise.IS_FOLLOW_1)
def handle_is_follow_1(character_id: int) -> int:
    """
    校验是否正智能跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.is_follow == 1:
        return 100
    return 0


@add_premise(constant_promise.Premise.NOT_FOLLOW_1)
def handle_not_follow_1(character_id: int) -> int:
    """
    校验是否没有智能跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    return not character_data.is_follow == 1


@add_premise(constant_promise.Premise.IS_FOLLOW_3)
def handle_is_follow_3(character_id: int) -> int:
    """
    校验是否当前正前往博士办公室
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    if character_data.is_follow == 3:
        return 100
    return 0


@add_premise(constant_promise.Premise.TARGET_IS_FOLLOW)
def handle_target_is_follow(character_id: int) -> int:
    """
    校验交互对象是否正跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return target_data.is_follow


@add_premise(constant_promise.Premise.TARGET_NOT_FOLLOW)
def handle_target_not_follow(character_id: int) -> int:
    """
    校验交互对象是否没有跟随玩家
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data: game_type.Character = cache.character_data[character_id]
    target_data: game_type.Character = cache.character_data[character_data.target_character_id]
    return not target_data.is_follow


# @add_premise(constant_promise.Premise.TARGET_IS_COLLECTION)
# def handle_target_is_collection(character_id: int) -> int:
#     """
#     校验交互对象是否已被玩家收藏
#     Keyword arguments:
#     character_id -- 角色id
#     Return arguments:
#     int -- 权重
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     player_data: game_type.Character = cache.character_data[0]
#     return character_data.target_character_id in player_data.collection_character


# @add_premise(constant_promise.Premise.TARGET_IS_NOT_COLLECTION)
# def handle_target_is_not_collection(character_id: int) -> int:
#     """
#     校验交互对象是否未被玩家收藏
#     Keyword arguments:
#     character_id -- 角色id
#     Return arguments:
#     int -- 权重
#     """
#     character_data: game_type.Character = cache.character_data[character_id]
#     player_data: game_type.Character = cache.character_data[0]
#     return character_data.target_character_id not in player_data.collection_character


@add_premise(constant_promise.Premise.T_NFEEL_GE_1)
def handle_t_nfeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_GE_3)
def handle_t_nfeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_GE_5)
def handle_t_nfeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_GE_7)
def handle_t_nfeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_L_1)
def handle_t_nfeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_L_3)
def handle_t_nfeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_NFEEL_L_5)
def handle_t_nfeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｎ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[0] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_GE_1)
def handle_t_bfeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_GE_3)
def handle_t_bfeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_GE_5)
def handle_t_bfeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_GE_7)
def handle_t_bfeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_L_1)
def handle_t_bfeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_L_3)
def handle_t_bfeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_BFEEL_L_5)
def handle_t_bfeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｂ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[1] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_GE_1)
def handle_t_cfeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_GE_3)
def handle_t_cfeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_GE_5)
def handle_t_cfeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_GE_7)
def handle_t_cfeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_L_1)
def handle_t_cfeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_L_3)
def handle_t_cfeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_CFEEL_L_5)
def handle_t_cfeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｃ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[2] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_GE_1)
def handle_pfeel_ge_1(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_GE_3)
def handle_pfeel_ge_3(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_GE_5)
def handle_pfeel_ge_5(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_GE_7)
def handle_pfeel_ge_7(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_L_1)
def handle_pfeel_l_1(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_L_3)
def handle_pfeel_l_3(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.PFEEL_L_5)
def handle_pfeel_l_5(character_id: int) -> int:
    """
    校验角色是否Ｐ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[3] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_GE_1)
def handle_t_vfeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_GE_3)
def handle_t_vfeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_GE_5)
def handle_t_vfeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_GE_7)
def handle_t_vfeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_L_1)
def handle_t_vfeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_L_3)
def handle_t_vfeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_VFEEL_L_5)
def handle_t_vfeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｖ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[4] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_GE_1)
def handle_t_afeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_GE_3)
def handle_t_afeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_GE_5)
def handle_t_afeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_GE_7)
def handle_t_afeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_L_1)
def handle_t_afeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_L_3)
def handle_t_afeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_AFEEL_L_5)
def handle_t_afeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ａ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[5] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_GE_1)
def handle_t_ufeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_GE_3)
def handle_t_ufeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_GE_5)
def handle_t_ufeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_GE_7)
def handle_t_ufeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_L_1)
def handle_t_ufeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_L_3)
def handle_t_ufeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_UFEEL_L_5)
def handle_t_ufeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｕ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[6] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_GE_1)
def handle_t_wfeel_ge_1(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_GE_3)
def handle_t_wfeel_ge_3(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_GE_5)
def handle_t_wfeel_ge_5(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_GE_7)
def handle_t_wfeel_ge_7(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_L_1)
def handle_t_wfeel_l_1(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_L_3)
def handle_t_wfeel_l_3(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_WFEEL_L_5)
def handle_t_wfeel_l_5(character_id: int) -> int:
    """
    校验交互对象是否Ｗ感觉<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[7] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_GE_1)
def handle_s_ge_1(character_id: int) -> int:
    """
    校验角色是否施虐>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_GE_3)
def handle_s_ge_3(character_id: int) -> int:
    """
    校验角色是否施虐>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_GE_5)
def handle_s_ge_5(character_id: int) -> int:
    """
    校验角色是否施虐>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_GE_7)
def handle_s_ge_7(character_id: int) -> int:
    """
    校验角色是否施虐>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_L_1)
def handle_s_l_1(character_id: int) -> int:
    """
    校验角色是否施虐<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_L_3)
def handle_s_l_3(character_id: int) -> int:
    """
    校验角色是否施虐<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.S_L_5)
def handle_s_l_5(character_id: int) -> int:
    """
    校验角色是否施虐<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[24] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_GE_1)
def handle_t_s_ge_1(character_id: int) -> int:
    """
    校验交互对象是否施虐>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_GE_3)
def handle_t_s_ge_3(character_id: int) -> int:
    """
    校验交互对象是否施虐>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_GE_5)
def handle_t_s_ge_5(character_id: int) -> int:
    """
    校验交互对象是否施虐>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_GE_7)
def handle_t_s_ge_7(character_id: int) -> int:
    """
    校验交互对象是否施虐>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_L_1)
def handle_t_s_l_1(character_id: int) -> int:
    """
    校验交互对象是否施虐<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_L_3)
def handle_t_s_l_3(character_id: int) -> int:
    """
    校验交互对象是否施虐<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_S_L_5)
def handle_t_s_l_5(character_id: int) -> int:
    """
    校验交互对象是否施虐<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[24] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_GE_1)
def handle_m_ge_1(character_id: int) -> int:
    """
    校验角色是否受虐>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_GE_3)
def handle_m_ge_3(character_id: int) -> int:
    """
    校验角色是否受虐>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_GE_5)
def handle_m_ge_5(character_id: int) -> int:
    """
    校验角色是否受虐>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_GE_7)
def handle_m_ge_7(character_id: int) -> int:
    """
    校验角色是否受虐>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_L_1)
def handle_m_l_1(character_id: int) -> int:
    """
    校验角色是否受虐<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_L_3)
def handle_m_l_3(character_id: int) -> int:
    """
    校验角色是否受虐<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.M_L_5)
def handle_m_l_5(character_id: int) -> int:
    """
    校验角色是否受虐<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    if character_data.ability[25] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_GE_1)
def handle_t_m_ge_1(character_id: int) -> int:
    """
    校验交互对象是否受虐>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_GE_3)
def handle_t_m_ge_3(character_id: int) -> int:
    """
    校验交互对象是否受虐>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_GE_5)
def handle_t_m_ge_5(character_id: int) -> int:
    """
    校验交互对象是否受虐>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_GE_7)
def handle_t_m_ge_7(character_id: int) -> int:
    """
    校验交互对象是否受虐>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_L_1)
def handle_t_m_l_1(character_id: int) -> int:
    """
    校验交互对象是否受虐<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_L_3)
def handle_t_m_l_3(character_id: int) -> int:
    """
    校验交互对象是否受虐<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_M_L_5)
def handle_t_m_l_5(character_id: int) -> int:
    """
    校验交互对象是否受虐<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[25] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_GE_1)
def handle_t_submit_ge_1(character_id: int) -> int:
    """
    校验交互对象是否顺从>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_GE_3)
def handle_t_submit_ge_3(character_id: int) -> int:
    """
    校验交互对象是否顺从>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_GE_5)
def handle_t_submit_ge_5(character_id: int) -> int:
    """
    校验交互对象是否顺从>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_GE_7)
def handle_t_submit_ge_7(character_id: int) -> int:
    """
    校验交互对象是否顺从>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_L_1)
def handle_t_submit_l_1(character_id: int) -> int:
    """
    校验交互对象是否顺从<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_L_3)
def handle_t_submit_l_3(character_id: int) -> int:
    """
    校验交互对象是否顺从<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SUBMIT_L_5)
def handle_t_submit_l_5(character_id: int) -> int:
    """
    校验交互对象是否顺从<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[20] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LOVE_SENSE_TASTE_0)
def handle_t_love_sense_taste_0(character_id: int) -> int:
    """
    校验交互对象是否精爱味觉==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[26] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LOVE_SENSE_TASTE_1)
def handle_t_love_sense_taste_1(character_id: int) -> int:
    """
    校验交互对象是否精爱味觉==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[26] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SADISM_0)
def handle_t_sadism_0(character_id: int) -> int:
    """
    校验交互对象是否施虐狂==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[27] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_SADISM_1)
def handle_t_sadism_1(character_id: int) -> int:
    """
    校验交互对象是否施虐狂==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[27] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_MASOCHISM_0)
def handle_t_masochism_0(character_id: int) -> int:
    """
    校验交互对象是否受虐狂==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[28] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_MASOCHISM_1)
def handle_t_masochism_1(character_id: int) -> int:
    """
    校验交互对象是否受虐狂==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[28] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_OESTRUS_0)
def handle_t_oestrus_0(character_id: int) -> int:
    """
    校验交互对象是否发情期==0
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[130] == 0:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_OESTRUS_1)
def handle_t_oestrus_1(character_id: int) -> int:
    """
    校验交互对象是否发情期==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.talent[130] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_L_1)
def handle_t_lubrication_l_1(character_id: int) -> int:
    """
    校验交互对象是否润滑<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_GE_3)
def handle_t_lubrication_ge_3(character_id: int) -> int:
    """
    校验交互对象是否润滑>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_GE_1)
def handle_t_lubrication_ge_1(character_id: int) -> int:
    """
    校验交互对象是否润滑>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_GE_5)
def handle_t_lubrication_ge_5(character_id: int) -> int:
    """
    校验交互对象是否润滑>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_GE_7)
def handle_t_lubrication_ge_7(character_id: int) -> int:
    """
    校验交互对象是否润滑>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_L_3)
def handle_t_lubrication_l_3(character_id: int) -> int:
    """
    校验交互对象是否润滑<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_LUBRICATION_L_7)
def handle_t_lubrication_l_7(character_id: int) -> int:
    """
    校验交互对象是否润滑<7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.status_data[8] < 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_GE_1)
def handle_t_exhibit_ge_1(character_id: int) -> int:
    """
    校验交互对象是否露出>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_GE_3)
def handle_t_exhibit_ge_3(character_id: int) -> int:
    """
    校验交互对象是否露出>=3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] >= 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_GE_5)
def handle_t_exhibit_ge_5(character_id: int) -> int:
    """
    校验交互对象是否露出>=5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] >= 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_GE_7)
def handle_t_exhibit_ge_7(character_id: int) -> int:
    """
    校验交互对象是否露出>=7
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] >= 7:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_L_1)
def handle_t_exhibit_l_1(character_id: int) -> int:
    """
    校验交互对象是否露出<1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] < 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_L_3)
def handle_t_exhibit_l_3(character_id: int) -> int:
    """
    校验交互对象是否露出<3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] < 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_EXHIBIT_L_5)
def handle_t_exhibit_l_5(character_id: int) -> int:
    """
    校验交互对象是否露出<5
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[23] < 5:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAPPY_MARK_1)
def handle_t_happy_mark_1(character_id: int) -> int:
    """
    校验交互对象是否快乐刻印==1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[13] == 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAPPY_MARK_2)
def handle_t_happy_mark_2(character_id: int) -> int:
    """
    校验交互对象是否快乐刻印==2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[13] == 2:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAPPY_MARK_3)
def handle_t_happy_mark_3(character_id: int) -> int:
    """
    校验交互对象是否快乐刻印==3
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[13] == 3:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAPPY_MARK_GE_1)
def handle_t_happy_mark_ge_1(character_id: int) -> int:
    """
    校验交互对象是否快乐刻印>=1
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[13] >= 1:
        return 1
    return 0


@add_premise(constant_promise.Premise.T_HAPPY_MARK_LE_2)
def handle_t_happy_mark_le_2(character_id: int) -> int:
    """
    校验交互对象是否快乐刻印<=2
    Keyword arguments:
    character_id -- 角色id
    Return arguments:
    int -- 权重
    """
    character_data = cache.character_data[character_id]
    target_data = cache.character_data[character_data.target_character_id]
    if target_data.ability[13] <= 2:
        return 1
    return 0
