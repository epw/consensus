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
		global mctext
		for line in f:
			l += 1
			workingdoc.append(line)
			if line.startswith('# The Master of Ceremonies'):
				start = workingdoc[l-1]
				startnum = l-1
			if line.startswith('# Stacking Moves'):
				end = workingdoc[l-1]
				endnum = l
				break


	mctext = workingdoc[startnum:endnum]
	f.closed
	
def mc_data():
	in_agenda = False
	in_always_say = False
	in_principles = False
	in_moves = False
	in_soft = False
	in_med = False
	in_hard = False
	in_start_session = False
	in_scene_types = False
	
	agenda = []
	always_say = []
	principles = []
	softmoves = []
	medmoves = []
	hardmoves = []
	start_session = []
	scene_types = []
	
	for line in mctext:
		if line.startswith('## Agenda'):
			in_agenda = True
			
		if line.startswith('## Always Say'):
			in_agenda = False
			in_always_say = True
		
		if in_agenda:
			if line.startswith('**'):
				agenda.append(line.strip(' *\n'))

		if line.startswith('## The Principles'):
			in_principles = True
			in_always_say = False
			
		if in_always_say:
			if line.startswith('**'):
				always_say.append(line.strip(' *\n'))
		
		if line.startswith('## Your Moves'):
			in_principles = False
			in_moves = True
		
		if in_principles:
			if line.startswith('**'):
				principles.append(line.strip(' *\n'))
			
		if line.startswith('## Running a Session'):
			in_moves = False
		
		if in_moves:
			if line.startswith('### Softer Moves'):
				in_soft = True
			if line.startswith('### Soft or Hard Moves'):
				in_soft = False
				in_med = True
			if line.startswith('### Harder Moves'):
				in_med = False
				in_hard = True
			if in_soft:
				if line.startswith('**'):
					softmoves.append(line.strip(' *\n'))
			if in_med:
				if line.startswith('**'):
					medmoves.append(line.strip(' *\n'))
			if in_hard:
				if line.startswith('**'):
					hardmoves.append(line.strip(' *\n'))
					
		if line.startswith('### Starting a Session'):
			in_start_session = True
			
		if line.startswith('### Scene Framing'):
			in_start_session = False
			in_scene_types = True
		
		if in_start_session:
			if line.startswith('#### '):
				start_session.append(line.strip(' #\n'))
		
		if line.startswith('### Ending a Session'):
			in_scene_types = False
			
		if in_scene_types:
			if line.startswith('#### '):
				scene_types.append(line.strip(' #\n'))
				
	
	softmoves.reverse()
	medmoves.reverse()
	hardmoves.reverse()
	agendanum = -1
	for item in agenda[:-1]:
		agendanum+=1
		agenda[agendanum] = item + ' \TEXTBULLET'
	
	always_say_num = -1
	for items in always_say[:-1]:
		always_say_num+=1
		always_say[always_say_num] = item + ' \TEXTBULLET'
	
	principlesnum = -1
	for item in principles:
		principlesnum+=1
		if item.startswith("Don"):
			principles[principlesnum] = '{\large\\bf ' + item + '}'
			
	
	output = {'agenda':agenda, 'always_say':always_say, 'principles':principles, 'hardmoves':hardmoves, 'medmoves':medmoves, 'softmoves':softmoves, 'start_session':start_session, 'scene_types':scene_types}
	return output

		
		
if __name__ == "__main__":
	get_data()
	data = mc_data()
	template = latex_jinja_env.get_template('mcsheet-template.tex')
	output = template.render(agenda = data['agenda'], always_say = data['always_say'], principles = data['principles'], hardmoves = data['hardmoves'], medmoves = data['medmoves'], softmoves = data['softmoves'], start_session = data['start_session'], scene_types = data['scene_types'])
	with io.open('mcsheet.tex', 'w+', encoding='utf-8') as f:
		f.write(output)	

