# -*- coding: utf-8 -*- 

# Part of Gitter - Simple Git client for Android
license="""Copyright 2011 Joshua King

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""
urls = {"Web site": "http://techtransit.blogspot.com", "Source Code": "https://github.com/jkingok/sl4a-scripts", "License": "http://www.apache.org/licenses/LICENSE-2.0"}

import android 

import os
import sys
import traceback

droid = android.Android()

def setoptionsmenu(l, d=None):
	droid.clearOptionsMenu()
	for i in l:
		icon=None
		if i=="Edit":
			icon="@android:drawable/ic_menu_edit"
		elif i=="Exit":
			icon="@android:drawable/ic_menu_close_clear_cancel" 
		elif i=="New":
			icon="@android:drawable/ic_menu_add"
		elif i=="Open":
			icon="@android:drawable/ic_menu_rotate"
		elif i=="Save":
			icon="@android:drawable/ic_menu_save"
		elif i=="Save As":
			icon="@android:drawable/ic_menu_save"
		elif i=="Help":
			icon="@android:drawable/ic_menu_help"
		elif i=="About":
			icon="@android:drawable/ic_menu_info_details"
		droid.addOptionsMenuItem(i, i, d, icon)

def showchoice(t, l, p="OK", n="Cancel"):
 	droid.dialogCreateAlert(t)
	droid.dialogSetSingleChoiceItems(l)
	droid.dialogSetPositiveButtonText(p)
	droid.dialogSetNegativeButtonText(n)
	droid.dialogShow()
	r=droid.dialogGetResponse().result
	if 'canceled' in r or r['which'] == "negative":
		return
	else:
		return l[droid.dialogGetSelectedItems().result[0]]

lasttitle=None

def showprogress(m, t=None, cur=None, max=None):
	global droid, lasttitle
	lasttitle=t or lasttitle
	droid.dialogDismiss()
	droid.dialogCreateSpinnerProgress(lasttitle, m)
	droid.dialogShow()
 
def showinput(t, m, d="", p="OK", n="Cancel", s=False):
	if s:
		droid.dialogCreatePassword(t, m)
	else:
		droid.dialogCreateInput(t, m, d)
	droid.dialogSetPositiveButtonText(p)
	droid.dialogSetNegativeButtonText(n)
	droid.dialogShow()
	r=droid.dialogGetResponse().result
	if 'canceled' in r or r['which']=="negative":
		return
	else:
		return r['value']

def showerror(t="Error"):
	droid.dialogDismiss()
	m=traceback.format_exc()
	if showquestion(t, m, "Copy to clipboard", "Close"):
		droid.setClipboard(m)
 
def showquestion(t, m, p="Yes", n="No"):
	droid.dialogCreateAlert(t, m)
	droid.dialogSetPositiveButtonText(p)
	droid.dialogSetNegativeButtonText(n)
	droid.dialogShow()
	r=droid.dialogGetResponse().result
	return (not ('canceled' in r)) and r['which']=="positive" 

def showerror(t="Error"):
	droid.dialogDismiss()
	m=traceback.format_exc()
	if showquestion(t, m, "Copy to clipboard", "Close"):
		droid.setClipboard(m)

def showmessage(t, m, n="OK"):
	droid.dialogCreateAlert(t, m)
	droid.dialogSetNeutralButtonText(n)
	droid.dialogShow()

def showlayoutfile(f):
	with open(f, "rb") as file:
		droid.fullShow(file.read())	 

def showopenfile(f=None, e=None, t="Open", p="Open", n="Cancel"): 
 	if f == None:
		rootdir = os.getcwd()
	else:
		rootdir = os.path.dirname(f)
	while True:
		l = []
		ld = []
		lf = []
		for i in os.listdir(rootdir):
			file = os.path.join(rootdir, i)
			ext = os.path.splitext(file)[1]
			if os.path.isdir(file):
				ld.append(i)
			elif e == None or ext.lower() == e.lower():
				lf.append(i)
		ld = sorted(ld)
		lf = sorted(lf)
 		if rootdir != "/":
			l.append(os.pardir)
		l = l + ld + lf
		r = showchoice(t + " from " + rootdir, l, p, n)
		if r == None or os.path.isfile(os.path.join(rootdir, r)):
			break
		elif r == os.pardir:
			rootdir = os.path.dirname(rootdir)
		else:
			rootdir = os.path.join(rootdir, r)
	if r == None:
		return None
	else:
		return os.path.join(rootdir, r)

def showsavedir(d=None, t="Save", p="Save", n="Cancel"):
	if d == None:
		rootdir = os.getcwd()
	else:
		rootdir = d
	while True:
		l = []
		ld = []
		for i in os.listdir(rootdir):
			file = os.path.join(rootdir, i)
			if os.path.isdir(file):
				ld.append(i)
		ld = sorted(ld)
		l.append("<New Folder>")
		l.append("<Select this Folder>")
		if rootdir != "/":
			l.append(os.pardir)
		l = l + ld
 		r = showchoice(t + " to " + rootdir, l, p)
		if r == None:
			break
		elif r == os.pardir:
			rootdir = os.path.dirname(rootdir)
		elif r == "<New Folder>":
			r = showinput("New folder in " + rootdir, "Enter name")
			if r == None:
				continue
			else:
				rootdir = os.path.join(rootdir, r)
				os.mkdir(rootdir)
		elif r == "<Select this Folder>":
			r = rootdir
			break
		else:
			rootdir = os.path.join(rootdir, r)
	if r == None:
		return None
	return r

def showsavefile(f=None, e=None, t="Save", w=True, p="Save", n="Cancel"):
 	if f == None:
		rootdir = os.getcwd()
	else:
		rootdir = os.path.dirname(f)
	while True:
		l = []
		ld = []
		lf = []
		for i in os.listdir(rootdir):
			file = os.path.join(rootdir, i)
			ext = os.path.splitext(file)[1]
			if os.path.isdir(file):
				ld.append(i)
			elif e == None or ext.lower() == e.lower():
				lf.append(i)
		ld = sorted(ld)
		lf = sorted(lf)
		l.append("<New Folder>")
		l.append("<New File>")
 		if rootdir != "/":
			l.append(os.pardir)
		l = l + ld + lf
		r = showchoice(t + " to " + rootdir, l, p)
		if r == None:
			break
		elif os.path.isfile(os.path.join(rootdir, r)):
			if not w or showquestion(t + " to " + rootdir, "Are you sure you want to overwrite " + r + "?"):
				break
		elif r == os.pardir:
			rootdir = os.path.dirname(rootdir)
		elif r == "<New Folder>":
			r = showinput("New folder in " + rootdir, "Enter name")
			if r == None:
				continue
			else:
				rootdir = os.path.join(rootdir, r)
				os.mkdir(rootdir)
		elif r == "<New File>":
			r = showinput(t + " to " + rootdir, "Enter name", e)
			if r == None:
				continue
			else:
				break
		else:
			rootdir = os.path.join(rootdir, r)
	if r == None:
		return None
	return os.path.join(rootdir, r) 

if not droid.requiredVersion(5): 
	if showquestion("SL4A Too Old", "I need at least version 5 of SL4A. Download now?"):
		droid.view("http://code.google.com/p/android-scripting/downloads/list")
	exit(1)

try:
	import dulwich.client
except:
	if showquestion("Dependency Missing", "Dulwich needs to ve installed. Download now?"):
		droid.view("http://techtransit.blogspot.com/2011/09/dulwich-for-android.html")
	exit(1)

try:
	import paramiko
except:
	try:
		import Crypto
	except:
		if showquestion("Dependency Missing", "PyCrypto needs to be installed. Download now?"):
			droid.view("http://code.google.com/p/python-for-android/downloads/list")
		exit(1)
	if showquestion("Dependency Missing", "Paramiko needs to be installed. Download now?"):
		droid.view("http://www.lag.net/paramiko/")
	exit(1)

class AskDroidUserPolicy(paramiko.MissingHostKeyPolicy):
	def missing_host_key(self, client, host, key):
		if showquestion("Missing SSH Host Key", "Connection to host " + host + " responded with unknown key " + key, "Accept", "Reject"):
			return
		raise SSHException("User rejected host and key")

knownhostsfile = None
sshkey = None
sshpass = None

lastwrapper = None

class ParamikoWrapper(object):
	"""A socket-like object that talks to a subprocess via pipes."""

	def __init__(self, client, channel):
		self.client=client
		self.channel=channel
		# self.read = lambda n: self.channel.recv(n)
		# self.write=lambda b:self.channel.sendall(b)
		self.can_read=lambda:self.channel.recv_ready

	def read(self, n=None):
		r = self.channel.recv(n)
		#print "RECV: " + r
		return r

	def write(self, s):
		self.channel.sendall(s)
		#print "SEND: " + s
		return None

	def close(self):
		global knownhostsfile
		# print "close::"
		self.channel.close()
		if knownhostsfile==None:
			knownhostsfile=showsavefile(knownhostsfile, None, "Save known hosts file")
		if knownhostsfile!=None:
			self.client.save_host_keys(knownhostsfile)

class ParamikoSSHVendor(object):

	def connect_ssh(self, host, command, username=None, port=None):
		#global knownhostsfile, keyfile, password, lastwrapper
		global knownhostsfile, sshkey, sshpass, lastwrapper
		#paramiko.util.log_to_file(r'para.log')
		#print "CONN: ", command
		client=paramiko.SSHClient()
		client.load_system_host_keys()
		if knownhostsfile==None:
			knownhostsfile=showopenfile(None, None, "Open known hosts file")
		if knownhostsfile!=None:
			client.load_host_keys(knownhostsfile)
		client.set_missing_host_key_policy(AskDroidUserPolicy())
		username=username or showinput("Username", "Enter username for " + host)
		port=port or 22
		key=username+"@"+host
		#if not (key in keyfile) and not (key in password):
		if not sshkey and not sshpass:
			r = showchoice("Select authentication for " + key, ["Key pair", "Password"])
			if r == "Key pair":
				f = showopenfile(None, None, "Select private key file", "Select")
				if f == None:
					return None
				#keyfile[key] = f
				sshkey = f
				if showquestion("Passphrase for private key", "Does this private key have a passphrase?"):
					p = showinput("Passphrase", "Enter passphrass for " + f, s=True)
					if p == None:
						return None
				else:
					p = None
				#password[key] = p
				sshpass = p
			elif r == "Password":
				p = showinput("Password", "Enter password for " + key, s=True)
				if p == None:
					return None
				#password[key] = p
				sshkey = None
				sshpass = p
			else:
				return None
		#if key in keyfile:
		#	client.connect(host, username=username, port=port, password=password[key], key_filename=keyfile[key])
		#else:
		#	client.connect(host, username=username, port=port, password=password[key])
		client.connect(host, username=username, port=port, password=sshpass, key_filename=sshkey)
		# client.get_transport().set_hexdump(True)
		channel=client.get_transport().open_session()
		# channel.set_combine_stderr(True)
		# channel.setblocking(1)
		# channel.ultra_debug = True
		channel.exec_command(command[0])
		lastwrapper = ParamikoWrapper(client, channel)
		return lastwrapper

dulwich.client.get_ssh_vendor = ParamikoSSHVendor

from dulwich.objects import Blob, Commit, Tree, parse_timezone

from time import time

from dulwich.repo import Repo 

from paramiko import RSAKey

exiting = False
localrepo = None
remoteclient = None
remoterepo = None
remotesrc = None
repo = None

def do_local_git(r=None, loading=False):
	global droid, localrepo, repo
	if r == None and not loading:
 		r = showsavedir(localrepo, "Select Local Git repository", "Select")
	if r != None:
		path = r
		if os.path.exists(os.path.join(path, ".git")):
			repo = Repo(path)
			droid.makeToast("Opened Git repository in " + path)
		else:
			repo = Repo.init(path)
			droid.makeToast("Created new Git repository in " + path)
		localrepo = r
		droid.fullSetProperty("textLocalGit", "text", localrepo)

def do_remote_git(r=None, loading=False):
	global droid, remoterepo, remoteclient, remotesrc
	if r == None and not loading:
		r = r or showinput("Enter Remote Git repository URI", "Enter the URI of the remote Git repository", remoterepo)
	if r != None:
		remoterepo = r
		remoteclient, remotesrc = dulwich.client.get_transport_and_path(r)
		droid.makeToast("Linked to remote URI " + remoterepo)
		droid.fullSetProperty("textRemoteGit", "text", remoterepo)

def do_ssh_comment():
	global droid, knownhostsfile, sshkey, sshpass
 	ssh_comment = "Known hosts file: " + (knownhostsfile or "(None)") + "\n"
	if sshkey:
		ssh_comment = ssh_comment + "Key pair: " + sshkey
		if sshpass:
			ssh_comment = ssh_comment + "\nWith passphrase"
	elif sshpass:
		ssh_comment = "With password"
	else:
		ssh_comment = ssh_comment + "No authentication set."
	droid.fullSetProperty("textSSH", "text", ssh_comment) 

def do_ssh(khf=None, k=None, p=None, loading=False):
	global droid, knownhostsfile, sshkey, sshpass
	if khf == None and not loading:
		khf=showsavefile(knownhostsfile, None, "Select known hosts file", False, "Select")
	if khf != None:
		knownhostsfile=khf
	if k == None and p == None and not loading:
 		r = showchoice("Select authentication", ["Key pair", "Password"])
		if r == "Key pair":
			f = showsavefile(sshkey, None, "Select private key file", False, "Select")
			if f != None:
				k = f
				if not os.path.exists(k):
					p = None
					p1 = showinput("Passphrase", "Enter passphrase for " + f, n="None", s=True)
					if p1 != None:
						p2 = showinput("Passphrase", "Confirm passphrase for " + f, s=True)
						if p1 != p2:
							showmessage("Passphrase", "Passphrases entered do not match!")
							k = None
						else:
							p = p1
					if k != None:
						showprogress("Generating 1024-bit RSA key", "SSH")
						key = RSAKey.generate(1024)
						showprogress("Writing to files")
						with open(f, "wb") as file:
							key.write_private_key(file, p)
						pubkey = key.get_name() + " " + key.get_base64()
						with open(f + ".pub", "w") as file:
							file.write(pubkey)
						droid.dialogDismiss()
						droid.makeToast("1024-bit RSA key generated in " + f)
						if showquestion("Public Key", pubkey, "Copy to clipboard", "Close"):
							droid.setClipboard(pubkey)
				else:
					p = showinput("Passphrase", "Enter passphrase for " + f, n="None", s=True)
		elif r == "Password":
			k = None
			p = showinput("Password", "Enter password for " + key, s=True)
	if k != None or p != None:
		sshkey = k
		sshpass = p
	do_ssh_comment()

def progress_to_log(text=None):
	global droid
	if text==None:
		droid.fullSetProperty("textLog", "text", "")
	else:
		oldText = droid.fullQueryDetail("textLog").result["text"]
		droid.fullSetProperty("textLog", "text", oldText + text)

def do_pull():
	global droid, repo, remoteclient, remoterepo, remotesrc
	if localrepo==None or remoterepo==None:
		droid.makeToast("Set repositories first!")
	else:
		showprogress("Fetching from remote repository", "Pull")
		progress_to_log()
		try:	
			remote_refs = remoteclient.fetch(remotesrc, repo, progress=progress_to_log)
		except:
			showerror("Remote Pull Error")
			return
		else:
			droid.dialogDismiss()
		if "HEAD" in remote_refs:
			repo.refs["refs/heads/master"] = remote_refs["HEAD"]
			if showquestion("Pull", "Do a checkout from the commit now?"):
				do_checkout()
		else:
			droid.makeToast("No HEAD to checkout yet!")

def do_checkout():
	global droid, localrepo, repo
	if localrepo==None:
		droid.makeToast("Set local repository first!")
	else:
		tree_id = repo["HEAD"].tree
		for entry in repo.object_store.iter_tree_contents(tree_id):
			path = os.path.join(localrepo, entry.path)
			if not os.path.exists(os.path.dirname(path)):
				os.makedirs(os.path.dirname(path))
			if os.path.exists(path) and not showquestion("Checkout", "Overwrite working copy of " + entry.path + "?"):
				continue 
			with open(path, 'wb') as file:
				file.write(repo.get_object(entry.sha).as_raw_string())
			try:
				os.chmod(path, entry.mode)
			except:
				droid.makeToast("Cannot match mode " + str(entry.mode) + " on " + entry.path) 

def log_recurse(sha):
	global repo
	commit = repo.get_object(sha)
	text = "Commit " + commit.id + "\n" + commit.message + "\n"
	for parent in commit.parents:
		text = text + log_recurse(parent)
	return text

def do_log():
	global droid, localrepo, repo
	if localrepo==None:
		droid.makeToast("Set local repository first!")
	else:
		if not "HEAD" in repo.refs:
			droid.makeToast("Repository is empty.")
		else:
			log = log_recurse(repo.refs["HEAD"])
			droid.fullSetProperty("textLog", "text", log)
			if showquestion("Log", "Copy to clipboard?"):
				droid.setClipboard(log)

def do_tree_for_commit(t, p=None):
	global droid, localrepo, repo
	changes = False
	deleted = []
	if p == None:
		top = localrepo
	else:
		top = os.path.join(localrepo, p)
	# Detect deleted files or directories
	for i in t:
		a = os.path.join(top, i)
		if p == None:
			r = i
		else:
			r = os.path.join(p, i)
		if not os.path.exists(a) and showquestion("Commit", "Delete " + r + "?"):
			progress_to_log("Deleted " + r)
			deleted.append(i)
			changes = True
	for i in deleted:
		del t[i]
	# Detect added or changed files or directories
	for i in os.listdir(top):
		a = os.path.join(top, i)
		if p == None:
			r = i
		else:
			r = os.path.join(p, i)
		if i in t:
			# File or directory modified
			oldmode, oldsha = t[i]
			if os.path.isdir(a):
				if showquestion("Commit", "Enter directory " + r + "?"):
					try:
						t2 = repo.tree(oldsha)
					except:
						t2 = Tree()
					if do_tree_for_commit(t2, r):
						repo.object_store.add_object(t2)
						t[i] = (oldmode, t2.id)
						changes = True
			else:
 				newmode = os.stat(a).st_mode 
 				with open(a, "rb") as file:
					newblob = Blob.from_string(file.read())
 					oldmode, oldsha = t[i]
					if oldmode != newmode or oldsha != newblob.id:
						if showquestion("Commit", "Change " + r + "?"):
							progress_to_log("Changed " + r)
							object_store.add_object(newblob)
							t[i] = (newmode, newblob.id)
							changes = True
		else:
			# File or directory added
			if os.path.isdir(a):
				if r != ".git" and showquestion("Commit", "Add directory " + r + "?"):
					t2 = Tree()
					if do_tree_for_commit(t2, r):
						repo.object_store.add_object(t2)
						t[i] = (040000, t2.id)
						changes = True
			else:
 				newmode = os.stat(a).st_mode
				with open(a, "rb") as file:
					newblob = Blob.from_string(file.read())
 					if showquestion("Commit", "Add " + r + "?"):
 						progress_to_log("Added " + r)
						repo.object_store.add_object(newblob)
						t.add(i, newmode, newblob.id)
 						changes = True
	return changes

def do_commit():
	global droid, localrepo, repo
	if localrepo==None:
		droid.makeToast("Set local repository first!")
	else:
 		object_store = repo.object_store
 		progress_to_log()
		if repo["refs/heads/master"] == None:
			tree = Tree()
		else:
			tree = object_store[repo["refs/heads/master"].tree]
		if do_tree_for_commit(tree):
			object_store.add_object(tree)
			commit = Commit()
			commit.tree = tree.id
			if repo.refs["refs/heads/master"] == None:
				commit.parents = []
				def_comment = "Initial commit"
			else:
				commit.parents = [repo.refs["refs/heads/master"]]
				def_comment = ""
			name = droid.fullQueryDetail("editName").result["text"]
			email = droid.fullQueryDetail("editEmail").result["text"]
			author = name + " <" + email + ">"
			commit.author = commit.committer = author
			commit.commit_time = commit.author_time = int(time())
			tz = parse_timezone('+0000')[0]
			commit.commit_timezone = commit.author_timezone = tz
			commit.encoding = "UTF-8"
			commit.message = showinput("Message", "Enter commit message", def_comment)
			object_store.add_object(commit)
			repo.refs['refs/heads/master'] = commit.id
 		else:
 			droid.makeToast("Nothing to commit.")

def push_helper_1(refs):
	global repo
	return { "refs/heads/master": repo.refs["refs/heads/master"] }

def push_helper_2(have, want, progress=None):
	global droid, repo
	return repo.object_store.generate_pack_contents(have, want, progress or progress_to_log)

def do_push():
	global droid, localrepo, remoteclient, remoterepo, remotesrc
	if localrepo==None or remoterepo==None:
		droid.makeToast("Set repositories first!")
	else:
		showprogress("Sending to remote repository", "Push")
		progress_to_log()
		try:
			remoteclient.send_pack(remotesrc, push_helper_1, push_helper_2)
		except:
			showerror("Remote Send Error")
			return
 		else:
 			droid.dialogDismiss()

def do_close(confirm=False):
	global exiting
	if not confirm or showquestion("Exit", "Are you sure you want to exit?"):
		exiting = True

def do_click(what):
	if what=="buttonLocalGit":
		do_local_git()
	elif what=="buttonRemoteGit":
		do_remote_git()
	elif what=="buttonSSH":
		do_ssh()
	elif what=="buttonPull":
		do_pull()
	elif what=="buttonCheckout":
		do_checkout()
	elif what=="buttonCommit":
		do_commit()
	elif what=="buttonPush":
		do_push()
	elif what=="buttonClose":
		do_close()
	elif what=="buttonLog":
		do_log()

def do_about():
	global license, urls
	text = """Gitter
