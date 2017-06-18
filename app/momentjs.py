from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        '''Wrapping the string in a Markup object tells jinja2 that the string 
        should not be escaped.
        '''
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % \
                      (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))
                
    def format(self, fmt):
        '''Set the format of moment object.'''
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")