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
	lstrip_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('templates'))
)

movesthing = []

def get_data():
	with io.open ('Consensus Book.md', encoding='utf-8') as f:
		l=0
		workingdoc = []
		global movestext
		for line in f:
			l += 1
			workingdoc.append(line)
			if line.startswith('# The Moves'):
				start = workingdoc[l-1]
				startnum = l-1
			if line.startswith('# The Master of Ceremonies'):
				end = workingdoc[l-1]
				endnum = l
				break


	movestext = workingdoc[startnum:endnum]
	f.closed
moves = {}	
class Move:

	def __init__(self):
		self.name = ''
		self.fulltext = ''
		self.is_basic = False
		self.is_advanced = False
		self.trigger = ''
		self.before = ''
		self.after = ''
		self.list = []
		self.after_list = ''
		self.description = ''


def movesdata():
	in_basic = False
	in_advanced = False
	in_move = False	basicmoves = []	advancedmoves = []	in_move = False
	in_move_list = False	in_move_description = False
	moveslist = []
	move_number = -1
	move_list_number = 0
	for line in movestext:
		if line.startswith('When') or line.startswith('At the **end of session**'):
			move_number += 1
			moveslist.append([])
			in_move = True

		if line == '\n':
			in_move = False
		
		if line.startswith('- '):
			in_move = True		if line.startswith('>'):			in_move = True		if line.startswith('>\n'):			in_move = False

		if in_move:
			moveslist[move_number].append(line)
	num_of_moves = -1
	for move in moveslist:		movesthing.append({'name':'','before':'', 'trigger':'', 'after':'', 'movestring':'', 'afterlist':'', 'description':'', 'list':[], 'number':'', 'secondlist':[], 'secondafter':''})
		num_of_moves += 1		movesthing[num_of_moves]['number'] = num_of_moves		if move[0].startswith('When you **suffer harm**'):			movedict = movesthing[num_of_moves]
			movedict['name'] = move[0].split('**')[1]
			movedict['trigger'] = move[0].split('**')[1]
			movedict['before'] = move[0].split('**')[0]
			movedict['after'] = move[0].split('**')[2]			rest = move[1:]#			print(rest)			in_list = False			listnum = 0			for line in rest:				if line.startswith('>'):					movedict['description'] = movedict['description'] + line			rest = [item for item in rest if not item.startswith('>')]			afters = []			doublelist = [[],[]]			for line in rest:				if line.startswith('-'):					in_list = True				if not line.startswith('-'):					in_list = False					afters.append(line)					listnum+=1				if in_list:					doublelist[listnum].append(line)			movedict['list'] = doublelist[0]			movedict['list'] = [item[2:-1] for item in movedict['list']]			movedict['secondlist'] = doublelist[1]			movedict['secondlist'] = [item[2:-1] for item in movedict['secondlist']]			movedict['afterlist'] = afters[0]			movedict['secondafter'] = afters[1]			movedict['movestring'] = movedict['before'] + movedict['trigger'] + movedict['after'] + str(movedict['list']) + movedict['afterlist'] + str(movedict['secondlist']) + movedict['secondafter']			continue
		if len(move) == 2:
			movedict = movesthing[num_of_moves]
			movedict['name'] = move[0].split('**')[1]
			list = move[0].split('**')
			movedict['before'] = list[0]
			movedict['after'] = list[2]
			trigger =list[1]
			movedict['trigger'] = trigger			
			movedict['movestring'] = movedict['before'] + movedict['trigger'] + movedict['after'] 			for line in move:				if line.startswith('>'):					movedict['description'] = movedict['description'] + line
		else:
			movedict = movesthing[num_of_moves]
			movedict['name'] = move[0].split('**')[1]			movedict['trigger'] = move[0].split('**')[1]			movedict['before'] = move[0].split('**')[0]			movedict['after'] = move[0].split('**')[2]
			movedict['list'] = move[1:]			for line in movedict['list']:				if line.startswith('>'):					movedict['description'] = movedict['description'] + line			movedict['list'] = [item for item in movedict['list'] if not item.startswith('>')]			if not movedict['list'][-1].startswith('-'):
				movedict['afterlist'] = movedict['list'][-1]
				movedict['list'] = movedict['list'][:-1]			for line in movedict['list']:				if not line.startswith('-'):					movedict['after'] = movedict['after'] + line						movedict['list'] = [item for item in movedict['list'] if item.startswith('-')]			movedict['list'] = [line[2:-1] for line in movedict['list']]
			list = move[0].split('**')
			movedict['movestring'] = movedict['before'] + movedict['trigger'] + movedict['after'] + str(movedict['list']) + movedict['afterlist']	output = {'assert':{}, 'impress':{}, 'sleeper':{}, 'help':{}, 'sell':{}, 'outfox':{}, 'head down':{}, 'rending':{}, 'aligned':{}, 'change':{}, 'backlash':{},		'willpower':{}, 'fix':{}, 'suffer harm':{}, 'plan':{}, 'begin':{}, 'lose':{}, 'end of session':{}, 'code n':{}, 'danger':{}, 'beyond':{}}	for key in output.keys():				for x in movesthing:			if key in x['name'].lower():				output.update({key:x})	return outputif __name__ == "__main__":
	get_data()	dict = movesdata()	if sys.argv[1] == 'basic':		template = latex_jinja_env.get_template('basicmoves-template.tex')		output = template.render(Assert = dict['assert'], impress = dict['impress'], sleeper = dict['sleeper'], help = dict['help'], sell = dict['sell'], outfox = dict['outfox'], headdown = dict['head down'], rending = dict['rending'], aligned = dict['aligned'], suddenchange = dict['change'], backlash = dict['backlash'])		with io.open('basicmoves.tex', 'w+', encoding='utf-8') as f:
			f.write(output)		if sys.argv[1] == 'extended':		template = latex_jinja_env.get_template('extendedmoves-template.tex')		output = template.render(willpower = dict['willpower'], coden = dict['code n'], fix = dict['fix'], sufferharm = dict['suffer harm'], plan = dict['plan'], begin = dict['begin'], anchor = dict['lose'], eos = dict['end of session'], danger = dict['danger'], quint = dict['beyond'])		with io.open('extendedmoves.tex', 'w+', encoding='utf-8') as f:
			f.write(output)	
		
		