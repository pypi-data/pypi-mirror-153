"""
Copyright (c) 2022 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from datetime import datetime
import os
import logging
import json
logger=logging.getLogger('adamapi')

from . import AdamApiError

class Search():
    def __init__(self,client):
        self.LOG=logger
        self.client=client

    def getProducts(self,datasetId,startIndex=0,maxRecords=10,**kwargs):
        """
        Product Catalogue Search
        @ datasetId, the dataseId ,required
        @ startDate, search start date (%Y-%m-%d)
        @ endDate, search end date (%Y-%m-%d)
        @ maxRecords, number of result showed
        @ startIndex, index of the first result to start showin
        """
        params={}
        url=os.path.join( 'apis','v2','opensearch',datasetId.split(":",1)[0],'records')

        params['datasetId']=datasetId.split(":",1)[1]
        params["client"]="adamapi"

        for par in kwargs:
            if par == 'geometry':
                if type(kwargs[par]) is str:
                    params[par] = kwargs[par]
                elif type(kwargs[par]) is dict:
                    params[par] = json.dumps(kwargs[par])
            elif par == 'startDate' and isinstance( kwargs[par], datetime ):
                params[ 'startDate' ] = kwargs[par].strftime( '%Y-%m-%dT%H:%M:%SZ' )
            elif par == 'endDate' and isinstance( kwargs[par], datetime ):
                params[ 'endDate' ] = kwargs[par].strftime( '%Y-%m-%dT%H:%M:%SZ' )
            else:
                params[par]=kwargs[par]

        params["page"]=startIndex
        params["items"]=maxRecords

        if 'geometry' in kwargs:
            self.LOG.info(params)
            response=self.client.client(url,params,"POST").json()
        else:
            response=self.client.client(url,params,"GET").json()
        if 'errors' in response:
            raise AdamApiError(response['errors'])
        else:
            return response
