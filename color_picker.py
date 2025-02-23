def main():
    colors_nbr = int(input("How many color palettes do you need ? (int) "))
    first_color_id = int(input("What is the ID of the first ColorPalette ? (int) "))
    groups_nbr = int(input("How many groups do you have ? (int) "))
    first_group_id = int(input("What is the ID of the first group ? (int) "))
    first_macro = int(input("What is the ID of the first macro you want to use ? (int) "))
    first_chan = int(input(f"What is the ID of the first loopback channel you want to use ? (int)\n This tool will use {colors_nbr*(groups_nbr+1)*2} loopback Channels \n"))
    magic_sheet_id = int(input("What is the ID of the magic sheet you want to use ? (int)"))
    
    with open("macros.asc", "w") as file:
        """CURRENT COLORS"""
        # Needed for file to work properly
        file.write("""Ident 3:0 \nManufacturer ETC\nConsole Eos\n$$Format 3.20\n$$Software Version 3.2.9 Build 16  Fixture Library 3.2.8.12, 31.Jul.2024\n \n""")
        current_chan = first_chan
        real_first_chan = first_chan
        current_macro = first_macro

        #Generating Macros for ALL groups
        file.write("!Generating macros for All groups \n")
        for c in range(colors_nbr):
            color_id = c + first_color_id
            file.write(generate_color_changing_all_macro(current_macro, groups_nbr, colors_nbr, color_id, first_chan, first_chan+colors_nbr-1, current_chan))
            current_chan += 1
            current_macro +=1

        # Generating Macros for EACH group
        for g in range(groups_nbr):
            first_chan, last_chan = current_chan, current_chan + colors_nbr - 1
            group_id = g + first_group_id
            file.write(f"! Generating Macros for group {group_id} \n")
            for c in range(colors_nbr):
                color_id = c + first_color_id
                file.write(generate_color_changing_macro(current_macro, group_id, color_id, first_chan, last_chan, current_chan))
                current_chan += 1
                current_macro += 1
        
        """NEW COLORS"""
        # Generating Macros for NEW colors for ALL groups
        file.write("!Geberating new colors macros for ALL groups \n")
        first_chan = current_chan 
        for c in range(colors_nbr):
            color_id = c + first_color_id
            file.write(generate_color_changing_all_macro(current_macro, groups_nbr, colors_nbr, color_id, first_chan, first_chan+colors_nbr-1, current_chan))
            current_chan += 1
            current_macro += 1
        
        # Generating Macros for NEW colors for EACH group
        main_next_cp_id = first_color_id + colors_nbr
        for g in range(groups_nbr):
            first_chan, last_chan = current_chan, current_chan + colors_nbr - 1
            group_id = g + first_group_id
            file.write(f"! Generation Macros for NEW colors for group {group_id} \n")
            for c in range(colors_nbr):
                color_id = c + first_color_id
                file.write(genereate_next_color_macro(current_macro, group_id, color_id, main_next_cp_id, first_chan, last_chan, current_chan))
                current_chan += 1
                current_macro += 1

        """GO MACROS"""
        file.write("! Generating the GO Macros !! \n")
        file.write(generate_go_macro(current_macro, main_next_cp_id, groups_nbr, colors_nbr, first_group_id, real_first_chan))

        """MAGIC SHEET"""
        file.write(generate_magic_sheet(magic_sheet_id, real_first_chan, first_macro, groups_nbr, colors_nbr, 100, 100))
        # Making sure the file has the right ending
        file.write("\nEndData\n")



"""CURRENT COLOR MACROS """        
def generate_color_changing_macro(macro_id, group_id, cp_id, first_chan, last_chan, chan):
    """Function that generates macro for a specific group and a specific color palette"""
    return f"""$MacroDef {macro_id}
   Text group{group_id}CP{cp_id}
   $$MacroMode Background

   $$MacroContents Clear_CmdLine <Enter>
   $$MacroContents Chan {first_chan} Thru {last_chan} @ 0 <Enter>
   $$MacroContents Chan {chan} @ Full <Enter>
   $$MacroContents Group {group_id} Color_Palette {cp_id} <Enter>
   $$MacroContents Clear_CmdLine <Enter>\n \n"""

