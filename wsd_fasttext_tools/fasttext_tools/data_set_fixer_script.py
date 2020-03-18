import json
# import click
#
#
# @click.command()
# @click.option('label_file_path', '--label-path', type=click.Path(),
#               help='The file where the label info is stored (name of each label and the corresponding number key')
# @click.option('key_file_path', '--key-path', type=click.Path(), help='The file with a key nummber per line')
# @click.option('data_file_path', '--data-path', type=click.Path(), help='The file with the test or training data')
# @click.option('output_file', '--output-path', type=click.Path(), help='Output file')
def main(label_file_path, key_file_path, data_file_path, output_file):
    with open(label_file_path) as f:
        labels = json.load(f)

    with open(key_file_path) as f:
        f_data = f.read()
        key_list = f_data.split("\n")

    with open(data_file_path) as f:
        f_data = f.read()
        data = f_data.split("\n")

    out = ""
    counter = 0
    for sentence in data:
        tmp = sentence.split("\t")
        key = key_list[counter]
        label = labels[key]
        label = "__label__" + label.replace("_", "__") + "__"
        label = label.replace('(', '')
        label = label.replace(')', '')
        out += label + " " + tmp[1] + "\n"
        counter += 1

    print(str(counter) + " lines processed")

    with open(output_file, "w") as f:
        f.write(out)

if __name__ == '__main__':
    main()
