import pymel.core as pm

char_group = pm.ls("walkers")

children = pm.listRelatives(char_group)
children_nsp_list = [child.namespace() for child in children]

ref_list = [pm.FileReference(namespace=nsp) for nsp in children_nsp_list]

for each in ref_list:
    each.load()




import pymel.core as pm
import ast

env_refs_list = mc.ls(sl=1)
str_ver = str(env_refs_list)

mc.fileInfo('env_refs', str_ver)

refos = mc.fileInfo('env_refs', q=1)[0]
clean_list = ast.literal_eval(refos)

mc.select(clean_list)


for ref in clean_list:
    ref_obj = pm.FileReference(refnode=ref)
    ref_obj.unload()


##################################################
# Get Unloaded Refs
# listReference creates FileReferences types, can run refNode, .load(), .unload()

unloaded_refs = pm.listReferences(unloaded=1)
ref_names = [ref.refNode.getName() for ref in unloaded_refs]
str_ref_names = str(ref_names)

pm.fileInfo('ref_names', str_ref_names)

refos = mc.fileInfo('ref_names', q=1)[0]
clean_list = ast.literal_eval(refos)

for ref in clean_list:
    ref_obj = pm.FileReference(refnode=ref)
    ref_obj.load()
