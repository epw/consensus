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

playbooks = {}

def get_data():
	startnum = None
	endnum = None
	with io.open ('consensus.md', encoding='utf-8') as f:
		l=0
		workingdoc = []
		global playbookstext
		for line in f:
			l += 1
			workingdoc.append(line)
			if line.startswith('# The Characters (Appendix A)'):
				start = workingdoc[l-1]
				startnum = l-1
		end = workingdoc[l-1]
		endnum = l

	playbookstext = workingdoc[startnum:endnum]
	f.closed

class Playbook:
	def __init__(self):
		self.name = ''
		self.description = ''
		self.names = ''
		self.question1 = ''
		self.question2 = ''
		self.question3 = ''
		self.presentation = ''
		self.eyes = ''
		self.faces = ''
		self.bodies = ''
		self.clothes = ''
		self.auras = ''
		self.paradigms = []
		self.moves = []
		self.specialmove = ''
		self.stats = 'Arrange +2, +1, +0, +0, -1'
		self.anchors = {'home':[], 'connection':[], 'memories':[]}
		self.gear = []
		self.special = {}
		self.place_of_power = {}
		self.advancements = {'basic':[], 'special':[]}
		
		
	def add_paradigm(self):
		self.paradigms.append({'name':'','aligned':'', 'opp1':'', 'opp2':''})
	def add_move(self):
		self.moves.append({'name':'','before':'', 'trigger':'', 'after':'', 'movestring':'', 'isdefault':False})

