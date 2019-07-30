
def get_data():
	with open ('Consensus Book.md') as f:
		l=0
		workingdoc = []
		global playbooks
		for line in f:
			l += 1
			workingdoc.append(line)
			if '# The Characters' in line :
				start = workingdoc[l-1]
				startnum = l-1
			if '# The Moves' in line:
				end = workingdoc[l-1]
				endnum = l-1


	playbooks = workingdoc[startnum:endnum]
	f.closed

def playbook(name):
	n=0
	z=0
	for line in playbooks:
		n+=1
		if '## ' +name[0] in line:
			startnum = n-1
		if '## ' + name[1] in line:
			endnum = n-1
			
	playbook = playbooks[startnum:endnum]
	playbookdescription = playbook[2]
	playbookname = playbook[0][3:]


	for line in playbook:
		z+=1
		if '**Name:**' in line:
			playbooknames = line
		if '**Why was your humanity trivialized?**' in line:
			playbookq1 = line
		if '**Why is your humanity still in question?**' in line:
			playbookq2 = line
		if '**Why are you hunted?**' in line:
			playbookq3 = line
		if '**Looks:**' in line:
			print z
			startlooks = z
		if '### Paradigms' in line:
			print z
			endlooks = z-1
			startparadigm = z-1
		if '### Moves' in line:
			endparadigm = z-1
			startmoves = z-1
	
	looks = playbook[startlooks:endlooks]
	paradigm = playbook[startparadigm:endparadigm]
	for line in looks:
		if 'presentation' in line:
			playbookpresentation = line[2:]
		if 'eyes' in line:
			playbookeyes = line[2:]
		if 'face' in line:
			playbookface = line[2:]
		if 'body' in line:
			playbookbody = line[2:]
		if 'clothes' in line:
			playbookclothest = line[2:]
		if 'aura' in line:
			playbookaura = line[2:]
			

	
			
			
		
		
if __name__ == "__main__":
	get_data()
	playbook(['The Cabalist', 'The Mentor'])