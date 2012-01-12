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

from hamcrest import *
import unittest
from ModelConvert import *

class TestModelConverter(unittest.TestCase):
    def testImport(self):
        data = """import com.extjs.gxt.ui.client.data.BaseModel;\n"""
        expected = ("", 1)
        assert_that(importConvert(data), equal_to(expected))
        
        data = """import com.extjs.gxt.ui.client.data.BaseModelData;\n"""
        expected = ("", 1)
        assert_that(importConvert(data), equal_to(expected))
        
        assert_that(importConvert(self._fullExample), equal_to((self._fullImportExpected,1)))
        
    def testBaseModelDataExtends(self):
        data = """public class Absence extends BaseModel implements IGsonModel {"""
        expected = ("""public class Absence implements IGsonModel {""", 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        data = """public class Absence extends BaseModel{"""
        expected = ("""public class Absence {""", 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        data = """public abstract class Absence extends BaseModel implements IGsonModel"""
        expected = ("""public abstract class Absence implements IGsonModel""", 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        data = """public class Absence extends BaseModelData {"""
        expected = ("""public class Absence {""", 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        data = """public class Absence extends BaseModelData"""
        expected = ("""public class Absence """, 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        data = """public class Absence extends com.extjs.gxt.ui.client.data.BaseModel implements IGsonModel {"""
        expected = ("""public class Absence implements IGsonModel {""", 1)
        assert_that(superClassConvert(data), equal_to(expected))
        
        assert_that(superClassConvert(self._fullExample), equal_to((self._fullSuperClassExpected,1)))
        
    def testSetter(self):
        assert_that(setConvert('set("fooBar", fooBar);'), equal_to(('this.fooBar = fooBar;', 1)))
        assert_that(setConvert("set('fooBar', fooBar);"), equal_to(('this.fooBar = fooBar;', 1)))
        assert_that(setConvert("set( 'fooBar', fooBar);"), equal_to(('this.fooBar = fooBar;', 1)))
        
        assert_that(setConvert("""public class Test {
	public Object getFooBar() {
		set('fooBar', fooBar);
	}
}"""), equal_to(("""public class Test {
	public Object getFooBar() {
		this.fooBar = fooBar;
	}
}""", 1)))
        assert_that(setConvert('''public class Test {
	public Object getFooBar() {
		set("fooBar", fooBar);
	}
}'''), equal_to(("""public class Test {
	public Object getFooBar() {
		this.fooBar = fooBar;
	}
}""", 1)))
        
        assert_that(setConvert('''public class Test {
	public Object getFooBar() {
		set( "fooBar" , fooBar );
	}
}'''), equal_to(("""public class Test {
	public Object getFooBar() {
		this.fooBar = fooBar;
	}
}""", 1)))
        
        assert_that(setConvert(self._fullExample), equal_to((self._fullSetExpected, 1)))
    
    
    def testGetter(self):
        assert_that(getConvert('return get("fooBar");'), equal_to(('return fooBar;', 1)))
        assert_that(getConvert("return get('fooBar');"), equal_to(('return fooBar;', 1)))
        assert_that(getConvert("return get( 'fooBar' );"), equal_to(('return fooBar;', 1)))
        assert_that(getConvert('return this.get("lastDay");'), equal_to(('return lastDay;', 1)))
        
        assert_that(getConvert("""public class Test {
 public Object getFooBar() {
     return get('fooBar');
 }
}"""), equal_to(("""public class Test {
 public Object getFooBar() {
     return fooBar;
 }
}""", 1)))
        assert_that(getConvert('''public class Test {
 public Object getFooBar() {
     return get("fooBar");
 }
}'''), equal_to(("""public class Test {
 public Object getFooBar() {
     return fooBar;
 }
}""", 1)))
        
        assert_that(getConvert('''public class Test {
 public Object getFooBar() {
     return get( "fooBar" );
 }
}'''), equal_to(("""public class Test {
 public Object getFooBar() {
     return fooBar;
 }
}""", 1)))
        
        assert_that(getConvert(self._fullExample), equal_to((self._fullGetExpected, 1)))
    
    def testFullCode(self):
        assert_that(convertAll(self._fullExample), equal_to((self._fullExpected, 4)))
    
    
    
    _fullExample = """package dk.rohdef.viewmodel;

import com.extjs.gxt.ui.client.data.BaseModel;

/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change extends BaseModel implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn get("dateOfChange");
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tset("dateOfChange", dateOfChange);
\t}
}"""

    _fullExpected = """package dk.rohdef.viewmodel;


/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn dateOfChange;
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tthis.dateOfChange = dateOfChange;
\t}
}"""
    
    _fullImportExpected = """package dk.rohdef.viewmodel;


/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change extends BaseModel implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn get("dateOfChange");
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tset("dateOfChange", dateOfChange);
\t}
}"""
    
    _fullSuperClassExpected = """package dk.rohdef.viewmodel;

import com.extjs.gxt.ui.client.data.BaseModel;

/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn get("dateOfChange");
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tset("dateOfChange", dateOfChange);
\t}
}"""

    _fullGetExpected = """package dk.rohdef.viewmodel;

import com.extjs.gxt.ui.client.data.BaseModel;

/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change extends BaseModel implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn dateOfChange;
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tset("dateOfChange", dateOfChange);
\t}
}"""
    
    _fullSetExpected = """package dk.rohdef.viewmodel;

import com.extjs.gxt.ui.client.data.BaseModel;

/**
 * Parent class for changes. Know changes are resignation and a change in 
 * employment. 
 * @author Rohde Fischer
 */
public abstract class Change extends BaseModel implements IGsonModel {
\tprivate static final long serialVersionUID = 1L;

\tpublic RfDate getDateOfChange() {
\t\treturn get("dateOfChange");
\t}
\t
\tpublic void setDateOfChange(RfDate dateOfChange) {
\t\tthis.dateOfChange = dateOfChange;
\t}
}"""


if __name__ == "__main__":
    runTests()