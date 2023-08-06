# Overview

A collection of simple utils for common operations
This includes configuration item from .ini file, a filemanger for hadling file uploads, some utilities for SQLAlchemy models and a CSV reader/writer unicode-safe for python 2.7


### Configuration from .ini 

The class ppss_pyramidutils.Utils offers convenience options to get data from the main ini file, allowing default values.
The easiest way to use it is to subclass it with your conf class and override the __myconf__ property:

```python
from ppss_pyramidutils import Utils as IniUtils

class MyClass(IniUtils):
  myconf = ['param1','param2']
```

Then you can read ini file calling the class method __config__:

```python
MyClass.config(settings)
```

This method accetps other optional parameters: __prefix__ and __defaultval__.

If __prefix__ is not passed, lowered case class name is used instead (i.e.: myclass).
Ths config method use  all values in __myconf__ property and read in the ini file the parameter:
__prefix__.__value__

In this example it reads myclass.param1 and myclass.param2.
If a key in missing in the ini file, the corresponding class property will assume the value __defaultval__.

__myconf__ can be a tuple/list instead of a string. In this case the first value is the string, the second value is the default value only for that key.

A full example can work as follow:

```python
#ini file
myprefix.param1 = 12
myprefix.param2 = A simple String

from ppss_pyramidutils import Utils as IniUtils

class MyClass(IniUtils):
  myconf = ['param1','param2',('param3',"a missing value with a default"),"param4"]

MyClass.config(settings,"myprefix",defaultval="default")

MyClass.param1
# '12'
MyClass.param2
# 'A simple String'
MyClass.param3
# 'a missing value with a default'
MyClass.param4
# 'param4'

```

Because they are just class values, you can simply include your class anywhere in your code and access the class property required.
This will allow to read and set default for each value in a centralized place and to access it whenever and wherever needed.


### filemanger (for upload and other purposes)

__ppss_pyramidutils.FileManager__ extends __ppss_pyramidutils.Uitls__ setting __myconf__ attribute myconf = ['savepath','tmppath']
You can include the class in the ini of the pyramid app and call the __config__ method against it to properly config the class.

FileManager offer the following class methods:
* __saveToTmp(cls,requestfile)__ -> __file_path__: takes as argument the file object from the form, replace some chars in the filename and save it to a temp location (specified through ini file). This method returns the file path of the temporary file.
* __moveToDestination(cls,source,filename,subfolder="")__ -> __file_path__: this method takes a file path (tipically the return value of pthe revious saveToTmp call) and moves it in target folder (as of ini file), with the given __filename__. It can put it in a subfolder if __subfolder__ is specified. This will create the folder if required. Returns the complete path of the file.
* __deleteFile(cls,file)__ -> None : delete a file with the path __file__

It also has two commodity class methods:
* __sanitizeFilename(cls,filename, whitelist=_valid_filename_chars, replace=' ')__ -> __sanitizedfilename__: replaces all occurency of each char of __replace__ string with a "_", that removes all not allowed char (allowed chat by default are: -, \_, \., \(, \), __string.ascii_letters__ and __string.digits__ ). The method returns the sanitized file name. It is called automatically by saveToTmp to prevent attempts of injections in file system.
* __slugify(cls,filename)__ -> __sluggifiedfilename__: This method tries to convert an arbitrary file name in a sluggied string. 

### CSV reader/writer for python 2.7

Python 2.7 CSV reader and writer fail to address many unicode problems. 
You can simply use __ppss_pyramidutils.UnicodeReader__ and __ppss_pyramidutils.UnicodeWriter__ for this purpose.

Both __UnicodeReader__ and __UnicodeWriter__ .\_\_init\_\___ methods accept this parameters:
* __f__: the already opened file to read.
* __dialect__=csv.excel: the csv dialect to use. 
* __encoding__="utf-8-sig": encoding to use.

All other keyword arguments are passed on to the CSV reader (check the module in standard Python 2.7 documentation)

For conveninece and use as importer/export of CSV formatted data, two more classes are defined.

__Importer__ class can be initialized with this parameters:
* __fn__: File name of the source. It will be opened and passed to 
* __mapping__=None: allow to remap column names. If present the mapping param must be a dictionary-like object, containing all CSV column names as key, and the mapped names as values
* __delimiter__=",": the delimiter for the CSV input
* __headertransform__=None: a callable that receive each column name and may transform it. Usually used to do some sanitization on the names (ie: lower and remove/substitute forbiden chars)

Creating the __Importer__ object actually triggers the file opening and reading. To get the resulting rows as a list of dictionaries, you can use the method __getRows__.


__Exporter__ class takes this parameters when initialized:
* __evcollection__ : list-like object, where each item is a dictionary-like (see getter param) object.
* __titles__ : ordered list-like object, containing column names
* __parserows__ = True: if set, allow pre-processing of the input (__evcollection__), using __getter__ and __datetimeformat__ paramesters. 
* __delimiter__  = ',': the delimiter for the CSV output
* __getter__ = None: a callable to override the dictionary like way to get values. If set the getter will be called for each column with the item and name of the column (ie: val = getter(ev,k)). Only used if __parserows__ is True.
* __datetimeformat__ = "%Y-%m-%d" : formatter for datetime.datetime and datetime.date objects. Only used if __parserows__ is True.

This method set the property __retfile__ to a __tempfile.NamedTemporaryFile__ (set to writemode in Python 2)

the method __writeAll__ accept only a __delimiter__ param and actualy writes all rows in the __retfile__ property (by default a __tempfile.NamedTemporaryFile__ instance)


### Modelbase utilities


__ppss_pyramidutils.ModelCommonParent__ attach some commodity methods to derived SQLAlchemy classes, as class methods, like:

* all(cls,DBSession): returns all elements of the given class
* byId(cls,id,DBSession): returns the object with __id__ = id. COC: the class must have a id column.
* byField(cls,field,value,DBSession): like byId, on an arbitraty __field__
* byFields(cls,fields,DBSession): accept a list of filters as tuples of (columnname, value) and returns all items that matches
* delete(cls,element,DBSession): delete the element
* deleteAll(cls,elements,DBSession): delete all elements in elements list-like parameter.




