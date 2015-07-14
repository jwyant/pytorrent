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

metainfo = bencode.bdecode(open(os.path.expanduser(' '.join(sys.argv[2:])),'rb').read())

if sys.argv[1] == 'tracker':
    sys.stdout.write(urlparse.urlparse(metainfo['announce']).hostname)
    sys.exit(0)
elif sys.argv[1] == 'infohash':
    sys.stdout.write(hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper())
    sys.exit(0)
elif sys.argv[1] == 'base_directory':
    sys.stdout.write(os.path.join(os.path.expanduser('~/rtorrent/torrents'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper()))
    sys.exit(0)
elif sys.argv[1] == 'initial_infohash_directory':
    sys.stdout.write(os.path.join(os.path.expanduser('~/rtorrent/torrents'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper()))
    sys.exit(0)
elif sys.argv[1] == 'completed_infohash_directory':
    sys.stdout.write(os.path.join(os.path.expanduser('~/rtorrent/completed'),hashlib.sha1(bencode.bencode(metainfo['info'])).hexdigest().upper()))
    sys.exit(0)
