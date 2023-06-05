import pymel.core as pm
import ast

from My_Tools import fileInfo_push_pull as info_pp

def get_namespace(obj):
    obj_namespace = obj.namespaceList()[0]

    return obj_namespace


# To get reference nodes, you only need the namespace
def get_ref(obj_namespace):
    ref_path = pm.FileReference(namespace=obj_namespace)
    ref_node = str( ref_path.refNode )

    return ref_node

# def make_dic(ref_list, ref_group_name="Group_1"):
#     ref_dic = {ref_group_name: ref_list}
#
#     return ref_dic

# def add_to_fileInfo(refs_key, dic):
#     str_dic = str_ify(dic)
#     pm.fileInfo(refs_key, str_dic)


def check_ref_grps_exists(refs_key):
    try:
        pm.fileInfo(refs_key, q=1)
        return True
    except:
        return False



def load_ref():
    pass

def unload_ref():
    pass


def main(info_key="My_Refs", info_grp="spikes"):
    data = info_pp.read_grp(info_key, info_grp)
    objs = pm.ls(data)

    ref_node_list = []

    for obj in objs:
        n_spc = get_namespace(objs)
        ref_node = get_ref(n_spc)

        ref_node_list.append(ref_node)

    print(f"Ref nodes: {ref_node_list}")

main()
