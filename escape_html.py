import cgi
def escape_html(s):
	return cgi.escape(s, quote = True)

print escape_html('"hello, & = &amp;"')