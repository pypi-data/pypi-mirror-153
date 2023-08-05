import click

class Streams:

	def __init__(self, **kwargs):
		pass

	def read_stdin(self, ctx, param, value):
	    if not value and not click.get_text_stream('stdin').isatty():
	        return click.get_text_stream('stdin').read().strip()
	    else:
	        return value