def generate_color_changing_all_macro(macro_id, groups_nbr, colors_nbr, cp_id, first_chan, last_chan, chan):
    """Function that generates macro for a specific color palette but for ALL groups"""
    result = f"""$MacroDef {macro_id}
   Text ALLCP{cp_id}
   $$MacroMode Background \n
   $$MacroContents Chan {first_chan} Thru {last_chan} @ 0 <Enter>
   $$MacroContents Chan {chan} @ Full <Enter>\n"""

    for i in range(groups_nbr):
        result += f"""   $$MacroContents Macro_Button {macro_id+colors_nbr*(i+1)} <Enter>\n"""
    
    return result +  """   $$MacroContents Clear_CmdLine <Enter>\n \n"""




"""PREPARING NEW COLORS MACROS"""
def genereate_next_color_macro(macro_id, group_id, cp_id, main_cp, first_chan, last_chan, chan):
    """Function that generates a macro for a specific group to prepare your color change"""
    return f"""$MacroDef {macro_id}
   Text group{group_id}CP{cp_id}NEXT
   $$MacroMode Background

 
   $$MacroContents Clear_CmdLine <Enter>
   $$MacroContents Chan {first_chan} Thru {last_chan} @ 0 <Enter>
   $$MacroContents Chan {chan} @ Full <Enter>
   $$MacroContents Blind Color_Palette {main_cp} <Enter>
   $$MacroContents Group {group_id} Color_Palette {cp_id} <Enter>
   $$MacroContents Live
   $$MacroContents Clear_CmdLine <Enter>\n \n"""

def generate_go_macro(macro_id, main_cp, groups_nbr, colors_nbr, first_group, first_chan):
    """Generate the go macro"""
    first_bank_first_chan, first_bank_last_chan = first_chan, first_chan + (groups_nbr+1)*colors_nbr - 1 # We add 1 to groups nbr because we have the ALL group
    second_bank_first_chan, second_bank_last_chan = first_bank_last_chan + 1, first_bank_last_chan + (groups_nbr+1)*colors_nbr
    result = """"""
    for time in (0, 1, 3):
        result += f"""   $MacroDef {macro_id}
   Text GO {time} sec
   $$MacroMode Background
    
   $$MacroContents Clear_CmdLine <Enter>
   $$MacroContents Manual Color Time {time} <Enter>
   $$MacroContents Group {first_group} Thru {first_group+groups_nbr} Color_Palette {main_cp} <Enter>
   $$MacroContents Manual Color Time 0 <Enter>
   $$MacroContents Chan {first_bank_first_chan} Thru {first_bank_last_chan} Recall_From {second_bank_first_chan} Thru {second_bank_last_chan} <Enter>
   $$MacroContents Chan {second_bank_first_chan} Thru {second_bank_last_chan} @ 0 <Enter>
   $$MacroContents Delete Color_Palette {main_cp} <Enter> <Enter>
   $$MacroContents Chan {first_bank_first_chan} Record Color_Palette {main_cp} <Enter>
   $$MacroContents Clear_CmdLine <Enter>\n \n"""
        macro_id += 1
    return result


