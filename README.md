# Py2STREAM-CNF.py
Python CLI for Panasonic P2Network Setting files operation (P2STREAM.CNF) 

This tool work to generate file for Panasonic HC-X1500 / X2000 CAM.


# Usage / Help :

```
Py2STREAM-CNF v 0.1
CLI for Panasonic P2STREAM.CNF configuration file

usage: Py2STREAM-CNF.py [-h] [-f] [-a {print,gen}] [-v] [--url URL] [--file FILE]

options:
  -h, --help            show this help message and exit
  -f, --force           Force overwrite if file exists
  -a {print,gen}, --action {print,gen}
                        Print or generate file
  -v, --verbose         Enable debug mode
  --url URL             URL used for generate config file

Required arguments:
  --file FILE           Specify the P2STREAM.CNF file name

```

# some example :

- Read P2STREAM.CNF file :

Command : `python Py2STREAM-CNF.py --file ./P2STREAM.CNF`

Output:

```
Py2STREAM-CNF v 0.1
CLI for Panasonic P2STREAM.CNF configuration file

INFO : Get RTMP configuration from ./P2STREAM.CNF
<P2Control version="1.0" generator="P2 Network Setting Software">
        <server>
                <rtmp>
                        <url>rtmp://example.com/live/stream</url>
                </rtmp>
        </server>
</P2Control>

Detecting P2Control file...
 -> Generated with:  P2 Network Setting Software
 -> Version:  1.0
 -> rtmp url is :  rtmp://example.com/live/stream
```

- Generate new P2STREAM.CNF file :

Command : `python Py2STREAM-CNF.py --file ./example.com/P2STREAM.CNF --action gen --url "rtmp://login:password@example.com/stream?token=1234567"`

Output : 

```
Py2STREAM-CNF v 0.1
CLI for Panasonic P2STREAM.CNF configuration file

INFO : Generating P2STREAM.CNF for rtmp://login:password@example.com/stream?token=1234567
INFO : destination file ./example.com/P2STREAM.CNF saved. 
```

Copy `P2STREAM.CNF` file on your SDCARD in `/PRIVATE/MEIGROUP/PAVCN/SBG/P2SD/` folder.

# License : MIT 

Copyright 2024 Nicolas GOLLET

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
