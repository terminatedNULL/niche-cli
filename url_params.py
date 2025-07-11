import sys, json, argparse

"""
A tool for extracting, formatting, and displaying the parameters or a URL.
Parameters can be sorted alphanumerically, along with filtering for empty
parameters.
"""

def main():
	parser = argparse.ArgumentParser(prog='URL Parameter Extractor', description='Breaks a url into its components, arranged visually')
	parser.add_argument('url')

	sort_group = parser.add_mutually_exclusive_group()
	sort_group.add_argument('-a', '--ascending', action='store_true', dest='ascending')
	sort_group.add_argument('-d', '--descending', action='store_true', dest='descending')

	empty_group = parser.add_mutually_exclusive_group()
	empty_group.add_argument('-ne', '--no-empty', action='store_true', dest='no_empty')
	empty_group.add_argument('-e', '--empty', action='store_true', dest='empty')

	args = parser.parse_args()

	url = sys.argv[1]
	base = url[:(url.index('?') + 1)]
	tail = url[(url.index('?') + 1):]

	domain_start = url.index('//') + 2
	domain = base[domain_start:base.index('/', domain_start)]
	path = base[(base.index('/', domain_start)):-1]

	params = tail.split('&')
	params = { p[:p.index('=')]: p[(p.index('=') + 1):] for p in params }

	if args.ascending:
		params = dict(sorted(params.items()))

	if args.descending:
		params = dict(sorted(params.items(), reverse=True))

	if args.no_empty:
		params = { k: v for k, v in params.items() if v is not None and v != '' }

	empty = False
	if args.empty:
		empty = True
		params = { k: '' for k, v in params.items() if v is None or v == '' }

	print(f'\nDomain\n ▪ {domain}\n')
	print(f'Path\n ▪ {path}\n')

	print('Parameters:')
	if len(params) > 0:
		max_key_len = max(len(key) for key in params.keys())
		line_char = True
		for key, val in params.items():
			if not empty:
				print(f' ▪ {(key + ' ').ljust(max_key_len + 3, '─' if line_char else '═')}{'┤' if line_char else '╣'} {val}')
				line_char = not line_char
			else:
				print(f' ▪ {key}')
	else:
		print(' ▪ None')


if __name__ == '__main__':
	main()
