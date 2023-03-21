read_file = 'D:\omd\shots\c190\scenes\c190_t002.ma'
write_file = 'D:\omd\shots\c190\scenes\c190_t002_PY2.ma'


with open(read_file, 'r') as file:
    # read the entire file as a string
    file_contents = file.read()

o_txt_0 = '''file -r -ns "BG01" -dr 1 -rfn "BG01RN" -op "VERS|2020|UVER|undef|MADE|undef|CHNG|Mon, Jan 23, 2023 03:12:29 PM|ICON|undef|INFO|undef|OBJN|3843|INCL|undef(|LUNI|cm|TUNI|ntscf|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "/Users/tom/Documents/maya/projects/omd//assets/BG/BG01/scenes/BG01.mb";'''
n_txt_0 = '''file -r -ns "BG01" -dr 1 -rfn "BG01RN" -op "VERS|2020|UVER|undef|MADE|undef|CHNG|Mon, Jan 23, 2023 03:12:29 PM|ICON|undef|INFO|undef|OBJN|3843|INCL|undef(|LUNI|cm|TUNI|ntscf|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "D:/omd//assets/BG/BG01/scenes/BG01.mb";'''

o_txt_1 = '''file -r -ns "JIN" -dr 1 -rfn "JINRN" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/CH/JIN/scenes/JIN.ma";'''
n_txt_1 ='''file -r -ns "JIN" -dr 1 -rfn "JINRN" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/CH/JIN/scenes/JIN.ma";'''

o_txt_2 = '''file -r -ns "JINgun" -dr 1 -rfn "JINgunRN" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/PR/JINgun/scenes/JINgun.ma";'''
n_txt_2 = '''file -r -ns "JINgun" -dr 1 -rfn "JINgunRN" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/PR/JINgun/scenes/JINgun.ma";'''

o_txt_3 = '''file -r -ns "CLEO" -dr 1 -rfn "CLEORN" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/CH/CLEO/scenes/CLEO.ma";'''
n_txt_3 = '''file -r -ns "CLEO" -dr 1 -rfn "CLEORN" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/CH/CLEO/scenes/CLEO.ma";'''

o_txt_4 = '''file -r -ns "CLEOknife" -dr 1 -rfn "CLEOknifeRN" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/PR/CLEOknife/scenes/CLEOknife.ma";'''
n_txt_4 = '''file -r -ns "CLEOknife" -dr 1 -rfn "CLEOknifeRN" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/PR/CLEOknife/scenes/CLEOknife.ma";'''

o_txt_5 = '''file -r -ns "CLEOgun" -dr 1 -rfn "CLEOgunRN" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/PR/CLEOgun/scenes/CLEOgun.ma";'''
n_txt_5 = '''file -r -ns "CLEOgun" -dr 1 -rfn "CLEOgunRN" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/PR/CLEOgun/scenes/CLEOgun.ma";'''

o_txt_6 = '''file -r -ns "CLEOknife1" -dr 1 -rfn "CLEOknifeRN1" -op "v=0;" -typ "mayaAscii" "/Users/tom/Documents/maya/projects/omd//assets/PR/CLEOknife/scenes/CLEOknife.ma";'''
n_txt_6 = '''file -r -ns "CLEOknife1" -dr 1 -rfn "CLEOknifeRN1" -op "v=0;" -typ "mayaAscii" "D:/omd//assets/PR/CLEOknife/scenes/CLEOknife.ma";'''

text_replacements = [(o_txt_0, n_txt_0), (o_txt_1, n_txt_1), (o_txt_2, n_txt_2), (o_txt_3, n_txt_3), (o_txt_4, n_txt_4), (o_txt_5, n_txt_5), (o_txt_6, n_txt_6)]

for old_text, new_text in text_replacements:
    file_contents = file_contents.replace(old_text, new_text)


with open(write_file, 'w') as file:
    file.write(file_contents)

