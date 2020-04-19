import shutil
import os
import sys
import binascii
import argparse

PERSONALITIES_FOLDER = "Data\\Personalities"
# if not hasattr(sys, 'frozen'):
#     os.chdir("D:\\Games\\Chessmaster Grand Master Edition 1.20 RUS")

def backup():
    global PERSONALITIES_FOLDER
    backup_folder = os.path.join(PERSONALITIES_FOLDER, 'backup')
    print(PERSONALITIES_FOLDER)
    os.makedirs(backup_folder, exist_ok=True)
    for file in os.listdir(PERSONALITIES_FOLDER):
        # print(file)
        if not file.lower().endswith('.cmp'):
            continue
        backup_file = os.path.join(backup_folder, os.path.basename(file))
        # print(file, backup_file)
        if not os.path.exists(backup_file):
            shutil.copy(file, backup_file)
            # print("backed up ", file)
        # else:
        #     print(backup_file, "exists")

def replace_ply(personality_file, desirable_ply):
    global PERSONALITIES_FOLDER
    file_path = os.path.join(PERSONALITIES_FOLDER, 'backup', personality_file)
    if not os.path.exists(file_path):
        # print(file_path, 'does not exist')
        return 0
    with open(file_path, 'rb') as f:
        contents = f.read()
        hex_contents = binascii.hexlify(contents)
        parts = hex_contents.split(b'64000000')
        ply = parts[1][:2]
        part_num = 1
        if ply == b'00' or not ply:
            ply = parts[2][:2]
            part_num = 2
        try:
            dec_ply = int("0x"+ply.decode(), 0)
            # print(personality_file, ply, dec_ply)
        except:
            # print(personality_file, 'error. ply=', ply)
            return 0
        if desirable_ply>dec_ply:
            return 0
        parts[part_num] = hex(desirable_ply)[2:].zfill(2).encode() + parts[part_num][2:]
        hex_contents = b'64000000'.join(parts)
        contents = binascii.unhexlify(hex_contents)
        with open(os.path.join(PERSONALITIES_FOLDER, personality_file), 'wb') as fw:
            fw.write(contents)
        return 1


def replace_ply_for_all_personalities(folder, ply):
    modded_files = 0
    for file in os.listdir(folder):
        if not file.lower().endswith('.cmp'):
            continue
        modded_files += replace_ply(file,ply)
    print("Modded "+str(modded_files)+" personality files.")

def main():
    global PERSONALITIES_FOLDER
    parser = argparse.ArgumentParser(description="Change ply count for all personalities in Chessmaster X and Grandmaster")
    parser.add_argument('--cmpath', help="Folder where Chessmaster is installed.", default="")
    parser.add_argument('--ply', help="Max desirable ply for all personalities.", type=int)
    args = parser.parse_args()
    if not os.path.exists(PERSONALITIES_FOLDER) and not args.cmpath:
        print("Chessmaster personalities not found. Place this script into the folder where Chessmaster is installed or set the --cmpath parameter.")
        end()
    elif args.cmpath and not os.path.exists(args.cmpath):
        print("Path "+args.cmpath+" does not exist.")
        end()
    else:
        PERSONALITIES_FOLDER = os.path.join(args.cmpath, PERSONALITIES_FOLDER)
        if not os.path.exists(PERSONALITIES_FOLDER):
            print("Folder "+PERSONALITIES_FOLDER+" does not exist. Cannot fine personalities to modify.")
            end()
    if not args.ply:
        args.ply = int(input("Enter max desirable ply for all characters (10 is recommended)\n"))
    print("Making backup of original personalities...")
    backup()
    print("Will modify all personalities to use ply="+str(args.ply))
    print("Personalities with ply<"+str(args.ply)+" will not be modified.")
    replace_ply_for_all_personalities(PERSONALITIES_FOLDER, args.ply)
    end()

def end():
    os.system("pause")
    sys.exit()

if __name__=='__main__':
    main()