def playbookdata(name):
	n=0
	z=0
	in_gear = False
	in_special = False
	in_advancements = False
	in_looks = False
	in_paradigms = False
	in_moves = False
	in_anchors = False
	in_description = False
	gear = []
	looks = []
	paradigm = []
	moves = []
	anchors = []
	special = []
	advancements = []
	def checkspecial(line):
		if 'Paradigms' in line:
			return False
		elif 'Moves' in line:
			return False
		elif 'Stats' in line:
			return False
		elif 'Anchors' in line:
			return False
		elif 'Starting Gear' in line:
			return False
		elif 'Advancements' in line:
			return False
		else:
			return True
	for line in playbookstext:
		n+=1
		if line.startswith('## ' + name[0]):
			startnum = n-1
			in_description = True
		if line.startswith('## ' + name[1]):
			endnum = n-1
			break
	endnum = n-1
	playbooktext = playbookstext[startnum:endnum]
	playbookdescription = ''
	playbook = playbooktext[0][3:][:-1]
	playbooks[playbook] = Playbook()
	p = playbooks[playbook]
	p.name = playbook[4:]
	
	if '_' in p.description:
		p.description = p.description.replace('_', '')
	
	for line in playbooktext:
		z+=1
		if line.startswith('## ' + name[0]):
			in_description = True
		if line.startswith('**Name:**'):
			in_description = False
			p.names = line[:-1]
		if in_description:
			if not line.startswith('## ' + name[0]):
				if not line == '\n':              
					playbookdescription = playbookdescription + line
					p.description = playbookdescription
					if '_' in p.description:
						p.description = p.description.replace('_', '')
		if line.startswith('**Why was your humanity trivialized?**'):
			p.question1 = line[39:].strip(' \n')
		if line.startswith('**Why is your humanity still in question?**'):
			p.question2 = line[44:].strip(' \n')
		if line.startswith('**Why are you hunted?**'):
			p.question3 = line[24:].strip(' \n')
		if line.startswith('**Looks:**'):
			in_looks = True
		if line.startswith('### '):
			in_looks = False
		if in_looks:
			looks.append(line)
		if line.startswith('### Paradigms'):
			in_paradigms = True
		if line.startswith('### ') and not line.startswith('### Paradigms'):
			in_paradigms = False
		if in_paradigms:
			paradigm.append(line)
		if line.startswith('### Moves'):
			in_moves = True
		if line.startswith('### ') and not line.startswith('### Moves'):
			in_moves = False
		if in_moves:
			moves.append(line)
		if line.startswith('### Anchors'):
			in_anchors = True
		if line.startswith('### ') and not line.startswith('### Anchors'):
			in_anchors = False
		if in_anchors:
			anchors.append(line)
		if line.startswith('### Starting Gear'):
			in_gear = True
		if line.startswith('###') and not line.startswith('### Starting Gear'):
			in_gear = False
		if in_gear:
			gear.append(line)
		if line.startswith('### ') and checkspecial(line):
			in_special = True
		if line.startswith('### Advancements'):
			in_special = False
			in_advancements = True
		if in_special:
			special.append(line)
		if in_advancements:
			advancements.append(line)
		
	for line in looks:
		if 'presentation' in line:
			p.presentation = line.strip(' -\n')
		if 'eyes' in line:
			p.eyes = line.strip(' -\n')
		if 'face' in line:
			p.faces = line.strip(' -\n')
		if 'body' in line:
			p.bodies = line.strip(' -\n')
		if 'clothes' in line:
			p.clothes = line.strip(' -\n')
		if 'aura' in line:
			p.auras = line.strip(' -\n')
			
	num_of_paradigms = -1	
	for line in paradigm[1:]:
		if line.startswith('####'):
			num_of_paradigms += 1
			p.add_paradigm()
			p.paradigms[num_of_paradigms]['name'] = line[5:-1]
			if '_' in p.paradigms[num_of_paradigms]['name']:
				linelist = p.paradigms[num_of_paradigms]['name'].split('_')
				p.paradigms[num_of_paradigms]['name'] = linelist[0] + '\\textit{' + linelist[1] + '}' + linelist[2]
		elif line.startswith('**Aligned'):
			if '(choose one)' in line:
				p.paradigms[num_of_paradigms]['aligned'] = line[26:-1]
			else:
				p.paradigms[num_of_paradigms]['aligned'] = line[13:-1]				
		elif line.startswith('**Opposed'):
			p.paradigms[num_of_paradigms]['opp1'] = line[13:-1]
		elif not line == '\n':
			p.paradigms[num_of_paradigms]['opp2'] = line[:-1]		
	in_move = False
	in_move_list = False
	moveslist = []
	move_number = -1
	move_list_number = 0
	for line in moves:
		if line.startswith('**'):
			move_number += 1
			moveslist.append([])
			in_move = True

		if line == '\n':
			in_move = False
		
		if line.startswith('- '):
			in_move = True

		if in_move:
			moveslist[move_number].append(line)

				
		if line.startswith('When you and another character **exchange a moment of humanity**'):
			p.specialmove = line[66:-1]

	num_of_moves = -1
	for move in moveslist:
		num_of_moves += 1
		p.add_move()
		if len(move) == 1:
			movedict = p.moves[num_of_moves]
			movedict['name'] = move[0].split(':**')[0][2:]
			list = move[0].split('**')
			if len(list) > 3:
				movedict['before'] = list[2]
				movedict['after'] = list[4][:-1]
				trigger =list[3]
				movedict['trigger'] = trigger
			else:
				movedict['trigger'] = ''
				movedict['movestring'] = list[2][:-1]
			
			if list[2].startswith(' (You have this move by default)'):
				movedict['isdefault'] = True
				movedict['movestring'] = movedict['movestring'][33:]
				movedict['before'] = movedict['before'][33:]
			else:
				movedict['isdefault'] = False
				movedict['movestring'] = movedict['movestring'][1:]
				movedict['before'] = movedict['before'][1:]
		else:
			movedict = p.moves[num_of_moves]
			movedict['name'] = move[0].split(':**')[0][2:]
			movedict['list'] = move[1:]
			x=0
			for item in movedict['list']:
				movedict['list'][x] = item[2:-1] 
				x+=1
			list = move[0].split('**')
			if len(list) > 3:
				movedict['before'] = list[2]
				movedict['after'] = list[4][:-1]
				trigger =list[3]
				movedict['trigger'] = trigger
			else:
				movedict['trigger'] = ''
				movedict['movestring'] = list[2][:-1]
			
			if list[2].startswith(' (You have this move by default)'):
				movedict['isdefault'] = True
				movedict['movestring'] = movedict['movestring'][33:]
				movedict['before'] = movedict['before'][33:]
			else:
				movedict['isdefault'] = False
				movedict['movestring'] = movedict['movestring'][1:]
				movedict['before'] = movedict['before'][1:]
	
	for line in anchors:
		if '______' in line:
			line = line.replace('______', '\BLANK')
		if 'My **Shelter Anchor** is:' in line:
			p.anchors['home'] = line[103:][:-1].split(';')
		if 'My **Connection Anchor** is:' in line:
			p.anchors['connection'] = line[113:][:-1].split(';')
		if 'My **Emotional Anchor** is:' in line:
			p.anchors['memories'] = line[103:][:-1].split(';')
			

	for line in gear[1:]:
		if not line == '\n':
			p.gear.append(line[2:])
			
	in_basic = True
	in_advanced = False
	advanced = []
	for line in advancements[2:]:
		if line.startswith('- Remove a Restriction from your Paradigm'):
			in_basic = False
		if in_basic:
			p.advancements['basic'].append(line[2:][:-1])
		if line.startswith('- (*) Remove a Restriction from your Paradigm'):
			in_advanced = True
		if line == '\n':
			in_advanced = False
		if in_advanced:
			advanced.append(line[2:][:-1])
	p.advancements['special'] = advanced[1:]
	
	in_pop = False
	in_other = False
	pop = []
	other = []
	for line in special:
		if line.startswith('### Place of Power'):
			in_pop = True
			in_other = False
		if line.startswith('### ') and not line.startswith('### Place of Power'):
			in_pop = False
			in_other = True
		if in_pop:
			pop.append(line)
		if in_other:
			other.append(line)
	popdict = {}
	in_fac = False
	in_rit = False
	p.place_of_power['First, pick a facade:'] = []
	p.place_of_power['Then pick up to 1 Strength:'] = []
	p.place_of_power['Pick at least 1 Weakness:'] = []
	p.place_of_power['A Ritual performed here will never (choose 1):'] = []
	for line in pop:
		if line.startswith('First, pick a facade:'):
			in_fac = True
		if line.startswith('Then pick'):
			in_fac = False
		if in_fac:
			if line.startswith('-'):
				p.place_of_power['First, pick a facade:'].append(line[2:][:-1])
		if line.startswith('Then pick up to 1 Strength'):
			p.place_of_power['Then pick up to 1 Strength:'] = (line.split('+')[1:])
		if line.startswith('Pick at least 1 Weakness:'):
			p.place_of_power['Pick at least 1 Weakness:'] = (line.split('+')[1:])
		if line.startswith('A Ritual performed here will never (choose 1):'):
			in_rit = True
		if in_rit:
			if line.startswith('-'):
				p.place_of_power['A Ritual performed here will never (choose 1):'].append(line[2:][:-1])

	other_number = -1
	blocklist = []
	in_block = False
	in_list = False	
	for line in other:
		if line.startswith('### '):
			p.special['name'] = line[4:][:-1] + ":"
		if not line == '\n':
			other_number += 1
			blocklist.append('')
			in_block = True
		if line == '\n':
			in_block = False

			
		if in_block:
			blocklist[other_number] = blocklist[other_number] + line
	

		
	p.special['blocks'] = blocklist		
		
