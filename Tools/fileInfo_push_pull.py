import pymel.core as pm
import ast

"""
Structure Overview.
The fileInfo node only takes strings, so functions will use ast.literal to retreave data is it's
proper format.

In the fileInfo node:
Info_key, { Info_Group_Name : [Info_Group_List] }
             ^            Info_Dic            ^
Example:
My_References, { Hero_Characters : [Tommy_Rig, Alice_Rig], Background_Environment : [Kitchen, Garden, Table] } 
My_Selections, { Trees : [tree_01, tree_02, tree_03], Rocks : [rock_01, rock_02], Dynamic : [vine, splinter_01] }

"""




def str_ify(item):
    str_item = str(item)
    return str_item

def remove_dup(my_list):
    a_set = set(my_list)
    exclusive_list = list(a_set)

    return exclusive_list

def make_base_dic(info_key):
    dic = {}
    str_dic = str_ify(dic)
    pm.fileInfo(info_key, str_dic)

    return dic

def make_dic(item_list, info_group_name="Group_1"):
    item_dic = {info_group_name: item_list}

    return item_dic

def make_key_pair(key, values):
    temp_dic = {key:values}

    return temp_dic

def append_to_base_dic(dic, key_pair):
    dic.update(key_pair)

    return dic


def update_dic(info_key, info_dic, info_grp_name, data_list):
    if check_info_key_exists(info_key) == False:
        make_base_dic(info_key)

    if check_info_grp_exists(info_dic, info_grp_name) == False:
        new_info_dic = create_new_info_grp(info_dic, info_grp_name, data_list)

    # if grp_exists, append
    else:
        new_info_dic = update_info_grp(info_dic, info_grp_name, data_list)

    print("{}{}".format("new_info_dic: ", new_info_dic))
    return new_info_dic


# FileInfo Functions
def add_to_fileInfo(info_key, dic):
    str_dic = str_ify(dic)
    pm.fileInfo(info_key, str_dic)

def get_my_keys():
    # From all data in fileInfo, find my info_keys
    all_info = pm.fileInfo(q=1)
    my_keys = []

    for key, val in all_info:
        literal_val = ast.literal_eval(val)
        if type(literal_val) == dict:

            my_keys.append(key)

    return my_keys

def check_info_key_exists(info_key):
    try:
        pm.fileInfo(info_key, q=1)
        return True
    except:
        return False

# Get info dic from info key
def get_info_dic(info_key):
    info_dic_as_string = pm.fileInfo(info_key, q=1)
    info_dic = ast.literal_eval(info_dic_as_string)  # Convert back from string

    return info_dic



def check_info_grp_exists(info_dic, info_grp):
    if info_grp in info_dic.keys():
        return True
    else:
        return False

def get_info_grps(info_dic):
    info_groups = info_dic.keys()

    return info_groups



def get_info_grp_list(info_dic, info_grp):
    info_grp_list = info_dic[info_grp]

    return info_grp_list

# Grp list update functions:
def extend_to_grp_list(info_grp_list, new_item):
    info_grp_list.extend(new_item)
    info_grp_list = remove_dup(info_grp_list)

    return info_grp_list

def remove_from_grp_list(info_grp_list, item_list):
    for item in item_list:
        info_grp_list.remove(item)

    return info_grp_list

def replace_grp_list(info_grp_list, items):
    replacement_grp_list = items

    return replacement_grp_list


def update_info_dic(info_dic, info_group_name, new_list):
    info_dic[info_group_name] = new_list

    return info_dic

def update_info_grp(info_dic, info_grp_name, data_list, update_type="extend"):
    if update_type == "extend":
        update_func = extend_to_grp_list
    if update_type == "remove":
        update_func = remove_from_grp_list
    if update_type == "replace":
        update_func = replace_grp_list

    grp_list = get_info_grp_list(info_dic, info_grp_name)

    new_grp_list = update_func(grp_list, data_list)
    new_info_dic = update_info_dic(info_dic, info_grp_name, new_grp_list)

    return new_info_dic


