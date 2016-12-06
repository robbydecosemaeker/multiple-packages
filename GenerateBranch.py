import hashlib
import os
import time
import datetime
from datetime import date

from github import Github

import csv
import sys

repo_name = "multiple-packages"
branch_name = 'new-one7'

g = Github("8debec4b4734776bf8b16203c50af9046f41afdb")



repo = g.get_user().get_repo(repo_name)

master_branch = repo.get_branch(repo.default_branch)

PY3 = sys.version_info[0] > 2

def read_properties(filename, delimiter=':'):
    ''' Reads a given properties file with each line of the format key=value.
        Returns a dictionary containing the pairs.
            filename -- the name of the file to be read
    '''
    open_kwargs = {'mode': 'r', 'newline': ''} if PY3 else {'mode': 'rb'}
    with open(filename, **open_kwargs) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, escapechar='\\',
                            quoting=csv.QUOTE_NONE)
        return {row[0]: row[1] for row in reader}

def write_properties(filename, dictionary, delimiter=':'):
    ''' Writes the provided dictionary in key sorted order to a properties
        file with each line in the format: key<delimiter>value
            filename -- the name of the file to be written
            dictionary -- a dictionary containing the key/value pairs.
    '''
    open_kwargs = {'mode': 'w', 'newline': ''} if PY3 else {'mode': 'wb'}
    with open(filename, **open_kwargs) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, escapechar='\\',
                            quoting=csv.QUOTE_NONE)
        writer.writerows(sorted(dictionary.items()))


for entry in os.scandir("."):
   if not entry.name.startswith('.') and entry.is_dir():
       print("checking status for: " + entry.name)
       config = read_properties(os.path.join(entry.path, "DESCRIPTION"))
       last_updated = master_branch.commit.commit.committer.date
       print(last_updated)
       update_pattern = config.get("UpdateRate-YMD")
       print(update_pattern, len(update_pattern))
       if update_pattern != None and len(update_pattern.lstrip()) == 3:
           weeks = int(update_pattern[0:1]) * 52
           weeks += int(update_pattern[1:2])* 30
           days = int(update_pattern[2:3])           
           should_update_before = (last_updated + datetime.timedelta(weeks = weeks, days = days))
           print(should_update_before.isoformat() + "<" + date.today().isoformat(), should_update_before.isoformat() < date.today().isoformat())
           if should_update_before.isoformat() < date.today().isoformat():
               print("we should update", config.get("Package"))
               

##
##

##
##try:
##    print("Creating new branch \"" + branch_name + "\" from " + master_branch.name)
##    ref = g.get_user().get_repo(repo).create_git_ref("refs/heads/" + branch_name,master_branch.commit.sha)
##expect ApiError as e:
##    print (e, e.request, e.response)
##
##new_branch = g.get_user().get_repo(repo).get_branch(branch_name)
##edit_url = new_branch.raw_data.get("_links").get("html")
##
##issue = g.get_user().get_repo("multiple-packages").create_issue("Issue for " + branch_name, "To edit click here: " + edit_url)
##issue.add_to_labels("branch->" + new_branch.name)
