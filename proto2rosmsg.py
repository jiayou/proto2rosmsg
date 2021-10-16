#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:32:28 2021

@author: jiayou
"""

import os
import argparse

def vprint(*args):
    if os.getenv('VERBOSE'):
        print(args)

# convert proto to ros message
def type_translate(type_str):
    return type_str

def ros_signal(text):
    tokens = text.strip().split()
    if len(tokens) < 3:
        return None
    
    if tokens[0] == 'optional' or tokens[0] == 'required':
        return type_translate(tokens[1]) + ' ' + tokens[2] + "\n"
    elif tokens[0] == 'repeated':
        return type_translate(tokens[1]) + '[] ' + tokens[2] + "\n"
    else:
        return None

def proto2_to_rosmsg(proto_file, out_dir):
    current_message = None
    current_file = None
    
    with open(proto_file) as f:
        for line in f.readlines():
            vprint(">>>> "+ line)
            if line.startswith('message '):
                assert current_message is None
                
                if line.endswith('{}'):
                    print(f"### WARNING: empty message? line={line}")
                    continue
                
                current_message = line.strip().lstrip('message ').rstrip('{').strip()
                ros_msg_file = os.path.join(out_dir, current_message+'.msg')
                if os.path.exists(ros_msg_file):
                    print("### WARNING: message exists: " + current_message)
                current_file = open(ros_msg_file, 'w')
                continue
            
            if line.startswith('}'):
                assert current_message is not None
                current_file.close()
                current_message = None
                continue
            
            newline=ros_signal(line)
            if newline is None:
                print(f"### WARNING: skipped signal in {current_message}, line={line}")
                # os.system(f'cat {proto_file}')
                continue
                
            vprint(newline)
            current_file.write(newline)

def pre_process(filename, out_dir):
    tempfile = os.path.join(out_dir, '.temp.proto')
    cmd = "cat {} | grep -v ^syntax | grep -v ^import | grep -v ^package | sed '/\/\*/,/*\//d' | sed 's|//.*$||g' | sed -E 's/^[ \\t]+//g' | sed -E 's/[ \\t]+$//g' | sed -E '/^$/d' | sed 's/=.*$//g' | sed '/^enum.*{{/,/^}}/d' | sed '/^oneof.*{{/,/^}}/d' > {}".format(filename, tempfile)
    
    vprint(cmd)
    """
        remove comments
        strip spaces
        remove empty lines
        remove signal index
        remove enumeration
    """
    
    ret = os.system(cmd)
    assert ret==0
    assert os.path.exists(tempfile)
    return tempfile
    
"""
usage: proto2rosmsg.py [-h] [--output OUTPUT] filename

Convert protobuf.proto to ROS messages

positional arguments:
  filename              proto file name (*.proto)

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        ROS message output folder (default:
                        /tmp/proto2rosmsg/msg)

"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert protobuf.proto to ROS messages')
    parser.add_argument('filename', help='proto file name (*.proto)')
    parser.add_argument('--output', '-o', default="/tmp/proto2rosmsg/msg",
                        help='ROS message output folder (default: /tmp/proto2rosmsg/msg)')

    args = parser.parse_args()
    print(args)
    filename = args.filename
    out_dir = args.output
    
    # check proto version: only proto2 is supported
    ret = os.system(f"cat {filename} | grep ^syntax | grep -qc proto2")
    if ret != 0:
        print(f"### ERROR: {filename} is not proto2 file")
        exit()

    os.makedirs(out_dir, exist_ok=True)
    tempfile = pre_process(filename, out_dir)
    try:
        proto2_to_rosmsg(tempfile, out_dir)
    except Exception as e:
        print("================================================================")
        print(f"ERROR PROCESS {filename}")
        print("================================================================")
        os.system(f"cat {tempfile}")
        print("================================================================")
        raise(e)
        
    os.remove(tempfile)
