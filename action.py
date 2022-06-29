'''
Authors: Camelot Developers (Edited and Commented by Chien-Chou Wu)
Purpose: Formats a command to be interpreted by the Camelot game engine. Waits for success repsonse before executing other actions
'''

'''
Purpose: Waits for success or fail response from Camelot
Inputs: command that was sent to Camelot
Outputs: True for success, False for failure
'''

succeeded = []

# Send a command to Camelot.
def action(command):
	print('start ' + command, flush = True)

	while(True):
		# return True
		i = input()
		if(i.startswith('succeeded')):
			succeeded.append(i)

		if('succeeded ' + command in succeeded):
			print('find it!')
			succeeded.remove('succeeded ' + command)
			return True
		elif(i == ''):
			print('pass')
			return True
		elif(i.startswith('error')):
			return False
		elif(i.startswith('failed')):
			continue