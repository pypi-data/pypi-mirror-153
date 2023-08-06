"""
Copyright (c) 2020 MEEO s.r.l.

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


class AdamApiError( Exception ):
    """Base class for exceptions on the adamapi module."""
    pass

class AdamApiMessage( Exception ):
    """Base class for adamapi mesage"""
    def __init__(self,json):
        self.pk=json["id"] if "id" in json else ""
        self.status=json["status"] if "status" in json else ""
        self.location = json["location"] if "location" in json else ""
        self.error = json["error"] if "error" in json else ""
        self.list = json["tasks"] if "tasks" in json else ""


from . import authorization
from . import datasets
from . import get_data
from . import search

Auth = authorization.Auth
Datasets = datasets.Datasets
GetData = get_data.GetData
Search = search.Search
