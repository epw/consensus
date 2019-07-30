import jinja2
import os
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
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('templates'))
)



playbooks = {}
def get_data():
	with open ('Consensus Book.md') as f:
		l=0
		workingdoc = []
		global playbookstext
		for line in f:
			l += 1
			workingdoc.append(line)
			if line.startswith('# The Characters'):
				start = workingdoc[l-1]
				startnum = l-1
			if line.startswith('# The Moves'):
				end = workingdoc[l-1]
				endnum = l-1
				break


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
		self.moves.append({'name':'', 'trigger':'', 'movestring':'', 'isdefault':False})

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
		if line.startswith('## ' + name[1]):
			endnum = n-1
			break
			
	playbooktext = playbookstext[startnum:endnum]
	playbookdescription = playbooktext[2]
	playbook = playbooktext[0][3:][:-1]
	playbooks[playbook] = Playbook()
	p = playbooks[playbook]
	p.name = playbook
	p.description = playbookdescription
	
	for line in playbooktext:
		z+=1
		if line.startswith('**Name:**'):
			p.names = line
		if line.startswith('**Why was your humanity trivialized?**'):
			p.question1 = line
		if line.startswith('**Why is your humanity still in question?**'):
			p.question2 = line
		if line.startswith('**Why are you hunted?**'):
			p.question3 = line
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
			p.presentation = line[2:]
		if 'eyes' in line:
			p.eyes = line[2:]
		if 'face' in line:
			p.face = line[2:]
		if 'body' in line:
			p.body = line[2:]
		if 'clothes' in line:
			p.clothes = line[2:]
		if 'aura' in line:
			p.aura = line[2:]
			
	num_of_paradigms = -1	
	for line in paradigm[1:]:
		if line.startswith('####'):
			num_of_paradigms += 1
			p.add_paradigm()
			p.paradigms[num_of_paradigms]['name'] = line[3:]
		elif line.startswith('**Aligned'):
			p.paradigms[num_of_paradigms]['aligned'] = line[13:]
		elif line.startswith('**Opposed'):
			p.paradigms[num_of_paradigms]['opp1'] = line[13:]
		elif not line == '\n':
			p.paradigms[num_of_paradigms]['opp2'] = line
			
	in_move = False
	moveslist = []
	move_number = -1
	for line in moves:
		if line.startswith('**'):
			move_number += 1
			moveslist.append('')
			in_move = True
		if line == '\n':
			in_move = False
		if in_move == True:
			moveslist[move_number] = moveslist[move_number] + line
		if line.startswith('When you and another character **exchange a moment of humanity**'):
			p.specialmove = line[66:]
	
	num_of_moves = -1
	for move in moveslist:
		num_of_moves += 1
		p.add_move()
		movedict = p.moves[num_of_moves]
		movedict['name'] = move.split(':**')[0] + ':**'
		list = move.split('**')
		if len(list) > 3:
			before = list[2]
			after = list[4]
			trigger = '**'+list[3]+'**'
			movedict['trigger'] = trigger
			movedict['movestring'] = before+trigger+after
		else:
			movedict['trigger'] = ''
			movedict['movestring'] = list[2]
		
		if list[2].startswith(' (You have this move by default)'):
			movedict['isdefault'] = True
			movedict['movestring'] = movedict['movestring'][33:]
		else:
			movedict['isdefault'] = False
	
	for line in anchors:
		if 'My **Shelter Anchor** is:' in line:
			p.anchors['home'] = line[103:][:-1].split(';')
		if 'My **Connection Anchor** is:' in line:
			p.anchors['connection'] = line[113:][:-1].split(';')
		if 'My **Memories Anchor** is:' in line:
			p.anchors['memories'] = line[103:][:-1].split(';')
			

	for line in gear[1:]:
		if not line == '\n':
			p.gear.append(line[2:])
			
	in_basic = True
	in_advanced = False
	advanced = []
	for line in advancements[2:]:
		if line.startswith('- (*)'):
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
	p.place_of_power['Then pick up to 1 Strength'] = []
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
			p.place_of_power['Then pick up to 1 Strength'].append((line.split('+')[1:])[:-1])
		if line.startswith('Pick at least 1 Weakness:'):
			p.place_of_power['Pick at least 1 Weakness:'].append((line.split('+')[1:])[:-1])
		if line.startswith('A Ritual performed here will never (choose 1):'):
			in_rit = True
		if in_rit:
			if line.startswith('-'):
				p.place_of_power['A Ritual performed here will never (choose 1):'].append(line[2:][:-1])
				
	other_number = -1
	blocklist = []
	in_block = False
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
	playbookdata(['The Pious', 'The Primordial'])
	template = latex_jinja_env.get_template('testpioustemplate.tex')
	playbook = playbooks['The Pious']
	with io.open('The_Pious_Test.tex', 'w+', encoding='utf-8') as f:
		f.write(template.render(name = playbook.name, description= playbook.description))
	