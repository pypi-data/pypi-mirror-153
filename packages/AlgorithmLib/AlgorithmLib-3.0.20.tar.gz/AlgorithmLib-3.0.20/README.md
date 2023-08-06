    Audio test libs to compute audio quality and 3A performance by objective metrics
	pcm,wav inputfiles is allowed,support different samplerate (invalid params are simply corrected to valid ones)

    
   	
	# How to install ?
	
    *******************************************************
	
	#Install with pip:
	
	simply use pip to install this toolkit
	
	"pip install algorithmLib"
	
	********************************************************
		
	# Build and Install with git:
	
	first step:
	
	git clone https://g.hz.netease.com/majianli/audiotestalgorithm
	
	second step:
	
	simply run move2sys.prefix.bat before you building the project
	
	**************************************************************
	
	
	# How to use?
	
        #just see ./demos/ 	
	def compute_audio_quality(metrics,testFile=None,refFile=None,cleFile=None,samplerate=16000,bitwidth=2,channel=1,refOffset=0,testOffset=0,,maxComNLevel =-48.0,speechPauseLevel=-35.0,audioType=0,
                          aecStartPoint=0,aecTargetType=0,aecScenario=0,rmsCalsection=None):
	
		"""
		:param metrics: G160/P563/POLQA/PESQ/STOI/STI/PEAQ/SDR/SII/LOUDNESS,
		# G160 no samplerate limiting,  WAV/PCM input , three inputfiles :clean,ref,test no duration limiting; 
		# P563 8000hz( only 8k spectrum is being calculated), WAV/PCM input , single inputfile, duration < 20s;
		# POLQA nb mode  8k  swb mode 48k :WAV/PCM input , 2 inputfiles: ref,test: duration < 20s;
		# PESQ nb mode 8k   wb mode  16k ,WAV/PCM input ,2 inputfiles: ref,test: duration < 20s;
		# STOI no samplerate limiting; 2 inputfiles: ref,test, no duration limiting;
		# STI >8k(only 8k spectrum is being calculated), WAV/PCM input , 2 inputfiles: ref,test ,duration > 20s;
		# PEAQ no samplerate limiting, WAV/PCM ,2 inputfiles: ref, test , no duration limiting;
		# SDR no samplerate limiting; WAV/PCM input ,2 inputfiles:ref,test: no duration limiting;
        # MATCH no samplerate limiting; WAV/PCM input;3 inputfiles:ref,test,out; no duration limiting;
        # MUSIC no samplerate limiting;WAV/PCM input;2 inputfiles:ref,test;no duration limiting;
        # TRANSIENT no samplerate limiting; WAV/PCM input;3 inputfiles: cle,noise,test; no duration limiting;
		# GAINTABLE , no samplerate limiting; WAV/PCM input;2 inputfiles: ref, test ; specific files;
		# ATTACKRELEASE  no samplerate limiting; WAV/PCM input;2 inputfiles: ref, test ; specific files;
		# MUSICSTA no samplerate limiting; WAV/PCM input;2 inputfiles: ref, test ;  no duration limiting;
        # AGCDELAY no samplerate limiting; WAV/PCM input 2 inputfiles：ref ,test; no duration limiting;
        # MATCHAEC no samplerate limiting; WAV/PCM input;3 inputfiles:ref,mic,test;  no duration limiting;
        # ELRE no samplerate limiting; WAV/PCM input;3 inputfiles:mic,ref,test; no duration limiting;
        # SLIENCE no samplerate limiting; WAV/PCM/MP4 input;1 input file：test; no duration limiting;
        # FORMAT no samplerate limiting; WAV/MP4 input;1 input file：test; no duration limiting;
        # AECMOS no samplerate limiting; WAV/PCM input ;3 inputfiles:mic,ref,test ; no duration limiting;
        # AIMOS no samplerate limiting; WAV/PCM input ;1 input file: test; no duration limiting;
        # TRMS no samplerate limiting; WAV/PCM input ;1 input file:test; no duration limiting;
        # ARMS no samplerate limiting; WAV/PCM input ;1 input file:test; no duration limiting;
        # NOISE no samplerate limiting; WAV/PCM input ;1 input file:ref、test; no duration limiting;
		there are different params for different metrics,if params you speend is valid,they will be corrected to valid ones while calculating
		:param testFile: the files under test ,
		:param refFile: the reference file ,FR metrics need POLQA/PESQ/PEAQ
		:param cleFile: clean file ,G160 need 
        :param noiseFile noise file,option, TRANSIENT NOISE
        :param outFile out file,option, MATCH SIG 
		:param samplerate: samplerate,option ,pcmfile  default = 16000
		:param bitwidth: bitwidth, option,pcmfile  default = 2
		:param channel: channels, option,pcmfile  default = 1
		:param refOffset: offset for ref file,option
		:param testOffset: offset for test file ,option
        :param maxComNLevel: G160
        :param speechPauseLevel G160
        :param audioType  0:speech 1:music MATCH/GAINTABLE
        :param aecStartPoint  AECMOS
        :param aecTargetType  0:Chiness 1:English 2:Single Digit 3:Music  MATCHAEC/ELRE
        :param aecScenario aec mos     0:'doubletalk_with_movement', 1:'doubletalk', 2:'farend_singletalk_with_movement', 3:'farend_singletalk', 4:'nearend_singletalk'
        :param rmsCalsection TRMS/ARMS
		:return
		"""
		
	#  PESQ example
	src = "a.pcm"
	test = "b.pcm"
	
	score = compute_audio_quality('PESQ',testFile=test,refFile=src,samplerate=16000)
	
	
	or
	
	src = "a.wav"
	test = "b.wav"
	
	score = compute_audio_quality('PESQ',testFile=test,refFile=src)
	
	
	#  G160 example
	
	src = "a.wav"
	test = "b.wav"
	cle = "c.wav"
	tnlr,nplr,snri,dsn  = compute_audio_quality("G160",testFile=test,refFile=src,cleFile=cle)
	
	or 
	
	src = "a.pcm"
	test = "b.pcm"
	cle = "c.pcm"
	
	tnlr,nplr,snri,dsn  = compute_audio_quality("G160",testFile=test,refFile=src,cleFile=cle,samplerate=48000)
	
	
	#p563 example
	
	test = "a.wav"
	
	Mos,SpeechLevel,Snr,NoiseLevel = compute_audio_quality('P563',testFile=test)
	
	or 
	
	test = "a.pcm" 
	
	Mos,SpeechLevel,Snr,NoiseLevel = compute_audio_quality('P563',testFile=test,samplerate=32000)