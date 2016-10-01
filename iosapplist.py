from zipfile import ZipFile
from biplist import readPlistFromString
from glob import glob
import os
import sys

base_dir = os.path.expanduser("~/Music/iTunes/Mobile Applications")


def get_app_name(plist):
	return plist["playlistName"]

def get_account_name(plist):
	if "appleId" in plist:
		return plist["appleId"]
	if "com.apple.iTunesStore.downloadInfo" in plist:
		return plist["com.apple.iTunesStore.downloadInfo"]["accountInfo"]["AppleID"]
	return "unknown"

def get_app_dict(base_dir):
	base_spec = "*ipa"
	app_files = glob(base_dir + "/" + base_spec)
	plist_fname = "iTunesMetadata.plist"
	app_dict = {}

	for file_name in app_files:
		file = ZipFile(file_name)
		bplist_data = file.read(plist_fname)
		plist = readPlistFromString(bplist_data)
		#print file_name
		app_name = get_app_name(plist)
		account_name = get_account_name(plist) 
		if not account_name in app_dict:
			app_dict.setdefault(account_name, [app_name])
		else:
			app_dict[account_name] += [app_name]

	return app_dict

def show_summary(app_dict):
	for apple_id in app_dict.keys():
		print apple_id, "has", len(app_dict[apple_id]), "applications."

def show_apps_for_account(app_dict, account_name):
	if account_name in app_dict:
		for app_name in app_dict[account_name]:
			print app_name
	else:
		print "No apps found for account:", account_name


print "Reading information from the ios apps found in:"
print base_dir
print "Please wait..."

app_dict = get_app_dict(base_dir)

if len(sys.argv) < 2:
	show_summary(app_dict)
else:
	show_apps_for_account(app_dict, sys.argv[1])

