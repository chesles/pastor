#!/usr/bin/python

import os, sys
import hashlib
import getpass
import argparse

def get_base():
  return getpass.getpass( "Enter base phrase: " )

def get_checksum(sanity_check):
  sanity_check = hashlib.sha256()
  sanity_check.update( base_phrase.encode('utf-8') )
  return sum( [ x for x in sanity_check.digest() ] )

def get_door():
  print( "Enter door id: ", file=sys.stderr, end="")
  return input()

def make_password(base_phrase, door_id, length, valid_chars):
  key_data = hashlib.sha256()
  key_data.update( (base_phrase + ' - ' + door_id).encode('utf-8') )

  return ''.join( [ valid_characters[ x % len( valid_chars ) ] for x in key_data.digest() ][:length] )

if __name__ == '__main__':
  argparser = argparse.ArgumentParser(description="Store all your passwords without storing them anywhere")
  argparser.add_argument('-d', '--door', type=str, default='', required=False)
  argparser.add_argument('-n', '--no-symbols', default=False, required=False,
          dest='no_symbols', action='store_const', const=True)
  argparser.add_argument('length', type=int, default=8)

  args = argparser.parse_args()

  base_phrase = get_base()
  print(get_checksum(base_phrase), file=sys.stderr)

  password_length = args.length
  door_id = args.door or get_door()

  valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  if not args.no_symbols:
    valid_characters += '!@#$%^&*()-_=+[{}]|\\:;\'",<.>/?'
  print(make_password(base_phrase, door_id, password_length, valid_characters))
