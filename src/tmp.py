import pycurl
import certifi
from io import BytesIO

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://zccagau.zendesk.com/api/v2/tickets/show_many.json?ids=1,2,3')
c.setopt(c.WRITEDATA, buffer)
c.setopt(pycurl.USERPWD, '%s:%s' %('ksilvergold18@gmail.com', 'Tmp123'))
c.setopt(c.CAINFO, certifi.where())
c.perform()
c.close()

body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
print(body.decode('iso-8859-1'))