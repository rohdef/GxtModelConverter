# 
# main.py
#  
# Author:
#       Rohde Fischer <rohdef@rohdef.dk>
# 
# Copyright (c) 2012 MIT X11
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import sys
import os
import os.path
import logging

def convert():
    recursive = False
    directories = []
    
    contents = sys.argv[1:] # remove the 
    
    if len(contents) < 3:
        index = 0
        
        if len(contents) == 2:
            if contents[0].lower() == "-r" or contents[0].lower() == "--recursive":
                recursive = True
                index = 1
            if contents[1].lower() == "-r" or contents[1].lower() == "--recursive":
                recursive = True
        
        folderCandidate = os.path.abspath(contents[index])
        if os.path.isdir(folderCandidate):
            logging.info('Directory, create file list')
            contents = map(lambda path: os.path.join(folderCandidate, path), os.listdir(folderCandidate))
        
        # could be optimized by an else statement, but looping 2 entries ain't worth it ;)
    
    for path in contents:
        if path == "-r" or path == "--recursive":
            recursive = True
            continue
        
        path = os.path.abspath(path)
        
        if os.path.isdir(path):
            logging.info("Directory found. Storing and continue")
            directories.append(path)
            continue
        
        parseFile(path)
        
    if recursive:
        logging.info("Recursive. Traverse directories.")
        for directory in directories:
            parseDirectory(directory, True)
    
    logging.info("Done converting")

def parseFile(fileName):
    """
    Parse a file, converting it from old style GXT to new style (standard java).
    
    Parameters:
        fileName: the file to parse, absolute paths is desired here.
    """
    if not os.path.splitext(fileName)[1] == ".java":
        logging.info("File name does not end in .java. Ignoring and continue.")
        return
    
    with open(fileName, "r+") as f:
        code = f.read()
        (newCode, count) = convertAll(code)
        if (count > 0):
            logging.info("Model structure found. Updating file: %s", fileName)
            f.seek(0)
            f.truncate()
            f.write(newCode)

def parseDirectory(directory, recursive=False):
    """
    Parse directory, simply traverses the directory, and parse the files with parseFile.
    This will convert all java-files from the old style GXT model code to the new style (standard java).
    
    Parameters:
        directory: the directory to parse. Absolute paths is desired here.
        recursive: if the operation should be done recursively (if subdirectories shoul be parsed).
            Defaults to False.
    """
    
    logging.debug("Parsing directory: %s", directory)
    
    for path in os.listdir(directory):
        path = os.path.join(directory, path)
        if os.path.isdir(path) and recursive:
            parseDirectory(path, True)
        else:
            parseFile(os.path.abspath(path))

def convertAll(code):
    """
    Convert getters and setters from old GXT 2.* code to GXT 3 (standard Java)
    Parameters:
        code: the code to convert
    
    Returns:
        A tuple with the(
            GTX 3 model (Standard Java)
            Number of replaces
    
    Example:
        input:
        public void setFoo(Foo foo) {
            set("foo", foo);
        }
        
        public Foo getFoo() {
            return get("foo");
        }
        
        will return:
        ("public void setFoo(Foo foo) {
            this.foo = foo;
        }
        
        public Foo getFoo() {
            return foo;
        }", 2)
    """
    
    (newCode, count1) = importConvert(code)
    (newCode, count2) = superClassConvert(newCode)
    (newCode, count3) = setConvert(newCode)
    (newCode, count4) = getConvert(newCode)
    
    return (newCode, count1+count2+count3+count4)

def importConvert(code):
    reg = re.compile(r'''import com\.extjs\.gxt\.ui\.client\.data\.BaseModel(?:Data)?;[ \t]*\n''')
    newCode = reg.subn(r'', code)
    return newCode

def superClassConvert(code):
    reg = re.compile(r'''(.*)extends (?:com\.extjs\.gxt\.ui\.client\.data\.)?BaseModel(?:Data)?(?: )?(.*)''')
    newCode = reg.subn(r'\1\2', code)
    return newCode

def setConvert(code):
    """
    Convert setters from old GXT 2.* code to GXT 3 (standard Java)
    Parameters:
        code: the code to convert
    
    Returns:
        A tuple with the
            GTX 3 model (Standard Java)
            Number of replaces
    
    Example:
        input:
        public void setFoo(Foo foo) {
            set("foo", foo);
        }
        
        will return:
        ("public void setFoo(Foo foo) {
            this.foo = foo;
        }",1)
    """
    
    reg = re.compile(r'''(\s*)(?:this\.)?set\s*\(\s*["']([a-zA-Z][\w-]*)["']\s*,\s*([a-zA-Z][\w-]*)\s*\)\s*;(\s*)''')
    newCode = reg.subn(r'\1this.\2 = \3;\4', code)
    return newCode
    
def getConvert(code):
    """
    Convert getters from old GXT 2.* code to GXT 3 (standard Java)
    Parameters:
        code: the code to convert
    
    Returns:
        GTX 3 model (Standard Java)
    
    Example:
        input:
        public Foo getFoo() {
            return get(foo);
        }
        
        will return:
        ("public Foo getFoo() {
            return foo;
        }", 1)
    """
    
    reg = re.compile(r'''(\s*)return (?:this\.)?get\s*\(\s*["']([a-zA-Z][\w-]*)["']\s*\)\s*;(\s*)''')
    newCode = reg.subn(r'\1return \2;\3', code)
    return newCode
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    convert()