#!/usr/bin/python
# An example script that uses the retrieve_records function from the 
# managed_records.py file as part of an async/await chain.
# Author: abukhari

import asyncio
from managed_records import retrieve_records

async def example_function(options):
	records = []
	try:
		records = await retrieve_records(options)
	except IOError:
		return False

	print(records)



if __name__ == '__main__':
	options = {'page':2, 'colors': []}
	loop = asyncio.get_event_loop()
	loop.run_until_complete(example_function(options))
