#!/usr/bin/python
# Unit tests for the managed_records.retrieve_records function.
# Author: abukhari

import asyncio
import unittest
from managed_records import retrieve_records

PRIMARY_COLORS = ['red', 'blue', 'yellow']

class TestBadInputs(unittest.TestCase):
	def test_negative_page(self):
		options = {'page':-1, 'colors': []}
		with self.assertRaises(Exception) as context:
			loop = asyncio.get_event_loop()
			results = loop.run_until_complete(retrieve_records(options))
			self.assertTrue('parameter page must be a positive integer' in context.exception)

	def test_nonexistent_page(self):
		options = {'page':999, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(len(results['ids']), 0)
		self.assertEqual(results['nextPage'], None)
		self.assertEqual(results['previousPage'], None)
		self.assertEqual(results['closedPrimaryCount'], 0)
		self.assertEqual(len(results['open']), 0)

	def test_nonlist(self):
		options = {'page':-1, 'colors': "brown"}
		with self.assertRaises(Exception) as context:
			loop = asyncio.get_event_loop()
			results = loop.run_until_complete(retrieve_records(options))
			self.assertTrue('parameter colors must be a List' in context.exception)

	def test_nonnumber(self):
		options = {'page':"1st page", 'colors': ["brown"]}
		with self.assertRaises(Exception) as context:
			loop = asyncio.get_event_loop()
			results = loop.run_until_complete(retrieve_records(options))
			self.assertTrue('parameter page must be a Number' in context.exception)

	def test_missing_color(self):
		options = {'page':1}
		with self.assertRaises(Exception) as context:
			loop = asyncio.get_event_loop()
			results = loop.run_until_complete(retrieve_records(options))
			self.assertTrue('parameter page must be a Number' in context.exception)

	def test_unknown_color(self):
		options = {'page':1, 'colors': ["chartreuse"]}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(len(results['ids']), 0)
		self.assertEqual(results['nextPage'], None)
		self.assertEqual(results['previousPage'], None)
		self.assertEqual(results['closedPrimaryCount'], 0)
		self.assertEqual(len(results['open']), 0)

	def test_fills_in_page_1(self):
		options = {'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(results['nextPage'], 2)
		self.assertEqual(results['previousPage'], None)


class TestPaging(unittest.TestCase):
	def test_basic(self):
		options = {'page':1, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertGreater(len(results), 0)

	def test_page_bounds(self):
		options = {'page': 1, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(results['nextPage'], 2)
		self.assertEqual(results['previousPage'], None)

		options = {'page': 49, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(results['nextPage'], None)
		self.assertEqual(results['previousPage'], 48)

	def test_correct_page(self):
		options = {'page':20, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(results['nextPage'], 21)
		self.assertEqual(results['previousPage'], 19)

	def test_correct_results_size(self):
		options = {'page':2, 'colors': []}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertEqual(len(results['ids']), 10)


class TestResults(unittest.TestCase):
	def test_page_1_accuracy(self):
		options = {'page':1, 'colors': []}
		expected = {"previousPage":None,"nextPage":2,"ids":[1,2,3,4,5,6,7,8,9,10],"open":[{"id":2,"color":"yellow","disposition":"open","isPrimary":True},{"id":4,"color":"brown","disposition":"open","isPrimary":False},{"id":6,"color":"blue","disposition":"open","isPrimary":True},{"id":8,"color":"green","disposition":"open","isPrimary":False},{"id":10,"color":"red","disposition":"open","isPrimary":True}],"closedPrimaryCount":1};
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertCountEqual(results, expected)

	def test_page_50_accuracy(self):
		options = {'page': 50}
		expected = {"previousPage":49,"nextPage":None,"ids":[491,492,493,494,495,496,497,498,499,500],"open":[{"id":491,"color":"red","disposition":"open","isPrimary":True}],"closedPrimaryCount":6};
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))
		self.assertCountEqual(results, expected)


	def test_color_filter(self):
		options = {'colors': ['brown']}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))

		for result in results['open']:
			self.assertEqual(result['color'], 'brown')

		multi_colors = ['green', 'yellow']
		options = {'colors': multi_colors}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))

		for result in results['open']:
			self.assertTrue(result['color'] in multi_colors)

	def test_primary_colors(self):
		options = {'colors': PRIMARY_COLORS}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))

		for result in results['open']:
			self.assertEqual(result['isPrimary'], 'true')

		options = {'colors': ['green']}
		loop = asyncio.get_event_loop()
		results = loop.run_until_complete(retrieve_records(options))

		for result in results['open']:
			self.assertEqual(result['isPrimary'], 'false')





if __name__ == "__main__":
    unittest.main()