from annoying.decorators import render_to
import httplib2
import urllib
from django.conf import settings
import re
@render_to('index.html')
def home(request):
    h = httplib2.Http(".cache")
    resp, content = h.request(settings.WARPED_URL, "GET")
    realcontent = []
    regex = re.compile(r'<tr class="event-row(.*?)</tr>', re.IGNORECASE)
    
    for m in regex.finditer(content):
        if m:
            match = re.search(r'<td class="location"><a.*?>(.*?)</a>(.*?)<.*?>(.*?)<',str(m.group(0)), re.DOTALL)
            if match:
                realcontent.append(str(match.group(3)))
             
    stuff = []   
    for entry in realcontent:
        stuff.append({ 'text': entry, 'link':'http://www.wunderground.com/cgi-bin/findweather/hdfForecast?query='+urllib.quote(entry)} )
    
    return {'content':stuff[::-1]}
