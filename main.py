import subprocess
from datetime import datetime
import json
import argparse
from time import sleep

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
        
        command += f"-d \'{contents}\' "
    
    command += url
    if args.verbose or args.dry:
        print(f'Running Hey with the following command:\n{command}')
    
    if args.dry:
        return

    # Template may have any of the following variables in it for better output clarity
    template = template.format(count=count, connections=connections, 
                               ymd=datetime.now().strftime('%Y_%m_%d'),
                               method=method)
    
    # Use Template and override the file if it exists to write the new results
    path = f"data/{template}.csv"
    if args.verbose:
        print(f"Saving results into {path}")
    
    with open(path, "w+") as file:
        subprocess.run(command, stdout=file, shell=True)

def run_scenario(scenario: dict):
    collection = scenario.pop('collection')

    total = 0
    for count, connections in collection:
        if not args.quiet:
            print(f'Making {count} requests with {connections} connections')
        
        if args.testing:
            count, connections = 2, 1


        
        scenario['count'], scenario['connections'] = count, connections
        run(**scenario)
        if args.testing:
            break

        total += count

        if args.backoff > 0 and total % args.backoff == 0:
            wait = args.wait
            if not args.quiet:
                print(f'Reached a total of {total} requests, waiting for {wait} seconds')
            sleep(wait)

if __name__ == '__main__':

    try:
        # Setup Argsparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--file', '-f', help="the scenario file to process through", type= str)
        parser.add_argument('--no-convert', help="do not convert the contents in scenarios to json encoded strings", action='store_true')
        parser.add_argument('--quiet', '-q', help="do not print the notices and progress updates (errors will still dump to STDERROR)", action='store_true')
        parser.add_argument('--verbose', '-v', help="show more technical information", action='store_true')
        parser.add_argument('--dry', help="only print the command instead of running hey", action='store_true')
        parser.add_argument('--testing', help="run the scenario only once with 2 requests and 1 concurrency", action='store_true')
        parser.add_argument('--backoff', '-b', help="the number of requests after which the program should backoff and wait (the total number of requests in each collection must be below this number and disivable by it for this feature to function correctly)", type=int, default=-1, metavar='[number]')
        parser.add_argument('--wait', '-w', help="the number of seconds the program should wait before continuing", type=int, default=60, metavar='[number]')
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