Simple Git client
""" 
	if license:
		text = text + "\n" + license + "\n"
 	if os.path.exists("NEWS"):
		with open("NEWS", "r") as file:
			text = text + "\nVersion history:\n" + file.read()  
  	elif os.path.exists("ChangeLog"):
		with open("ChangeLog", "r") as file:
			text = text + "\nVersion history:\n" + file.read() 
	if showquestion("About", text, "Go to web site", "Close"):
		r = showchoice("View web site", urls.keys(), "View")
		if r != None:
			droid.view(urls[r])

def do_help():
	showmessage("Help", """Gitter is a simple Git client.
Git is a distributed version control system, used to keep a history of your work.
You can create or open a local repository, checkout or commit the latest. Changes to files or the repository are confirmed.
You can also connect to a remote repository. If connecting via SSH, you can create or open a key pair or set the password.
You can push the latest local changes to the remote repository or pull changes that have been made remotely.
Note that Gitter does not support branches.
Your settings will be remembered for next time.
Gitter is a work in progress.""")

def eventloop():
	global exiting
	while not exiting:
		event=droid.eventWait().result
		if event["name"]=="click":
			do_click(event["data"]["id"])
		elif event["name"]=="key":
			if event["data"]["key"]=="4":
				do_close(True)
		elif event["name"]=="About":
			do_about()
		elif event["name"]=="Help":
			do_help()
		elif event["name"]=="Exit":
			do_close(True)
		elif event["name"]=="screen":
			if event["data"]=="destroy":
				droid.makeToast("Ignoring destroy screen request")

from pickle import Pickler, Unpickler

os.chdir(os.path.dirname(__file__))
showlayoutfile("gitter.xml")
setoptionsmenu(["About", "Help", "Exit"])

if os.path.exists(".pickle"):
	with open(".pickle", "rb") as file:
		u = Unpickler(file)
		v = u.load()
		do_local_git(u.load(), True)
		if v>0:
			do_remote_git(u.load(), True)
		if v>1:
			droid.fullSetProperty("editName", "text", u.load() or "Your Name")
			droid.fullSetProperty("editEmail", "text", u.load() or "your@email")
		if v>2:
			do_ssh(u.load(), u.load(), u.load(), True)
else:
	droid.makeToast("First time user: Showing Help")
	do_help()

eventloop()

with open(".pickle", "wb") as file:
	p = Pickler(file)
	p.dump(3) # version
	p.dump(localrepo)
	p.dump(remoterepo)
	p.dump(droid.fullQueryDetail("editName").result["text"])
	p.dump(droid.fullQueryDetail("editEmail").result["text"])
	p.dump(knownhostsfile)
	p.dump(sshkey)
	p.dump(sshpass)

exit(0)
