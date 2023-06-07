import pymel.core as pm
import ast

from My_Tools import fileInfo_push_pull as info_pp

def get_namespace(obj):
    #obj_namespace = obj.namespaceList()[0]

    # Using string-base name space finding incase ref is unloaded
    obj_namespace = obj.rpartition(':')[0]

    return obj_namespace


# To get reference nodes, you only need the namespace
def get_ref(obj_namespace):
    ref_path = pm.FileReference(namespace=obj_namespace)
    ref_node = str( ref_path.refNode )

    return ref_node


def check_ref_grps_exists(refs_key):
    try:
        pm.fileInfo(refs_key, q=1)
        return True
    except:
        return False


def load_ref(node_list):
    for node in node_list:
        ref_obj = pm.FileReference(refnode=node)
        ref_obj.load()

def unload_ref(node_list):
    for node in node_list:
        ref_obj = pm.FileReference(refnode=node)
        ref_obj.unload()


def main(info_key="my_references", info_grp="env", unload=0, load=0):
    data = info_pp.read_grp(info_key, info_grp)
    ref_node_list = []

    for obj in data:
        n_spc = get_namespace(obj)
        ref_node = get_ref(n_spc)

        ref_node_list.append(ref_node)

    print(f"Ref nodes: {ref_node_list}")

    if load == 1:
        load_ref(ref_node_list)

    if unload == 1:
        unload_ref(ref_node_list)

main(info_key="my_references", info_grp="env", unload=1, load=0)
