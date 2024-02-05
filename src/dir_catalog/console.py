from posix import write
import click
import os
import uuid
from os.path import join, getsize
from lxml import etree
from datetime import datetime
from pathlib import Path

from . import __version__


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formatted_date = d.isoformat(sep='T', timespec='milliseconds') + 'Z' # +  d.strftime('%d %b %Y')
    return formatted_date

@click.command()
@click.option("--depth", default=0, help="Depth to traverse. When '0' (defualt), the entire subtree will be traversed.")
@click.option("-p", "--print", "dump_output", is_flag=True, default=False, help="Print paths to stdout.")
@click.argument('root_path')
@click.option("-o", "--output", "output_file_name", help="Output xml file.")
@click.option("--id", default=None, help="ID to associate with this file.")
@click.option("--date", "collection_date", default=None)
@click.option("--include-hidden", "include_hidden", is_flag=True, default=False, help="Include hidden directories.")
@click.version_option(version=__version__)
def main(root_path, output_file_name, depth=0, dump_output=False, id=None, collection_date=None, include_hidden=False):
    print(f"INCLUDE HIDDEN: {include_hidden}")
    if id is None:
        id = uuid.uuid4().hex.replace("-","")

    if collection_date is None:
        collection_date = datetime.utcnow().isoformat(sep='T', timespec='milliseconds') + 'Z'

    if output_file_name is None:
        output_file_name = os.devnull

    with open(output_file_name, "wb") as f, etree.xmlfile(f, encoding='utf-8') as xf:
        xf.write_declaration()
        with xf.element("root"):
            with xf.element("metadata"):
                id_elem = etree.Element("id")
                id_elem.text = id
                collection_time_elem = etree.Element("collection_time")
                collection_time_elem.text = collection_date
                xf.write(id_elem, pretty_print=True)
                xf.write(collection_time_elem, pretty_print=True)
            
            with xf.element("entities"):

                if dump_output: 
                    print(f"Dumping directory: {root_path}:")
                current_depth = 1
                for root, dirs, files in os.walk(root_path):
                    if not include_hidden:
                        dirs = [d for d in dirs if not d.startswith('.')]
                    for dir in dirs:
                        with xf.element("current_entry"):
                            is_directory_element = etree.Element("is_directory")
                            is_directory_element.text = "true"
                            xf.write(is_directory_element, pretty_print=True)
                            is_directory_element = None
                            name = etree.Element("name")
                            name.text = dir
                            xf.write(name, pretty_print=True)
                            full_path_element = etree.Element("full_path")
                            full_path = os.path.join(root, dir)
                            full_path_element.text = full_path
                            stat_obj = os.stat(full_path)
                            size = stat_obj.st_size
                            size_elem = etree.Element("size")
                            size_elem.text = str(size)
                            xf.write(size_elem, pretty_print=True)
                            size_elem = None
                            last_modified = stat_obj.st_mtime
                            modified_elem = etree.Element("modified_date")
                            modified_elem.text = convert_date(last_modified)
                            xf.write(modified_elem, pretty_print=True)
                            modified_elem = None
                            if hasattr(stat_obj, "st_birthtime"):
                                created = stat_obj.st_birthtime

                            perms = oct(stat_obj.st_mode & 0o777)[2:]
                            xf.write(full_path_element, pretty_print=True)
                            permissions = etree.Element("permissions")
                            permissions.text = perms
                            xf.write(permissions, pretty_print=True)
                            permissions = None
                            name = None
                            
                            path_obj = Path(full_path)
                            owner = path_obj.owner()
                            group = path_obj.group()
                            group_elem = etree.Element("group")
                            group_elem.text = group
                            xf.write(group_elem, pretty_print=True)
                            group_elem = None
                            owner_elem = etree.Element("owner")
                            owner_elem.text = owner
                            xf.write(owner_elem, pretty_print=True)
                            owner_elem = None
                    #     print(f"{' ' * current_depth}{dir}")

                    if dump_output:
                        print(f"{' ' * current_depth}{root}")
                    for f in files:
                        if dump_output:
                            print(f"{' ' * current_depth}{f}")

                        with xf.element("current_entry"):
                            is_directory_element = etree.Element("is_directory")
                            is_directory_element.text = "false"
                            xf.write(is_directory_element, pretty_print=True)
                            is_directory_element = None
                            name = etree.Element("name")
                            name.text = f
                            xf.write(name, pretty_print=True)
                            full_path_element = etree.Element("full_path")
                            full_path = os.path.join(root, f)
                            full_path_element.text = full_path
                            stat_obj = os.stat(full_path)
                            size = stat_obj.st_size
                            size_elem = etree.Element("size")
                            size_elem.text = str(size)
                            xf.write(size_elem, pretty_print=True)
                            size_elem = None
                            last_modified = stat_obj.st_mtime
                            modified_elem = etree.Element("modified_date")
                            modified_elem.text = convert_date(last_modified)
                            xf.write(modified_elem, pretty_print=True)
                            modified_elem = None
                            if hasattr(stat_obj, "st_birthtime"):
                                created = stat_obj.st_birthtime

                            perms = oct(stat_obj.st_mode & 0o777)[2:]
                            xf.write(full_path_element, pretty_print=True)
                            permissions = etree.Element("permissions")
                            permissions.text = perms
                            xf.write(permissions, pretty_print=True)
                            permissions = None
                            name = None
                            
                            path_obj = Path(full_path)
                            owner = path_obj.owner()
                            group = path_obj.group()
                            group_elem = etree.Element("group")
                            group_elem.text = group
                            xf.write(group_elem, pretty_print=True)
                            group_elem = None
                            owner_elem = etree.Element("owner")
                            owner_elem.text = owner
                            xf.write(owner_elem, pretty_print=True)
                            owner_elem = None



                    if depth != 0 and current_depth >= depth:
                        break
                    
                    current_depth += 1