"""MAGIC SHEET AUTO GENERATION"""
def generate_magic_sheet(ms_id, first_chan, first_macro, groups_nbr, colors_nbr, start_x, start_y):
    color_array = []
    with open("colors.txt", "r") as colors:
        for line in colors.read().splitlines():
            color_array.append(line)

    result = f"""$MagicSheet {ms_id}
   $$Data Pen #ff484452 3 1 0
   $$Data Brush #ff0f1923 1 0
   $$Data LiveBG Color #ff000000 #ff0f1923
   $$Data BlindBG Color #ff0f1923 #ff1e3246 \n \n"""

    # FURTUR COLOR GRID
    first_next_macro = first_macro + (groups_nbr+1)*colors_nbr
    first_next_chan = first_chan + (groups_nbr+1)*colors_nbr
    for group in range(groups_nbr+1):
        result += f"! Group {group} LABEL\n"
        result += f"""   $$MSItem Text
   $$Data Text {"GROUP"+str(group) if group != 0 else "ALL"}
   $$Data Pos {start_x-90} {start_y + 80*group + 20}
   $$Data Rect 0 0 90 20
   $$Data Pen #00000000 3 0 0
   $$Data TextPen #ffffffff 1 1 0
   $$Data Font Tahoma
   $$Data FontAttr 21 0 0 0 132 ! HC VC
   $$Data Fields 1 0 ! ExtRelativeUpright"""

        for color in range(colors_nbr):
            x, y = start_x + 80*color, start_y + 80*group
            result += f"""   ! Triangle Targeting channel NEXT {first_next_chan+group*colors_nbr + color}
   $$MSItem Triangle
   $$Data Pos {x+2} {y+2}
   $$Data Mode 1 ! Target
   $$Data Rect 0 0 56 56
   $$Data Brush #ff{color_array[color]} 1 3
   $$Data Target 20 -1 {first_next_chan + group*colors_nbr + color} ! Manual
   $$Data Fields 4 0 ! IntRelative
   $$Data Vert 56 4
   $$Data Vert 4 56
   $$Data Vert 56 56

   ! Triangle Targeting channel CURRENT {first_chan+group*colors_nbr + color}
   $$MSItem Triangle
   $$Data Pos {x+2} {y+2}
   $$Data Mode 1 ! Target
   $$Data Rect 0 0 56 56
   $$Data Brush #ff{color_array[color]} 1 3
   $$Data Target 20 -1 {first_chan + group*colors_nbr + color} ! Manual
   $$Data Fields 4 0 ! IntRelative
   $$Data Vert 4 4
   $$Data Vert 56 4
   $$Data Vert 4 56

   ! Macro Targeting Channel {first_next_chan+group*colors_nbr + color}
   $$MSItem Button
   $$Data Mode 1 ! Target
   $$Data Pos {x} {y}
   $$Data Rect 0 0 60 60
   $$Data Pen #ff{color_array[color]} 6 1 0
   $$Data Target 4 -1 {first_next_macro + group*colors_nbr + color} ! Macro
   $$Data Fields 4 0 ! IntRelative \n \n"""

    # CURRENT COLOR GRID
    start_x += 80*(colors_nbr+3)
    for group in range(groups_nbr+1):
        result += f"! Group {group} LABEL\n"
        result += f"""   $$MSItem Text
   $$Data Text {"GROUP"+str(group) if group != 0 else "ALL"}
   $$Data Pos {start_x-90} {start_y + 80*group + 20}
   $$Data Rect 0 0 90 20
   $$Data Pen #00000000 3 0 0
   $$Data TextPen #ffffffff 1 1 0
   $$Data Font Tahoma
   $$Data FontAttr 21 0 0 0 132 ! HC VC
   $$Data Fields 1 0 ! ExtRelativeUpright"""

        for color in range(colors_nbr):
            x, y = start_x + 80*color, start_y + 80*group
            result += f"""! SQUARE Targeting channel {first_chan+group*colors_nbr + color}
   $$MSItem Button
   $$Data Mode 1 ! Target
   $$Data Pos {x} {y}
   $$Data Rect 0 0 60 60
   $$Data Brush #ff{color_array[color]} 1 3
   $$Data Target 20 -1 {first_chan + group*colors_nbr + color} ! Manual
   $$Data Fields 4 0 ! IntRelative

   ! Macro Targeting Channel {first_chan+group*colors_nbr + color}
   $$MSItem Button
   $$Data Mode 1 ! Target
   $$Data Pos {x} {y}
   $$Data Rect 0 0 60 60
   $$Data Pen #ff{color_array[color]} 6 1 0
   $$Data Target 4 -1 {first_macro + group*colors_nbr + color} ! Macro
   $$Data Fields 4 0 ! IntRelative \n \n"""

    return result + "\n \n"

if __name__ == "__main__" :
    main()