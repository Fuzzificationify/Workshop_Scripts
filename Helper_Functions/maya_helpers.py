# Helper functions for general purpose Maya things
import maya.cmds as mc
import pymel.core as pm
import difflib

def find_closest_match(possibilities, word):
    n = 1
    cutoff = 0.8

    closest_match = difflib.get_close_matches(word, possibilities, n, cutoff)
    print('closest_match', closest_match)
    return closest_match[0]


def switch_substring(source_list, source_substring, target_substring):
    target_list = []
    print('source_list', source_list)
    print('source_substring', source_substring)
    print('target_substring', target_substring)

    for obj in source_list:
        target_obj = obj.replace(source_substring, target_substring)
        target_list.append(target_obj)

    return target_list

def namespace_check(source):
    # Check if there's a namespace
    obj = pm.ls(source)[0]

    namespace = obj.namespace() or []
    if namespace == []:
        print("No Namespace")
        return False
    elif namespace:
        return True

def switch_namespace_selection(source_sel, target_sel):

    if type(source_sel) is not list:
        source_sel = [source_sel]
    if type(target_sel) is not list:
        target_sel = [target_sel]

    source_namespace = source_sel[0].rpartition(":")[0]
    target_namespace = target_sel[0].rpartition(":")[0]

    if source_namespace == target_namespace:
        print("Same namespace, exiting")
        return False

    else:
        target_list = switch_substring(source_sel, source_namespace, target_namespace)

        return target_list


def get_substring_difference(source, target):

    comparison = [(source, target)]
    print('source', source)
    print('target', target)
    old_substring = ""
    new_substring = ""

    for source_obj, target_obj in comparison:

        for index, diff in enumerate(difflib.ndiff(source_obj, target_obj)):

            if diff[0] == '-':
                old_substring += (diff[-1])
            elif diff[0] == '+':
                new_substring += (diff[-1])

    print(old_substring, new_substring)
    return old_substring, new_substring


# def get_delta_substrings(string1, string2):
#     diff = difflib.ndiff(string1, string2)
#     print('{}:{}'.format('string1:', string1))
#     print('{}:{}'.format('string2:', string2))
#
#     minus_diff = []
#     plus_diff = []
#
#     i = 0
#     consecutive = 0
#
#     for change in diff:
#         if change[0] == "-":
#             if (consecutive != 0) and (i > seq + 1):
#                 continue
#             else:
#                 minus_diff.append(change[-1])
#                 consecutive = i
#
#         elif change[0] == "+":
#             plus_diff.append(change[-1])
#
#         i = i + 1
#
#     minus_string = "".join(minus_diff)
#     plus_string = "".join(plus_diff)
#
#     print('{}:{}'.format('minus_string:', minus_string))
#     print('{}:{}'.format('plus_string:', plus_string))
#
#     return minus_string, plus_string


def get_delta_substrings(string1, string2):
    diff = difflib.ndiff(string1, string2)

    minus_diff = []
    plus_diff = []

    i = 0
    first_hit = 0
    last_hit = 0
    consecutive = 0

    first_hitP = 0
    consecutiveP = 0

    for change in diff:
        if change[0] == "-":
            if (consecutive != 0) and (i > consecutive + 1):
                continue
            else:
                minus_diff.append(change[-1])
                consecutive = i

                if first_hit == 0:
                    first_hit = i
                last_hit = i

        elif change[0] == "+":
            if (consecutiveP != 0) and (i > consecutiveP + 1):
                continue
            else:
                plus_diff.append(change[-1])
                consecutiveP = i

                if first_hitP == 0:
                    first_hitP = i

        i = i + 1

    minus_string = "".join(minus_diff)
    plus_string = "".join(plus_diff)


    return first_hit, last_hit, plus_string, minus_string


def smart_switch(obj_list, first_hit, last_hit, plus_string, minus_string):
    new_objs_ls = []
    for obj in obj_list:
        new_obj = smart_splitter(obj, first_hit, last_hit, minus_string, plus_string)
        new_objs_ls.append(new_obj)

    return new_objs_ls


def smart_splitter(string, first_hit, last_hit, old_string, new_string):
    string_head = string[:first_hit - 1]
    string_delta = string[first_hit - 1:last_hit + 2]
    string_tail = string[last_hit + 2:]

    print('{}: {}'.format('string_head',string_head))
    print('{}: {}'.format('string_delta',string_delta))
    print('{}: {}'.format('string_tail',string_tail))
    print('{}: {}'.format('old_string',old_string))
    print('{}: {}'.format('new_string',new_string))


    new_string_delta = string_delta.replace(old_string, new_string, 1)
    new_string = string_head + new_string_delta + string_tail

    return new_string
