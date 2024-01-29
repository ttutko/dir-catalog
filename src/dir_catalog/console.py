import click
import os
import uuid
from os.path import join, getsize
from lxml import etree

from . import __version__

@click.command()
@click.option("--depth", default=0, help="Depth to traverse. When '0' (defualt), the entire subtree will be traversed.")
@click.option("-p", "--print", "dump_output", is_flag=True, default=False, help="Print paths to stdout.")
@click.argument('root_path')
@click.option("-o", "--output", "output_file_name", help="Output xml file.")
@click.option("--id", default=None, help="ID to associate with this file.")
@click.version_option(version=__version__)
def main(root_path, output_file_name, depth=0, dump_output=False, id=None):
    if id is None:
        id = uuid.uuid4().hex.replace("-","")

    if output_file_name is None:
        output_file_name = os.devnull

    with open(output_file_name, "wb") as f, etree.xmlfile(f, encoding='utf-8') as xf:
        xf.write_declaration()
        with xf.element("root"):
            with xf.element("metadata"):
                id_elem = etree.Element("id")
                id_elem.text = id
                xf.write(id_elem, pretty_print=True)
            
            with xf.element("entities"):

                if dump_output: 
                    print(f"Dumping directory: {root_path}:")
                current_depth = 1
                for root, dirs, files in os.walk(root_path):
                    # for dir in dirs:
                    #     print(f"{' ' * current_depth}{dir}")

                    if dump_output:
                        print(f"{' ' * current_depth}{root}")
                    for f in files:
                        if dump_output:
                            print(f"{' ' * current_depth}{f}")

                        with xf.element("current_entry"):
                            name = etree.Element("name")
                            name.text = f
                            xf.write(name, pretty_print=True)

                    if depth != 0 and current_depth >= depth:
                        break
                    
                    current_depth += 1



