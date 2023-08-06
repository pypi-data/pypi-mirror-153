import aiohttp

class NumberNotAvailable(Exception):
    """Raised when a phone number is not provided."""

class NotFound(Exception):
    """Raised when a phone number is not provided."""


class InvalidApiKey(Exception):
    """Raised when an invalid API key is provided."""


class InvalidInput(Exception):
    """Raised when multiple errors are raised."""


class FiveSim(object):
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.api_url = "https://5sim.net/v1"
        
    async def fetch(self, method = "GET", function = "", params = None, headers = None, data = None):
        headers = {"Accept": "application/json"}
        if self.api_key and "guest" not in function: headers["Authorization"] = self.api_key
        async with aiohttp.ClientSession() as client_session:
            response = await client_session.request(method = method, url = self.api_url + function, params = None, headers = headers, data = data)
            if response.status == 401:
                raise InvalidApiKey("Api key is not valid or expired")
            elif response.status == 400:
                raise InvalidInput("Invalid Input")
            elif response.status == 404:
                raise NotFound("Input Not Found")
            elif response.status == 200:
                content = await response.json()
                return content
            else:
                return response.text
        
    async def get_profile(self):
        """Provides profile data: email, balance and rating."""
        return await self.fetch("GET", "/user/profile")
        
    async def order_history(self, category: str, limit: str = None, offset: str = None, order: str = None, reverse: str = None):
        """Provides orders history by choosen category."""
        return await self.fetch("GET", "/user/orders?category={}".format(category))
        
    async def payment_history(self, limit: str = None, offset: str = None, order: str = None, reverse: str = None):
        """Provides payments history."""
        return await self.fetch("GET", "/user/payments")
        
    async def product_details(self, country: str = "any", operator: str = "any"):
        """To receive the name, the price, quantity of all products, available to buy."""
        return await self.fetch("GET", "/guest/products/{}/{}".format(country, operator))
        
    async def get_prices(self):
        """Return prices of products of countries."""
        return await self.fetch("GET", "/guest/prices")

    async def get_prices_by_country(self, country: str):
        """Returns product prices by country and specific product."""
        return await self.fetch("GET", "/guest/prices?country={}".format(country))
    
    async def get_prices_by_country_and_product(self, country: str, product: str):
        """Returns product prices by country and specific product."""
        return await self.fetch("GET", "/guest/prices?country={}&product={}".format(country, product))
    
    async def get_prices_by_product(self, product: str):
        """Returns product prices by country and specific product."""
        return await self.fetch("GET", "/guest/prices?product={}".format(product))
    
    async def buy_activation_number(self, country: str, operator: str, product: str):
        """Buy a activation number."""
        return await self.fetch("GET", "/user/buy/activation/{}/{}/{}".format(country, operator, product))
        
    async def buy_hosting_number(self, country: str, operator: str, product: str):
        """Buy a hosting number."""
        return await self.fetch("GET", "/user/buy/hosting/{}/{}/{}".format(country, operator, product))
        
    async def re_buy_number(self, product: str, number: str):
        """Buy again a old number."""
        return await self.fetch("GET", "/user/reuse/{}/{}".format(product, number))
    
    async def check_order(self, id: str):
        """Check order history of a number."""
        return await self.fetch("GET", "/user/check/{}".format(id))
        
    async def get_sms(self, id: str):
        """Get sms of a number."""
        return await self.fetch("GET", "/user/check/{}".format(id))
        
    async def finish_order(self, id: str):
        """Finish a order by order."""
        return await self.fetch("GET", "/user/finish/{}".format(id))
        
    async def cancel_order(self, id: str):
        """Cancel a order by order's id."""
        return await self.fetch("GET", "/user/cancel/{}".format(id))
        
    async def ban_order(self, id: str):
        """Ban a order by order's id."""
        return await self.fetch("GET", "/user/ban/{}".format(id))
    
    async def sms_inbox_list(self, id: str):
        """Get SMS inbox list by order's id."""
        return await self.fetch("GET", "/user/sms/inbox/{}".format(id))
        
    async def crypto_rates(self):
        """Return rates of cryptocurrencies."""
        return await self.fetch("GET", "/user/payment/crypto2/rates")
        
    async def get_deposit_address(self, amount: str, currency: str, address_type: str = None):
        """Return address to crypto payment."""
        data = {"amount": amount, "currency": currency, "address_type": address_type}
        return await self.fetch("POST", "/user/payment/crypto2/invoice", data = data)
        
    async def get_notifications(self, lang: str):
        """Get a flash notification."""
        return await self.fetch("GET", "/guest/flash/{}".format(lang))
        
    async def vendor_stats(self):
        """Return Vendor statistics."""
        return await self.fetch("GET", "/user/vendor")
        
    async def wallets_reserve(self):
        """Available reserves currency for partner."""
        return await self.fetch("GET", "/vendor/wallets")
        
    async def vendor_orders_history(self, category: str):
        """Provides vendor's orders history by chosen category."""
        return await self.fetch("GET", "/vendor/orders?category={}".format(category))
        
    async def vendor_payments_history(self):
        """Provides vendor's payments history."""
        return await self.fetch("GET", "/vendor/payments")
        
    async def create_payouts(self, receiver: str, method: str, amount: str, fee: str):
        """Create payouts for a partner."""
        data = {"receiver": receiver, "method": method, "amount": amount, "fee": fee}
        return await self.fetch("POST", "/vendor/withdraw", data = data)
        
    async def countries_list(self):
        """Returns a list of countries with available operators for purchase."""
        return await self.fetch("GET", "/guest/countries")
