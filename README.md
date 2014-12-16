avr-stl
=======

This repository contains a copy of Andy Brown's Standard Template
Library (STL) for AVR with C++ streams version 1.1.

See his post here for more details:

<http://andybrown.me.uk/wk/2011/01/15/the-standard-template-library-stl-for-avr-with-c-streams/>

#Installation Instructions

##Linux and Mac OS X

```shell
mkdir ~/git
cd ~/git
git clone https://github.com/peterpolidoro/avr-stl.git
cd ~/git/avr-stl
python symlinks.py -i -a <arduino_installation_path> (.e.g. ~/arduino-1.0.6)
```

##Windows

If you want to use the STL from within the popular Arduino IDE then
all you need to do is copy all the files in the avr-stl\include
directory into the hardware\tools\avr\avr\include subdirectory of the
Arduino installation. For example, copy all the header files into
here:

```shell
C:Program Files (x86)\arduino-1.0.6\hardware\tools\avr\avr\include
```

