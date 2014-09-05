#!/usr/bin/env python
import base64
import urllib2 as url
from google.appengine.api import urlfetch

api_key = "secret"
shared_secret = "secret"
#Shopify_Base is prefixed with a _ so that it cannot be used outside of its
#own file. Since it just serves as a template for other API classes to inherit
#from, it should never be called directly.
#@classmethods are used so that API classes can be called directly, without having
#to first create an instances of them.

class _Shopify_Base(object):
    prefix="override_me_please"
    
    @classmethod
    def all(self,shop,password):
    	b64string = base64.b64encode('%s:%s' % (api_key, password))
    	headerstring = { "Authorization" : "Basic %s" % b64string }
    	url = "https://%s/admin/%s.json" % (shop, self.prefix)
    	request = urlfetch.fetch(url = url, headers = headerstring)
    	return request.content
    
    @classmethod
    def one(self, shop, password, id):
       	b64string = base64.b64encode('%s:%s' % (api_key, password))
       	headerstring = { "Authorization" : "Basic %s" % b64string }
       	url = "https://%s/admin/%s/%s.json" % (shop, self.prefix, id)
       	request = urlfetch.fetch(url = url, headers = headerstring)
       	return request.content

class Event(_Shopify_Base):
	prefix = "events"

class Order(_Shopify_Base): 
	prefix = "orders"

class Product(_Shopify_Base): 
	prefix = "products"
	
#Transactions don't follow the url pattern of the above classes
#so they cannot easily extend _Shopify_Base. 
class Transaction(object): 

	@classmethod
	def all(self, shop, password, order_id):
	    url = "https://%s/admin/orders/%s/transactions.json" % (shop, order_id)
	    b64string = base64.b64encode('%s:%s' % (api_key, password))
	    headerstring = { "Authorization" : "Basic %s" % b64string }
	    request = urlfetch.fetch(url = url, headers = headerstring)
	    return request.content
	@classmethod
	def one(self, shop, password, order_id, transaction_id):
	    b64string = base64.b64encode('%s:%s' % (api_key, password))
	    headerstring = { "Authorization" : "Basic %s" % b64string }
	    url = "https://%s/admin/orders/%s/transactions/%s.json" % (shop, order_id, transaction_id)
	    request = urlfetch.fetch(url = url, headers = headerstring)
	    return request.content
