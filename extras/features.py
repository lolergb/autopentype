conf_features    = {
		#Standar ligature configuration
		'liga' :{
				'name'             : 'liga',
				'expresionRegular' : '._.',
				'nameGroup'        : [],
				'init'             : '# Init standard ligatures',
				'end'              : '# End standard ligatures'
				},
		#Case ligature configuration
		'smcp' :{
				'name'             : 'smcp',
				'expresionRegular' : '.*\.smcp',
				'nameGroup'        : ['lowercase', 'small_caps'],
				'init'             : '# Init smcp ligatures',
				'end'              : '# End smcp ligatures'
				},
		#Case ligature configuration
		'case' :{
				'name'             : 'case',
				'expresionRegular' : '.*\.case',
				'nameGroup'        : ['case', 'case1'],
				'init'             : '# Init case ligatures',
				'end'              : '# End case ligatures'
				},
		}
