#!/usr/bin/env python
# Configuration for leap script

class LeapConfig:
    def __init__(self, config_file="~/.leaprc"):
        self.attributes = {}
        self.projects   = []
        self.parse_config_file(config_file)


    def parse_config_file(self, config_file):
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
