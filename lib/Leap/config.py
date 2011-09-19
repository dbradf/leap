#!/usr/bin/env python
# Configuration for leap script

import Leap.defaults
import os
import shutil

from Leap.project import LeapProject

class LeapConfig:
    def __init__(self, config_file=Leap.defaults.config_file):
        self.attributes = {}
        self.projects   = []
        self.config_filename = config_file
        self.parse_config_file(config_file)


    def parse_config_file(self, config_file):
        if not os.path.exists(config_file):
            if not create_config_file():
                return None

        for line in open(config_file):
            str_parts = line.rstrip().split('=')
            if len(str_parts) > 1:
                self.set_attribute(str_parts[0], str_parts[1])
            else:
                self.add_project(str_parts[0])

    def set_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def add_project(self, project):
        self.projects.append(project)

    def get_projects(self):
        return self.projects

    def get_project_directory(self):
        return self.attributes['leap_directory']

    def get_project(self, project_name):
        found_project = False
        for proj in self.get_projects():
            if proj == project_name:
                found_project = True

        if found_project:
            return LeapProject(self.get_project_directory(), project_name)
        else:
            return None

    def add_new_project(self, project_name, project_file):
        if not os.path.exists(project_file):
            print "Error: Could not find project file: %s" % project_file
            return 1
        shutil.copyfile(project_file, "%s%s%s" % (
            self.get_project_directory(), os.sep, project_name))
        config_file = open(self.config_filename, "a")
        config_file.write("%s\n" % project_name)
        config_file.close()
        print "Project: '%s' Added" % project_name
        return 0



def create_config_file():
    print "Config file does not exist, create? [Y\\n]"
    create_file = raw_input('?')
    if create_file == "Y" or create_file == 'y' or create_file == '':
        create_new_config()
        return True
    return False

def query_option(query, default):
    print "%s? [%s]" % (query, default)
    user_input = raw_input("?")
    if user_input == "":
        return default
    return user_input


def create_new_config():
    config_location  = query_option("Config file location", 
                                    Leap.defaults.config_file)
    config_directory = query_option("Project directory", 
                                    Leap.defaults.config_directory)
    install_config(config_location, config_directory)


def install_config(location, directory):
    config_file = open(location, 'w')
    config_file.write("leap_directory=%s\n" % (directory))
    config_file.close()

    if not os.path.exists(directory):
        os.makedirs(directory)

