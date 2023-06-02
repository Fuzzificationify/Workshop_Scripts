import re
import pymel.core as pm

selection = pm.ls(sl=1)[0]
sel_namespace = selection.namespace()[:-1]

path = r'C:\Users\jono.tillson\Desktop\dog_clips\layers'
filename = r"tail_flick.ma"
sub_folder = "\\" + sel_namespace
sub_path = path + sub_folder
dupfile_path = sub_path + sub_folder + "_" + filename

def make_folder(sub_path):
    if not os.path.exists(sub_path):
        os.makedirs(sub_path)

def find_namespace_from_file(filedata):
    sub_str = r'"\w+:'  # regex voodoo

    temp_obj = re.compile(sub_str)
    found_namespace = temp_obj.findall(filedata)
    print(found_namespace[0][1:])

    return found_namespace[0][1:] # [1:] to remove the leading " sign

def rewrite_file():
    with open(path + "\\" + filename, 'r') as firstfile, open(dupfile_path, 'w') as dupfile:
        filedata = firstfile.read()
        og_namespace = find_namespace_from_file(filedata)
        filedata = filedata.replace(og_namespace, sel_namespace + ":")
        # read content from first file
        for line in filedata:
            # write content to second file
            dupfile.write(line)


make_folder(sub_path)
rewrite_file()
mc.file(dupfile_path, i=1, mergeNamespacesOnClash=1, namespace=":")
