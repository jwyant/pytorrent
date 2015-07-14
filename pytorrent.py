#!/usr/bin/env python2
import os
import sys
import bencode
import urlparse
import hashlib

def to_unicode(text):
	""" Return a decoded unicode string.
		False values are returned untouched.
	"""
	if not text or isinstance(text, unicode):
		return text

	try:
		# Try UTF-8 first
		return text.decode("UTF-8")
	except UnicodeError:
		try:
			# Then Windows Latin-1
			return text.decode("CP1252")
		except UnicodeError:
			# Give up, return byte string in the hope things work out
			return text

metainfo = bencode.bdecode(open(os.path.expanduser(''.join(sys.argv[2:])),'rb').read())

#print metainfo

if sys.argv[1] == 'tracker':
    print urlparse.urlparse(metainfo['announce']).hostname
    sys.exit(0)
elif sys.argv[1] == 'infohash':
    print hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper()
    sys.exit(0)
elif sys.argv[1] == 'base_directory':
    print os.path.join(os.path.expanduser('~/rtorrent/torrents'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper())
    sys.exit(0)
elif sys.argv[1] == 'initial_infohash_directory':
    print os.path.join(os.path.expanduser('~/rtorrent/torrents'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper())
    sys.exit(0)
elif sys.argv[1] == 'complete_directory':
    name = metainfo['info']['name']
    try:
    	tempfiles = metainfo['info']['files']
    	files = []
    	size = 0
    	for tf in tempfiles:
    		files.append({'filename':'/'.join(tf['path']),'filesize':tf['length']})
    		size += tf['length']
    except KeyError as e:
    	files = [{'filename':metainfo['info']['name'],'filesize':metainfo['info']['length']}]
    	size = metainfo['info']['length']

    numfiles = 0
    for f in files:
    	numfiles += 1


    if numfiles > 1:
    	torrentfolder = to_unicode(name)+'/'
    elif numfiles == 1 and files[0]['filename'] != name:
    	torrentfolder = to_unicode(name)+'/'
    else:
    	torrentfolder = ''
    print os.path.join(os.path.expanduser('~/rtorrent/completed'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper(),torrentfolder)
    sys.exit(0)
