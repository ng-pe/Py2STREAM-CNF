from Crypto.Cipher import AES
from xml.dom.minidom import parse, parseString, Node

import argparse
import os.path
from os.path import exists

class Py2StreamConfigGenerator:
    def __init__(self, debug=False):

        self.key = b'\x6d\x63\x35\x63\x38\x38\x57\x4a\x5a\x62\x58\x6a\x5a\x59\x4a\x6d'
        self.template_P2stream = '<P2Control version="1.0" generator="P2 Network Setting ' \
                                 'Software"><server><rtmp><url>{URL}</url></rtmp></server></P2Control>'
        self.debug = debug

    def gen_file(self, url, file, forced=False):
        print(f'INFO : Generating P2STREAM.CNF for {url}')
        cipher = AES.new(self.key, AES.MODE_ECB)
        config_data = self.template_P2stream.format(URL=url).encode('UTF8')
        bytestoadd = (16 - (len(config_data) % 16))
        msg = cipher.encrypt(config_data + bytearray(bytestoadd) if bytestoadd > 0 else config_data)
        if self.debug:
            print("\nDEBUG : P2STREAM.CNF encrypted data in hex ----")
            print(msg.hex())
            print("----\n")

        if os.path.isfile(file) and not forced:
            print("WARNING : File already exists, use -f to force overwrite!")
            return False

        with open(file, 'wb') as config_file:
            config_file.write(msg)
            config_file.flush()
            print("INFO : destination file {file} saved. ".format(file=file))
        return True

    def decrypt_file(self, file):
        print(f'INFO : Get RTMP configuration from {file}')
        cipher = AES.new(self.key, AES.MODE_ECB)
        with open(file, mode="rb") as P2STREAM_file:
            contents = P2STREAM_file.read()
            decipher = AES.new(self.key, AES.MODE_ECB)
            P2STREAM_bytes = decipher.decrypt(contents)
            P2STREAM_xml = P2STREAM_bytes.decode('utf-8').rstrip('\x00')

        if self.debug:
            print("--DEBUG: RAW P2STREAM.CNF decrypted data: --")
            print(P2STREAM_xml)
            print("----")

        # parsing XML file :
        document = parseString(P2STREAM_xml)
        print(document.childNodes[0].toprettyxml())
        rootP2Control = document.documentElement
        if rootP2Control.nodeName == "P2Control":
            print("Detecting P2Control file...")
            print(f' -> Generated with: ', rootP2Control.getAttribute("generator"))
            print(f' -> Version: ', rootP2Control.getAttribute("version"))
            url = document.getElementsByTagName('url')
            print(f' -> rtmp url is : ', url[0].firstChild.nodeValue)


if __name__ == '__main__':
    print("Py2STREAM-CNF v0.1")
    print("CLI for Panasonic P2STREAM.CNF configuration file\n")

    parser = argparse.ArgumentParser(description="CLI for Panasonic P2STREAM.CNF configuration file")
    parser.add_argument('-f', '--force', dest='forced', action='store_true', default=False,required=False, help='Force overwrite if file exists')
    parser.add_argument('-a', '--action', choices=['print', 'gen'], default='print', required=False,  help='Print or generate file')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, required=False, help='Enable debug mode')

    parser.add_argument('--url', help='URL used for generate config file', default=None, required=False)

    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed.add_argument('--file', dest='file', help='Specify the P2STREAM.CNF file name')
    args = parser.parse_args()

    file_path = args.file
    force = args.forced
    debug_mode = args.verbose
    action = args.action
    url = args.url

    if debug_mode:
        print("INFO : Verbose Mode enabled...")
        debug = True
    else:
        debug = False

    p2_gen = Py2StreamConfigGenerator(debug=debug)

    if (action == 'print'):
        if exists(file_path):
            p2_gen.decrypt_file(file_path)
        else:
            print("ERROR: File {file} not exists!".format(file=file_path))

    elif (action == 'gen'):
        # check url :
        if url is None:
            print("ERROR: url args is required (eg --url \"rtmp://example.com/live/stream\" )")
            exit(1)
        elif str(url).upper().startswith("RTMP://") == False:
            print("ERROR: url args must start with rtmp:// (eg --url \"rtmp://example.com/live/stream\" )")
            print("current value is : ", url)
            exit(1)

        if p2_gen.gen_file(url, file_path, forced=force) == True:
            exit(0)
        else:
            exit(1)

    exit(0)

