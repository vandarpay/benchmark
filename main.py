import subprocess
from datetime import datetime
import json
import argparse

PATH_TO_HEY = "./hey"
args = None

def run(url, template, method='GET', contents_file='',
        contents='', count=200, connections=50, 
        headers=[]):
    command = f"{PATH_TO_HEY} -m {method} -n {count} -c {connections} -o csv "
    
    for header in headers:
        command += f"-H \"{header}\" "
    
    if contents_file: # if contents_file is specified, contents is ignored
        command += f"-D \"{contents_file}\" "
    
    elif contents:
        if type(contents) in [dict, list] and not args.no_convert:
            contents = json.dumps(contents) # The program assumes the data type is application/json
        
        command += f"-d \"{contents}\" "
    
    command += url

    # Template may have any of the following variables in it for better output clarity
    template = template.format(count=count, connections=connections, 
                               ymd=datetime.now().strftime('%Y_%m_%d'),
                               method=method)
    
    # Use Template and override the file if it exists to write the new results
    with open(f"data/{template}.csv", "w+") as file:
        subprocess.run(command, stdout=file, shell=True)

def run_scenario(scenario: dict):
    collection = scenario.pop('collection')

    for count, connections in collection:
        if not args.quiet:
            print(f'Making {count} requests with {connections} connections')

        scenario['count'], scenario['connections'] = count, connections
        run(**scenario)

if __name__ == '__main__':

    try:
        # Setup Argsparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--file', '-f', help="the scenario file to process through", type= str)
        parser.add_argument('--no-convert', help="do not convert the contents in scenarios to json encoded strings", action='store_true')
        parser.add_argument('--quiet', '-q', help="do not print the notices and progress updates (errors will still dump to STDERROR)", action='store_true')
        args = parser.parse_args()
        file = args.file
        if file is None:
            file = input('Enter the path to your scenario file:')
        
        # Read & Run File
        with open(file, 'r') as file:
            for scenario in json.load(file):
                run_scenario(scenario)
            if not args.quiet:
                print('Finished')
            
    except KeyboardInterrupt:
        exit()