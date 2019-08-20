import jinja2
import os
import sys
from jinja2 import Template
import io
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	lstrip_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('templates'))
)

def get_data():
	with io.open ('consensus.md', encoding='utf-8') as f:
		l=0
		workingdoc = []
		global forcestext
		for line in f:
			l += 1
			workingdoc.append(line)
			if line.startswith('## How to Make a Force out of A Stressor'):
				start = workingdoc[l-1]
				startnum = l-1
			if line.startswith('## Special Forces'):
				end = workingdoc[l-1]
				endnum = l
				break


	forcestext = workingdoc[startnum:endnum]
	f.closed
	
def forces_data():
	in_steps = False
	stepcount = -1
	three_captured = False
	typecount = -1
	four_captured = False
	stressorcount = -1

	
	steps = []
	stressors = []
	types = []
	
	for line in forcestext:
		if line.startswith('Step'):
			in_steps = True
			stepcount+=1
			steps.append('')
		if line.startswith('##'):
			in_steps = False
		if in_steps:
			if not line.startswith('Step') and not line == '\n':
				if stepcount == 2:
					if not three_captured:
						steps[stepcount] = line.strip(' \n')
						three_captured = True
					else:
						if not line.startswith('*') and not line == '\n':
							types.append({'name':line.strip(' \n'), 'subtypes':[]}) 
							typecount+=1
						if line.startswith('*'):
							types[typecount]['subtypes'].append(line.strip(' *\n'))
					
				elif stepcount == 3:
					if not four_captured:
						steps[stepcount] = line.strip(' \n')
						four_captured = True
					else:
						if not line == '\n' and not line.startswith('\\'):
							stressors.append({'name':line.strip(' \n'), 'moves':[]})
							stressorcount+=1
						if line.startswith('\\item'):
							listitem = line.strip(' \n')
							listitem = listitem[6:]
							stressors[stressorcount]['moves'].append(listitem)
					
				else:
					steps[stepcount] = line.strip(' \n')			
	
	output = {'steps':steps, 'stressors':stressors, 'types':types}
	return output

		
		
if __name__ == "__main__":
	get_data()
	data = forces_data()
	template = latex_jinja_env.get_template('makingforces-template.tex')
	output = template.render(steps = data['steps'], stressors = data['stressors'], types = data['types'])
	with io.open('makingforces.tex', 'w+', encoding='utf-8') as f:
		f.write(output)	

