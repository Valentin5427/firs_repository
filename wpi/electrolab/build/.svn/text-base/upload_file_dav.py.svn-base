#-*- coding: UTF-8 -*-
import easywebdav
import argparse
# server, user, pass, path, file

parser = argparse.ArgumentParser(description='Upload file to WebDav server. Support only http protocol.')
parser.add_argument('server', help='Server name or IP')
parser.add_argument('username', help='User name', )
parser.add_argument('password', help='Password')
parser.add_argument('localfile', help='File name for upload (source)')
parser.add_argument('davpath', help='Remote path for upload (destantion)')
parser.print_help()

#webdav = easywebdav.connect('diposoft.ru',
#                            username='knurov',
#                            password='marazm',
#                            protocol='http'
#                            )
#http://diposoft.ru/dav/ElectroLab/install/
# Do some stuff:
#webdav.exists('dav/ElectroLab/install')
#webdav.cd('dav/ElectroLab/install')
#print webdav.ls()

args = parser.parse_args()

webdav = easywebdav.connect(args.server
                            , username=args.username
                            , password=args.password
                            , protocol='http'
                            )
webdav.upload(args.localfile, args.davpath)
