# Pokitdok-Mongo
Basic python code and instructions for making Poktidok API calls to dump JSON containing patient data to a MongoDB database. 

Uploaded here for your reference and to potentially save 3-4 hours of your time, since this is a common task...

## Importing claims for API call

The function used in the py file imports the claim data for each API call from another MongoDB database. Note that you can replace this function to retrieve call data from wherever you have stored it. However, it might be more time-effective to move this data to MongoDB, since you'll be exporting there anyway.

## Exporting data to MongoDB

The JSON is dumped over the range you've specified to a database that you've named.

In the file, I make a call to the /eligibility/ endpoint. Note, that this can easily be adjusted. However, the JSON required for the POST call varies by endpoint.

See [Pokitdok's documemtation](https://platform.pokitdok.com/documentation/v4/#activities) for the parameters of each call.
