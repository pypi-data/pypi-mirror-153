FXCM provides a RESTful API to interact with its trading platform. Among others, it allows the retrieval of historical data as well as of streaming data. In addition, it allows to place different types of orders and to read out account information. The overall goal is to allow the implementation automated, algortithmic trading programs.

fxcmpy.py is a Python wrapper package for that API.

# To get started with the the API and the package, a demo account with FXCM is sufficient. You can open such an account under https://www.fxcm.com/uk/forex-trading-demo/.

# Installation happens via pip install on the command line.

		pip install fxcmpy

# To connect to the API, you need an API token that you can create or revoke from within your (demo) account in the Trading Station https://tradingstation.fxcm.com/.

In an interactive context, you can use e.g. a variable called TOKEN to reference your unique API token.

		TOKEN = YOUR_FXCM_API_TOKEN

Connecting to the server, then boils down to the following line of code.

		con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error', log_file='log.txt', server='demo')

The detailed documentation of the API is found under:

https://github.com/fxcm/RestAPI