#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:31:38 2017

@author: christopher
"""

import sys
sys.path.append("fitbitlib/")

# import keys
# import fitbit
# import pandas as pd
import keys
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

authd_client = auth2_client