#!/usr/bin/python
# A replica of the Records JS API, but written in Python. Uses Flask to serve the /records API on Port 3000.
# This allows us to write and run a complete end-to-end example of the Fetch-Python Promise application.
# Author: abukhari

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import numbers
import decimal
import logging
import re
import urllib.parse


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)

RECORDS_DATA = app.config['RECORDS_DATA']
HOST = app.config['HOST']
PORT = app.config['PORT']

BAD_REQUEST = 'Bad Request'

# Convenience method: Try to parse param value as an integer, but return default_value if unable to do so.
def try_parse_int_or_default(value, default_value):
	try:
		return int(value)
	except ValueError:
		return default_value

# GET /records
@app.route("/records", methods=['GET'])
def getRecords():
	app.logger.debug("entered Records request")

	# parse querystring parameters
	limit_param = 100

	if 'limit' in request.args:
		limit_param = try_parse_int_or_default(request.args.get('limit'), 100)

	offset_param = 0

	if 'offset' in request.args:
		offset_param = try_parse_int_or_default(request.args.get('offset'), 0)

	# parse color string query parameter into a list, to mimic Javascript functionality
	query_string = urllib.parse.unquote(request.query_string.decode("utf-8"))

	# first, verify that color string is a list

	color_not_list_regex = re.compile('color=([a-z]*),?')
	if color_not_list_regex.match(query_string):
		return BAD_REQUEST, 400

	# now that we know color is a list, proceed with parsing it
	color_regex = re.compile('color\[\]=([a-z]*),?')
	color_filters = color_regex.findall(query_string)

	app.logger.debug("limit_param is " + str(limit_param))
	app.logger.debug("offset_param is " + str(offset_param))
	app.logger.debug("color_filters is {}".format(color_filters))

	response = []

	# check input constraints (color being a list is checked above)
	if not isinstance(limit_param, numbers.Number) or limit_param < 0 or not isinstance(offset_param, numbers.Number) or offset_param < 0:
		return BAD_REQUEST, 400

	# return RECORDS_DATA filtered by specified color filters and limited to offset_param:offset_param+limit
	if len(color_filters) > 0:
		response = list(filter(lambda list_item: list_item['color'] in color_filters, RECORDS_DATA))[offset_param:offset_param+limit_param]
	else:
		response = RECORDS_DATA[offset_param:offset_param+limit_param]

	return jsonify(response), 200

if __name__ == '__main__':
	app.logger.debug("Starting Fetch Server. Total number of records is {}".format(len(RECORDS_DATA)))
	app.run(host=HOST, port=PORT)
