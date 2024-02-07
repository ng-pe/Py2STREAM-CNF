# Py2STREAM-CNF.py
Python CLI for Panasonic P2Network Setting files operation (P2STREAM.CNF) 

This tool work to generate and view P2STREAM.CNF file for Panasonic HC-X1500 / HC-X2000 CAM.


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


# How to find key?
According to the specification, the file is encrypted using AES-128-ECB. The tool provided by Panasonic can be used to create these files (https://eww.pass.panasonic.co.jp/pro-av/support/content/download/EN/ep2main/nw_setting_e.htm). 

A first method would be to disassemble and look for the key in memory, but this method requires more time and assembly skills, so I'm going to explain another method that works when the key is in the binary... somewhere... (and when the exe is not packed ;) ).

First you need to generate a P2STREAM.CNF file on your camcorder using an identifiable url (rtmp://example.com/stream/) for example.
Once this has been done, you need to retrieve the file from the SD card.

The idea here is to go through the file byte by byte and test all the 128bit sequences (16 bytes) of exe file to decrypt the P2STREAM.CNF file ... 

Here is a small piece of code to illustrate:

```
from Crypto.Cipher import AES

if __name__ == '__main__':
    with open("P2STREAM.CNF", mode="rb") as P2STREAM_file:
        contents = P2STREAM_file.read()
    bad_key_tested = 0

    with open('P2NetGen3.exe', 'rb') as P2bintools:
        while True:
            possible_key = P2bintools.read(16)
            try:
                decipher = AES.new(possible_key, AES.MODE_ECB)
                P2STREAM_bytes = decipher.decrypt(contents)
                P2STREAM = P2STREAM_bytes.decode('utf-8').rstrip('\x00')

                if "example.com" in P2STREAM:
                    key = ' '.join(format(octet, '02X') for octet in possible_key)
                    print('Key Found ! : {key}'.format(key=key))
                    print('Tested key ' , bad_key_tested)
                    break

            except Exception as e:
                bad_key_tested = bad_key_tested + 1

```

Output :

```
Key Found ! : 6D 63 35 63 38 38 57 4A 5A 62 58 6A 5A 59 4A 6D
Tested key  7868
```



# License : MIT 

Copyright 2024 Nicolas GOLLET

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