if __name__ == "__main__":
	get_data()
	playbooknames = ['The Cabalist', 'The Hedge Mage', 'The Inspired', 'The Mentor', 'The Pious', 'The Primordial', 'The Tech Adept', 'The Voiced', 'The Wayfarer', '___']
	iterations = 0

	runs = -1
	for pb in playbooknames:
		runs += 1
		if len(sys.argv) == 1:
			print ("No Args")
			break
		input = sys.argv[1]
		input = input.strip('.tex')
		converted = pb.lower()
		converted = converted.replace(' ', '_')
		if input in converted:
			print ("Arg accepted")
			start =  playbooknames[runs]
			end = playbooknames[runs+1]


			playbookdata([start, end])
			filename = start[4:].replace(' ', '_')
			filename = filename.lower()
			template = latex_jinja_env.get_template(filename + '-template.tex')
			playbook = playbooks[start]
			defaultmove = []
			othermoves = []
			for move in playbook.moves:
				if move['isdefault']: 
					defaultmove.append(move)
				else:	
					othermoves.append(move)

			output = template.render(name = playbook.name, description= playbook.description, names = playbook.names[10:], question1 = playbook.question1, question2 = playbook.question2, question3 = playbook.question3, eyes = playbook.eyes, faces = playbook.faces, clothes = playbook.clothes, presentation = playbook.presentation, bodies = playbook.bodies, auras = playbook.auras, homeanchors = playbook.anchors['home'], connectionanchors = playbook.anchors['connection'], memoryanchors = playbook.anchors['memories'], gear = playbook.gear, basicadvancements = playbook.advancements['basic'], specialadvancements = playbook.advancements['special'],	defaultmove = defaultmove, othermoves = othermoves, specialmove = playbook.specialmove, paradigms = playbook.paradigms, special = playbook.special, place_of_power = playbook.place_of_power)
			with io.open(filename + '.tex', 'w+', encoding='utf-8') as f:
				f.write(output)	

	"""
	for i in range(len(playbooknames)-1):
	
		playbookdata([playbooknames[i], playbooknames[i+1]])

		template = latex_jinja_env.get_template(playbooknames[i] + '-template.tex')
		playbook = playbooks[playbooknames[i]]
		defaultmove = []
		othermoves = []
		for move in playbook.moves:
			if move['isdefault']: 
				defaultmove.append(move)
			else:
				othermoves.append(move)
		filename = playbooknames[i][4:].replace(' ', '_')
		filename = filename.lower()
		output = template.render(name = playbook.name, description= playbook.description, names = playbook.names[10:], question1 = playbook.question1, question2 = playbook.question2, question3 = playbook.question3, eyes = playbook.eyes, faces = playbook.faces, clothes = playbook.clothes, presentation = playbook.presentation, bodies = playbook.bodies, auras = playbook.auras, homeanchors = playbook.anchors['home'], connectionanchors = playbook.anchors['connection'], memoryanchors = playbook.anchors['memories'], gear = playbook.gear, basicadvancements = playbook.advancements['basic'], specialadvancements = playbook.advancements['special'],	defaultmove = defaultmove, othermoves = othermoves, specialmove = playbook.specialmove, paradigms = playbook.paradigms, special = playbook.special, place_of_power = playbook.place_of_power)
		with io.open(filename + '.tex', 'w+', encoding='utf-8') as f:
			f.write(output)	
	"""
