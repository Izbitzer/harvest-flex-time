# Harvest hour calculator

Tool to calculate how many hours you have worked compared to the expected amount. It should account for holidays
and "klämdagar".

## Prerequisites

You need to have `pipenv` installed, and you also need to generate a token for Harvest. It can be done at
https://id.getharvest.com/developers.

## Running

First, initialize the environment using `pipenv install` in the root directory.

Then run using `pipenv run python -m calculator <start-date> <end-date> <token> [<user_id>]`

You can also set the parameters with the environment variables `START_DATE`, `END_DATE`, `TOKEN`, `USER_ID`.

The `user_id` parameter should be used if getting the hours for another person, the default behavior is to get your own.

