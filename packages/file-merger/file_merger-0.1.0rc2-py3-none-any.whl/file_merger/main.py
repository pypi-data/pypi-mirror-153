import os, re

from file_merger.helper import get_args, get_file_name, ask_overwrite, load_config

code_extension_highlight = {
	'c': 'c',
	'cpp': 'cpp',
	'css': 'css',
	'glsl': 'glsl',
	'h': 'cpp',
	'html': 'html',
	'js': 'js',
	'py': 'py',
	'rs': 'rs',
	'svelte': 'svelte',
	'svg': 'xml',
	'yaml': 'yaml',
	'yml': 'yaml',
}

filename_regex = r'/([^\/]+\.[a-zA-Z0-9\-\_]+)'

def merge_files(path, result_name, config):
	result_file = open(result_name, 'a')
	name = ''
	was_error = False

	for file in config['files']:
		if 'text' in file:
			# write some text instead of file
			result_file.write(file['text'] + '\n')
			continue

		# if is code, add back-tics
		file_ext = re.search(r'\.([a-z]+)', file)
		file_ext = file_ext.group(1) if file_ext else ''
		if config['code_in_md'] and file_ext in code_extension_highlight:
			start_tics = '```' + code_extension_highlight[file_ext] + '\n'
			end_tics = '```\n\n'
		else:
			start_tics = ''
			end_tics = ''

		if config['add_file_names']:
			file_name_label = file

			if config['remove_folder']:
				file_name_label = re.search(filename_regex, file)
				file_name_label = file_name_label.group(1) if file_name_label else file

			if config['file_name_as_code']:
				file_name_label = f'`{file_name_label}`'

			file_name_label = config['file_label'] + file_name_label + '\n\n'
		else:
			file_name_label = ''

		if config['code_in_md']:
			name = file_name_label + start_tics

		file_name = get_file_name(os.path.join(path, config['folder']), file, config['extension'])
		try:
			with open(file_name, 'r') as f:
				new_code = f.read()

				# file is empty
				if new_code == '':
					break

				# if file not end with linebreak
				if new_code[-1] != '\n':
					new_code += '\n'
				result_file.write(name + new_code + end_tics)
		except Exception as e:
			print(e, f'\nFile: {file_name}')
			was_error = True

	result_file.close()
	if was_error:
		print('Written with errors')
	else:
		print('Successfully written')

def setup_merge(config, current_path, config_path):
	if config['use'] is False:
		quit('This config file marked as unused')

	if config['empty']:
		open(config['empty'], 'w').close()
		quit('Written empty file')

	if not config['files']:
		quit('No input files specified')

	result_name = get_file_name(config_path, config['output'], config['extension'])

	if not ask_overwrite(result_name, config['ask_overwrite']):
		quit('Exiting')

	merge_files(current_path, result_name, config)

def main():
	args = get_args()

	current_path = args.folder
	if os.path.exists(args.config):
		config_path = args.config
	else:
		config_path = current_path + '/' + args.config

	config = load_config(config_path)

	config_folder = os.path.dirname(config_path)
	setup_merge(config, current_path, config_folder)