def write_to_fileInfo(info_key, info_dic, info_group_name):
    string_dic = str_ify(info_dic)
    pm.fileInfo(info_key, string_dic)

def read_fileInfo(info_key):
    check_info_key_exists(info_key)

    info_dic = get_info_dic(info_key)
    grp_names = get_info_grps(info_dic)

    read_data_list = []

    for grp in grp_names:
        pretty_print(info_key, info_dic, grp)
        data = return_data(info_key, info_dic, grp)
        read_data_list.append(data)

    return read_data_list

def read_fileInfo_grp(info_key, info_grp):
    check_info_key_exists(info_key)

    info_dic = get_info_dic(info_key)

    pretty_print(info_key, info_dic, info_grp)
    data = return_data(info_key, info_dic, info_grp)

    return data

def remove_info_grp(info_dic, info_grp_name):
    info_dic.pop(info_grp_name, None)



def create_new_info_grp(info_dic, new_grp, new_grp_list):
    info_dic[new_grp] = new_grp_list

    return info_dic

def return_data(info_key, info_dic, info_grp):
    return info_dic[info_grp]

def pretty_print(info_key, info_dic, info_grp):

    print("////////////////////////")
    print("{}{}".format("Info Key  : ", info_key))
    print("{}{}".format("Info Group: ", info_grp))
    print("-----------------------")

    print(info_dic[info_grp])
    print("////////////////////////")


# Manual To Use Functions:
def clear_info_grp(info_key, info_grp_name):
    info_dic = get_info_dic(info_key)
    empty_list = []
    new_info_dic = update_info_dic(info_dic, info_grp_name, empty_list)

    add_to_fileInfo(info_key, new_info_dic)

    return new_info_dic

def select_info_grp(info_key, info_grp):
    dic = get_info_dic(info_key)

    grp_list = dic[info_grp]
    obj_list = pm.ls(grp_list)

    pm.select(obj_list)

    left_overs = [obj for obj in grp_list if obj not in obj_list]
    print("////////////////////////")
    print("Objects that weren't selected because they aren't in scene:")
    print(left_overs)




def main_add(info_key="my_selections", grp_name="spikes"):
    sel_list = mc.ls(sl=1) # mc is used so it's a list

    if check_info_key_exists(info_key) == False:
        info_dic = make_base_dic(info_key)
    else:
        info_dic = get_info_dic(info_key)

    if check_info_grp_exists(info_dic, grp_name) == False:
        new_info_dic = create_new_info_grp(info_dic, grp_name, sel_list)

    else:
        new_info_dic = update_info_grp(info_dic, grp_name, sel_list, update_type="extend")

    add_to_fileInfo(info_key, new_info_dic)

    pretty_print(info_key, new_info_dic, grp_name)


def main_remove(info_key="my_selections", grp_name="spikes"):
    sel_list = mc.ls(sl=1)

    if check_info_key_exists(info_key) == False:
        print("Info key doesn't exist")
        return

    info_dic = get_info_dic(info_key)

    if check_info_grp_exists(info_dic, grp_name) == False:
        print("Group Name doesn't exist")
        return


    new_info_dic = update_info_grp(info_dic, grp_name, sel_list, update_type="remove")

    add_to_fileInfo(info_key, new_info_dic)

    pretty_print(info_key, new_info_dic, grp_name)


def main_read(info_key="all", info_grp=""):
    data_list = []

    if info_key == "all":
        my_keys = get_my_keys()

        for key in my_keys:
            data = read_fileInfo(key)
            data_tup = (key, data)
            data_list.append(data_tup)

    else:
        data = read_fileInfo(info_key)
        data_tup = (info_key, data)
        data_list.append(data_tup)

    return data_list

def read_grp(info_key, info_grp):
    data = read_fileInfo_grp(info_key, info_grp)
    return data

#main_add()
wop = main_read()

#main_remove(info_key="my_selections", grp_name="spikes")
