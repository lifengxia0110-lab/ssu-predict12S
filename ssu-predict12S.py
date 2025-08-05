import os
import subprocess



input_file = input("Please enter the path to the .fasta file:")
output_directory = input("Please enter the path where the prediction result directory is stored:")
cmfile = input("Please enter the name of the .cm file:")

def split_fasta(input_file, output_directory):
    with open(input_file, 'r') as fasta_file:
        lines = fasta_file.readlines()

    rna_name = None
    rna_sequence = None
    rna_names = []

    for line in lines:
        line = line.strip()

        if line.startswith('>'):
            if rna_name and rna_sequence:
                save_fas_file(rna_name, rna_sequence, output_directory)
            rna_name = line[1:]
            rna_sequence = ''
            # Add RNA name to the list
            rna_names.append(rna_name)
        else:
            rna_sequence += line

    if rna_name and rna_sequence:
        save_fas_file(rna_name, rna_sequence, output_directory)
# Write the RNA name into a .txt file
    txt_file = os.path.join(output_directory, "code.txt")
    with open(txt_file, "w", encoding='utf-8', newline='\n') as txtfile:
        for rna_name in rna_names:
            txtfile.write("ssu-align -m "+cmfile+".cm " + rna_name + ".fas " + rna_name + "\n")

def save_fas_file(rna_name, rna_sequence, output_directory):

    output_file = os.path.join(output_directory, f"{rna_name}.fas")

    # Write RNA sequence information into output file
    with open(output_file, "w") as outfile:
        outfile.write(f">{rna_name}\n")
        outfile.write(rna_sequence)

# Call the function to extract RNA sequence information and store it in the corresponding. fas and. txt files
split_fasta(input_file, output_directory)
os.chdir(output_directory)
subprocess.run("bash -c 'source code.txt'", shell=True)
print("Successful prediction")

# Process the prediction results in the .stk file
def find_matching_left_bracket(input_str, right_index):
    count = 1  # Count of unmatched ')' characters
    for i in range(right_index - 1, -1, -1):
        if input_str[i] == ')':
            count += 1
        elif input_str[i] == '(':
            count -= 1
            if count == 0:
                return i
    return -1


def find_matching_right_bracket(input_str, left_index):
    count = 1  # Count of unmatched '(' characters
    for i in range(left_index + 1, len(input_str)):
        if input_str[i] == '(':
            count += 1
        elif input_str[i] == ')':
            count -= 1
            if count == 0:
                return i
    return -1


def find_matching_bracket(input_str, index):
    Index = -1
    if input_str[index] == "(":
        Index = find_matching_right_bracket(input_str, left_index=index)
    if input_str[index] == ")":
        Index = find_matching_left_bracket(input_str, right_index=index)
    return Index


def replace_character(input_string, index, replacement='.'):
    if index < 0 or index >= len(input_string):
        # If the index exceeds the string range, no replacement will be performed
        return input_string
    else:
        return input_string[:index] + replacement + input_string[index + 1:]

directory_path = output_directory
predict_path = input("Please enter the path to store the cleaned files:")
# Retrieve all files and subdirectories in the specified directory
last_part = os.path.basename(directory_path)
all_files = os.listdir(directory_path)

# Traverse all files and subdirectories
for file_name in all_files:
    full_path = os.path.join(directory_path, file_name)
    # Check if it is a directory
    if os.path.isdir(full_path):
        # Retrieve a list of files in the directory that end with. stk
        stk_files = [file for file in os.listdir(full_path) if file.endswith('.stk')]

        for stk_file in stk_files:
            file_path = os.path.join(full_path, stk_file)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # Process each row of data and perform further operations
                sequence = lines[3].split()[1]
                symbol = lines[5].split()[2]
                symbol = symbol.replace('<', '(')
                symbol = symbol.replace('>', ')')
                symbol = symbol.replace(':', '.')
                symbol = symbol.replace(',', '.')
                symbol = symbol.replace('[', '(')
                symbol = symbol.replace(']', ')')
                symbol = symbol.replace('-', '.')
                symbol = symbol.replace('_', '.')
                symbol = symbol.replace('{', '(')
                symbol = symbol.replace('}', ')')
                indices_to_remove = [i for i, char in enumerate(sequence) if char == '-' and symbol[i] != '.']

                if indices_to_remove != []:
                    D_char = []
                    for i in range(len(indices_to_remove)):
                        d_char = find_matching_bracket(symbol, indices_to_remove[i])
                        D_char.append(d_char)
                    # print(D_char)
                    for index in D_char:
                        symbol = replace_character(symbol, index, replacement='.')
            char_remove = [i for i, char in enumerate(sequence) if char == "-"]
            # Delete the corresponding subscript character in string 1
            string1_filtered = ''.join([char for i, char in enumerate(sequence) if i not in char_remove])
            # Delete the corresponding subscript character in string 2
            string2_filtered = ''.join([char for i, char in enumerate(symbol) if i not in char_remove])
            dirname = os.path.dirname(predict_path)
            dir_path = dirname
            folder_name = lines[3].split()[0]
            subfolder_path = os.path.join(predict_path, folder_name)
            # print(subfolder_path)
            os.makedirs(subfolder_path)
            final_name = folder_name + '.txt'
            final_path = os.path.join(subfolder_path, final_name)
            # print(final_path)
            with open(final_path, 'w') as file:
                file.write('>' + folder_name + '\n')
                file.write(string1_filtered + '\n')
                file.write(string2_filtered)
            all_fold = last_part + '.str'
            subfolderall_path = os.path.join(predict_path, all_fold)
            with open(subfolderall_path, 'a') as all_file:
                all_file.write('>' + folder_name + '\n')
                all_file.write(string1_filtered + '\n')
                all_file.write(string2_filtered + ' #FS' + '\n')


print("Cleaning Successful")
