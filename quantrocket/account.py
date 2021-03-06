# Copyright 2017 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from quantrocket.houston import houston
from quantrocket.cli.utils.output import json_to_cli
from quantrocket.cli.utils.files import write_response_to_filepath_or_buffer
from quantrocket.cli.utils.parse import dict_strs_to_dict, dict_to_dict_strs

def download_account_balances(filepath_or_buffer=None, output="csv",
                              start_date=None, end_date=None,
                              latest=False, accounts=None, below=None,
                              fields=None, force_refresh=False):
    """
    Query IB account balances.

    Parameters
    ----------
    filepath_or_buffer : str or file-like object
        filepath to write the data to, or file-like object (defaults to stdout)

    output : str
        output format (json, csv, txt, default is csv)

    start_date : str (YYYY-MM-DD), optional
        limit to account balance snapshots taken on or after this date

    end_date : str (YYYY-MM-DD), optional
        limit to account balance snapshots taken on or before this date

    latest : bool
        return the latest account balance snapshot

    accounts : list of str, optional
        limit to these accounts

    below : dict of FIELD:AMOUNT, optional
        limit to accounts where the specified field is below the specified
        amount (pass as {field:amount}, for example {'Cushion':0.05})

    fields : list of str, optional
        only return these fields (pass ['?'] or any invalid fieldname to see
        available fields)

    force_refresh : bool
        refresh account balances from IB (default is to query the
        database, which is refreshed every minute)

    Returns
    -------
    None

    Examples
    --------
    Query latest balances. You can use StringIO to load the CSV into pandas.

    >>> f = io.StringIO()
    >>> download_account_balances(f, latest=True)
    >>> balances = pd.read_csv(f, parse_dates=["LastUpdated"])
    """
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if latest:
        params["latest"] = latest
    if accounts:
        params["accounts"] = accounts
    if below:
        params["below"] = dict_to_dict_strs(below)
    if fields:
        params["fields"] = fields
    if force_refresh:
        params["force_refresh"] = force_refresh

    output = output or "csv"

    if output not in ("csv", "json", "txt"):
        raise ValueError("Invalid ouput: {0}".format(output))

    response = houston.get("/account/balances.{0}".format(output), params=params)

    houston.raise_for_status_with_json(response)

    # Don't write a null response to file when using below filters
    if below and response.content[:4] == b"null":
        return

    filepath_or_buffer = filepath_or_buffer or sys.stdout

    write_response_to_filepath_or_buffer(filepath_or_buffer, response)

def _cli_download_account_balances(*args, **kwargs):
    below = kwargs.get("below", None)
    if below:
        kwargs["below"] = dict_strs_to_dict(*below)
    return json_to_cli(download_account_balances, *args, **kwargs)

def download_exchange_rates(filepath_or_buffer=None, output="csv",
                            start_date=None, end_date=None, latest=False,
                            base_currencies=None, quote_currencies=None):
    """
    Query exchange rates for the base currency.

    The exchange rates in the exchange rate database are sourced from the
    European Central Bank's reference rates, which are updated each day at 4 PM
    CET.

    Parameters
    ----------
    filepath_or_buffer : str or file-like object
        filepath to write the data to, or file-like object (defaults to stdout)

    output : str
        output format (json, csv, txt, default is csv)

    start_date : str (YYYY-MM-DD), optional
        limit to exchange rates on or after this date

    end_date : str (YYYY-MM-DD), optional
        limit to exchange rates on or before this date

    latest : bool
        return the latest exchange rates

    base_currencies : list of str, optional
        limit to these base currencies

    quote_currencies : list of str, optional
        limit to these quote currencies

    Returns
    -------
    None

    Examples
    --------
    Query latest exchange rates. You can use StringIO to load the CSV into pandas.

    >>> f = io.StringIO()
    >>> download_exchange_rates(f, latest=True)
    >>> rates = pd.read_csv(f, parse_dates=["Date"])
    """
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if latest:
        params["latest"] = latest
    if base_currencies:
        params["base_currencies"] = base_currencies
    if quote_currencies:
        params["quote_currencies"] = quote_currencies

    output = output or "csv"

    if output not in ("csv", "json", "txt"):
        raise ValueError("Invalid ouput: {0}".format(output))

    response = houston.get("/account/rates.{0}".format(output), params=params)

    houston.raise_for_status_with_json(response)

    filepath_or_buffer = filepath_or_buffer or sys.stdout

    write_response_to_filepath_or_buffer(filepath_or_buffer, response)

def _cli_download_exchange_rates(*args, **kwargs):
    return json_to_cli(download_exchange_rates, *args, **kwargs)
