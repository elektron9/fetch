# Fetch

This is a solution to the Fetch/Records API problem set.

## Development Environment

* Operating System: Windows Linux Subsystem 2, running Ubuntu 20.04 LTS
* Python 3.8.2 with Pip 20.1.1
* All Python dependencies listed in requirements.txt


## How to run this solution
* Ensure you have the correct version of Python and Pip installed.
* Create a virtualenv via `virtualenv fetchenv`, activate it via `source fetchenv/bin/activate`, and then run `pip install -r requirements.txt` to install all dependencies.
* Update any configuration items for the Records API in `records_api/config.py`
* Start the Records API server by running `python records_api/records_api.py`
* Import the provided `retrieve_records` function into your Python script by adding the statement `from managed_records import retrieve_records` (you will need to ensure that this directory is in your `$PATH`)
* You can now use the provided function by adding `await retrieve_records(options)` to your Python script. See `example_script.py` for an example of this.

## Unit Tests
* Unit tests have been provided in the `unit_test.py` class. To run them:
  * Start the Records API server by running `python records_api/records_api.py`
  * Then, run `python unit_test.py` to run the tests.
