# GxtModelConverter
From the previous versions of Sencha GXT we used to use BaseModelData and BaseModel for our models.
Those two implemented their own internal map, for storing the data and to enable GXT to communicate 
with them.

In GXT 3 though Sencha have moved away from that approach and now uses the standard Java way of doing it.
Leaving old GXT code unusable.

This converts model code from the old code to standard Java code.

## Code starndards
This script basically runs a few simple regular expressions on your code to update old style code. Therefore
it will run best en nicely formatted code. Although I've tried to make the regex general enough to match 
most cases, there is no guarantee that it will take badly formatted code.

To be sure please make sure your code conforms with the Java coding standards. If you are unsure if you do
I would recommend you to search for them and learn them. Also if you are using Eclipse as your IDE, you can
run *ctrl+shift+f* to format the code in your active file. Netbeans, IntelliJ and so on, should have a
 similar functionality.

## Usage
**Warning:** Please take an backup before running this script! If something goes wrong I will not take the responsibility.

Just download this project and run:
    
    $ python ModelConvert /path/to/model/directory
    
or if you want it to run recursively:
    
    $ python ModelConvert -r /path/to/model/directory

You can also run it on a single file or a list of files.

## What it doesn't do
+ It doesn't add the private variables needed for the getters and setters (if people are interested I can be talked into adding that).
+ It won't handle specialized code, such as custom implementations of equals and hashCode

## Bugs, suggestions etc.
Please use the issues tool on GitHub for bugs, suggestions, etc.

If you find a bug, please include code that demonstrates the bug. If you can't use real world code, please construct an example.

If you can provide a unit test that shows the bug or proves a correct solution for an improvement, you're great.

## License, author (the boring stuff ;) )
+ License: MIT X11
+ Author: Rohde Fischer <rohdef@rohdef.dk>
