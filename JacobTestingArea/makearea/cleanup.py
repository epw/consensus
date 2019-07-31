import os
list = ['cabalist', 'guru', 'hedge_mage', 'inspired', 'mentor', 'pious', 'primordial', 'tech_adept', 'voiced', 'wayfarer']
for name in list:
	if os.path.exists(name + '.tex'):
		os.remove(name + '.tex')
	if os.path.exists(name + '.pdf'):
		os.remove(name + '.pdf')
	if os.path.exists(name + '.log'):
		os.remove(name + '.log')
	if os.path.exists(name + '.aux'):
		os.remove(name + '.aux')