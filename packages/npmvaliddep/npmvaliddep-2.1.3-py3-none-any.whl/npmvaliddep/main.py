import argparse
import os
import json
import sys
from npmvaliddep.argumentmapper import *

def main(input_args = None):

    if input_args is None:
        input_args = sys.argv[1:]

    my_parser = argparse.ArgumentParser(description='Dependency Checker')
    my_parser.add_argument('--check', nargs=1, type=str,
                        help='Specify the csv path !!')
    my_parser.add_argument('--deps', default=[], nargs='+',
                        help='Specify the dependencies name@version !!')
    my_parser.add_argument("--output", nargs=1, type=str, 
                        help="Specify the output path, if not defined then it will generate the output file in user home directory !!")
    my_parser.add_argument('--createpr', default=False, action=argparse.BooleanOptionalAction,
                        help='Specify if you want to generate pull request for the dependency change !!')
    my_parser.add_argument('--getgithubcreds', default=False, action=argparse.BooleanOptionalAction, 
                        help="Check your github configurations !!")
    my_parser.add_argument("--setgithubcreds", default=False, action=argparse.BooleanOptionalAction, 
                        help="Set your github username and password/token !!")
    my_parser.add_argument("--matchgithubpass", default=False, action=argparse.BooleanOptionalAction,
                        help="Match github password/token !!")

    args = my_parser.parse_args(input_args)

    github_path = os.path.join(os.getcwd(), 'github.json')
    exist = os.path.exists(github_path)
    if not exist:
        temp_github_json = {"github_username": "", "github_password": ""}
        with open(github_path, "w") as outfile:
            outfile.write(json.dumps(temp_github_json, indent = 4))
    
    if args.setgithubcreds:
        setgithubcreds()

    if args.getgithubcreds:
        getgithubcreds()

    if args.matchgithubpass:
        matchgithubpass()
    
    if args.check:
        check_dependency(args)
