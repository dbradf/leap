

import optparse

import Leap.defaults

from Leap.config  import LeapConfig
from Leap.project import LeapProject


version = "0.1"
usage   = "[options] project target1 [target2 .. targetN]"


def build_arg_parser():
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option("-l", "--list", dest="list_projects", action="store_true",
                      help="list known projects")
    parser.add_option("-s", "--source", dest="source", 
                      help="directory to look for files to copy")
    parser.add_option("--config", dest="config", default=Leap.defaults.config_file,
                      help="specify config file (default=%s)" % (Leap.defaults.config_file))
    return parser


def list_projects(config):
    for proj in config.get_projects():
        print proj


def main():
    arg_parser = build_arg_parser()
    (options, args) = arg_parser.parse_args()

    config = LeapConfig(options.config)

    if len(args) == 0 or options.list_projects:
        list_projects(config)
        exit(0)

    if len(args) == 1:
        arg_parser.error("Missing arguments")

    project = config.get_project(args[0])

    for target in args[1:]:
        project.migrate(target)

