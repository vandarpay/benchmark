# Vandar Benchmark Wrapper
Vandar Benchmark Wrapper is a Python tool for the [rakyll/hey](https://github.com/rakyll/hey) benchmarking tool that makes it easier to design and use pre-built scenarios for load-testing and determining performance improvements.

## Setup
You may either clone this project using git or download a zip file containing this project, after extracting it, you need to make sure to follow these two steps:
1. Make sure you have Python 3.6+ installed on your system.
2. Download a compiled hey binary from [here](https://github.com/rakyll/hey/tree/master#installation) (or [use this specific version](https://github.com/rakyll/hey/tree/master#installation)), rename it to `hey` and place it in project's folder.

This project has been tested on Linux, we expect it to work with Mac or any *nix operating system that supports python. Windows has not been tested and may not be supported.

## Usage 
Before starting with this package, please take a moment to read the documentation for hey.

In Vandar Benchmark Wrapper, we use something called a **scenario** object for creating pre-determined requests, these objects can run with different numbers of connections and requests multiple times, as determined by their **collection** object.

Once a scenario is run, the output for the run is stored inside the `data` folder in CSV format with the name you give it through the `template` entry inside a scenario.

Scenario objects are stored in json files, each json file contains a root array which may contain a number of related scenario objects.
```json
[
    {
        "url": "https://example.org/",
        "method": "GET",
        "headers": [
            "Accept: text/html"
        ],
        "collection": [
            [2, 1],
            [4, 2]
        ],
        "template": "example_{count}_{connections}_{ymd}",
        "contents": {}
    }
]
```
In this example:
1. `url` is the path you're going to send requests to (same as hey)
2. `method` the HTTP method you want to use (same as hey)
3. `headers` an array of your heards in form of string
4. `collection` an array, containing every variation of number of requests and connectionss respectively. (`[<number_of_requests>, <number_of_connections>]`)
5. `template` is a name you give your output file, which can contain the following special variables:
5.1. `{count}` the number of total requests to be sent as determined in `collection`
3.2. `{connection}` the number of connections used for this benchmark as determined in `collection`
5.3. `{ymd}` the current date in `Y_m_d` format
5.4. `{method}` the method used to send this request (e.g GET)
6. `contents` HTTP body either in form of an object or array (which is automatically converted to a json encoded object, pass `--no-convert` to stop this from happening)
6.1. please note that you will need to escape the ' character when using `contents`
6.1. alternatively, you may have a `contents_file` string instead which determines the path to the body of your content.

Once you have built your scenario in a JSON file, you can run the wrapper using the following command:
```python3 main.py -f /path/to/your_file.json```
or you may run the file without arguments and enter your file path interactively.

Run `python3 main.py -h` for more information.

After running, the test results will be saved with your determined name template inside the `data/` folder.
## License
All files in this project (unless otherwise noted) are licensed under the MIT License. See LICENSE for more.