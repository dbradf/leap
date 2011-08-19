#!/usr/bin/env python

import re
import os

class LeapProject:
    def __init__(self, config_dir, project_name):
        self.config_directory = config_dir
        self.name = project_name
        self.files = []
        self.before_file = ""
        self.after_file  = ""
        self.parse_project_file()

    def parse_project_file(self):
        state = "none"
        before_code = ""
        after_code  = ""
        file_list   = ""
        for line in open(self.config_directory + '/' + self.name):
            if re.match('before {', line):
                state = "before"
            elif re.match('after {', line):
                state = "after"
            elif re.match('^}', line):
                state = "none"
            else:
                if state == "before":
                    before_code = before_code + line
                elif state == "after":
                    after_code = after_code + line
                elif len(line.rstrip()) > 0:
                    file_list = file_list + line

        if len(before_code) > 0:
            self.before_file = before_code

        if len(after_code) > 0:
            self.after_file = after_code


        for line in file_list.rstrip().split('\n'):
            target = ""
            destination = ""
            str_parts = line.rstrip().split(' ')
            if len(str_parts) > 1:
                target = str_parts[0]
                destination = str_parts[1]
            else:
                target = str_parts[0]
                destination = str_parts[0]
            self.add_file(target, destination)

    def add_file(self, target, destination):
        self.files.append((target, destination))

    def migrate(self, target):
        self.run_before(target)

        for file_pair in self.files:
            flags = ""
            if os.path.isdir(file_pair[0]):
                flags = "-r"
            self.send_file(target, file_pair[0], file_pair[1], flags)

        self.run_after(target)

    def run_before(self, target):
        if len(self.before_file) > 0:
            tmp_file = "/tmp/leap_before_file"
            self.create_file(tmp_file, self.before_file)
            self.send_file(target, tmp_file, tmp_file, "")
            self.execute_file(target, tmp_file)
            self.remove_file(target, tmp_file)


    def run_after(self, target):
        if len(self.after_file) > 0:
            tmp_file = "/tmp/leap_after_file"
            self.create_file(tmp_file, self.after_file)
            self.send_file(target, tmp_file, tmp_file, "")
            self.execute_file(target, tmp_file)
            self.remove_file(target, tmp_file)

    def send_file(self, target, target_location, destination_location, flags):
        os.system("scp %s %s %s:%s" % (
            flags, target_location, target, destination_location))

    def create_file(self, filename, file_contents):
        tmp_file = open(filename, "w")
        tmp_file.write(file_contents.rstrip())
        tmp_file.close()

    def execute_file(self, target, exe_file):
        os.system("ssh %s chmod +x %s" % (target, exe_file))
        os.system("ssh %s %s" % (target, exe_file))

    def remove_file(self, target, rm_file):
        os.system("ssh %s rm -rf %s" % (target, rm_file))
        
        

        


