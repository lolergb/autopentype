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
		# Subscript
		'subs' :{
				'name'             : 'subs',
				'expresionRegular' : '.*\.subs',
				'nameGroup'        : ['subs1', 'subs2'],
				'init'             : '# Init subs',
				'end'              : '# End subs'
				},
		# Subscript
		'sups' :{
				'name'             : 'sups',
				'expresionRegular' : '.*\.sups',
				'nameGroup'        : ['sups1', 'sups2'],
				'init'             : '# Init sups',
				'end'              : '# End sups'
				},
		# Scientific Inferiors
		'sinf' :{
				'name'             : 'sinf',
				'expresionRegular' : '.*\.subs',
				'nameGroup'        : ['subs1', 'subs2'],
				'init'             : '# Init Scientific Inferiors',
				'end'              : '# End Scientific Inferiors'
				},
		# Scientific Inferiors
		'numr' :{
				'name'             : 'numr',
				'expresionRegular' : '.*\.numr',
				'nameGroup'        : ['subs1', 'numr1'],
				'init'             : '# Init Numerators',
				'end'              : '# End Numerators'
				},
		}
