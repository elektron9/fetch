#!/usr/bin/python
# Provides an async function named retrieve_records that can be used 
# as part of an async/await chain to interact with the Records API and
# return transformed data according to the Fetch API specs.
# Author: abukhari

import asyncio
import logging
import numbers
import requests

logging.basicConfig(level=logging.DEBUG)
PRIMARY_COLORS = ['red', 'blue', 'yellow']
PAGE_SIZE = 10
RECORDS_API_HOST = 'http://localhost:3000'

# parse page, colors from options dict, call /records API and await result.
# param options: a dictionary containing two keys: page, and colors.
async def retrieve_records(options):
	# check inputs
	if not isinstance(options, dict):
		raise TypeError('parameter options must be a Dictionary')

	# parse options dict into page, colors
	page = 1
	if 'page' in options:
		page = options['page']

	colors = []
	if 'colors' in options:
		colors = options['colors']

	records = []
	try:
		logging.debug("calling records API")
		records = await get_records(page, colors)
		logging.debug("retrieved records")
	except IOError:
		logging.debug("failed to retrieve data")

	return records

# make request against /records API
# param page: the page of results to retrieve from the API. A page has
#  PAGE_SIZE records.
# param colors: the list of colors to retrieve from the API.
async def get_records(page, colors):
	# check inputs
	if not isinstance(page, numbers.Number):
		raise TypeError('parameter page must be a Number')
	if not isinstance(colors, list):
		raise TypeError('parameter colors must be a List')
	if page <= 0:
		raise ValueError('parameter page must be a positive integer')

	# create request to /records API, correctly transforming constraints
	# Process pages PAGE_SIZE items at a time
	# Limit results to the colors specified. If colors is an empty 
	# array, return all colors

	# request one item before and one after the chosen offset so we can
	# know if there are previous/next pages of results available
	limit = PAGE_SIZE + 2 
	offset = (page * PAGE_SIZE) - 1

	query_params = {'limit': limit, 'offset': offset, 'color[]': colors}
	results = requests.get(RECORDS_API_HOST + '/records', params=query_params)

	if results.status_code != 200:
		print("API request failed")
		return None

	# check if there's another page available
	# (if there were at least PAGE_SIZE + 2 elements returned)
	is_next_page = False
	if len(results.json()) == PAGE_SIZE + 2:
		is_next_page = True

	# only use the middle PAGE_SIZE number of results for the response
	results_json = results.json()[1:PAGE_SIZE+1]

	# transform the results into an output array containing:

	# ids: An array containing the ids of all items returned from the request.
	ids = [element['id'] for element in results_json]

	# add an isPrimary key to all the elements to prepare for the next two
	# output array elements.
	augmented_elements = [dict(item, **{'isPrimary':'true'}) 
		if item['color'] in PRIMARY_COLORS 
		else dict(item, **{'isPrimary':'false'}) for item in results_json]

	# open: An array containing all of the items returned from the request that
	#  have a disposition value of "open". Add a fourth key to each item 
	#  called isPrimary indicating whether or not the item contains a primary 
	#  color (red, blue, or yellow).
	open_elements = list(filter(lambda list_item: list_item['disposition'] ==
	 	'open', augmented_elements))

	# closedPrimaryCount: The total number of items returned from the request 
	#  that have a disposition value of "closed" and contain a primary color.
	closed_primary_count = len(list(filter(lambda list_item: 
		list_item['disposition'] == 'closed' 
		and list_item['color'] in PRIMARY_COLORS, augmented_elements)))

	# previousPage: The page number for the previous page of results, or null 
	#  if this is the first page.
	previous_page = None
	if page > 1 and len(results_json) > 0 and results.json()[0] is not None:
		previous_page = page - 1

	# nextPage: The page number for the next page of results, or null if this 
	#  is the last page.
	next_page = None
	if is_next_page:
		next_page = page + 1

	return {'ids': ids,
	 'open': open_elements, 
	 'closedPrimaryCount': closed_primary_count, 
	 'previousPage': previous_page,
	 'nextPage': next_page}
