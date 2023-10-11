import os
import re


before = 0
after = 1
Min = 0
Max = 1

class Paint (object):
	
	def __init__( self ):
		self.DesignVariables = [] 
		self.Limits = []
		
	def addDesignVariable( self, designVariable ):
		self.DesignVariables.append( designVariable )
		
	def addLimit( self, Limit ):
		self.Limits.append( Limit )
		
	def setObjective( self, objective ):
		self.Objective = objective
	
	def setExecute( self, execute ):
		self.execute = execute	

	def bestPoint( self, DVs ):				
		for DV in DVs:
			if( len ( DVs ) > 1 ):
				for count in range( 0, DV.numSteps ): 
					DV.value = DV.minVal + ( DV.maxVal - DV.minVal )*count/( DV.numSteps - 1 )
					temp =  DVs.copy()
					temp.pop( 0 )
					self.bestPoint( temp )
			else:
				for count1 in range( 0, DV.numSteps ):
					DV.value = DV.minVal + ( DV.maxVal - DV.minVal )*count1/( DV.numSteps - 1 )
					self.run()
					if ( self.Objective.MinOrMax == Min and self.Objective.value < self.Objective.best and self.DesignPass ):
						self.Objective.best = self.Objective.value
						for DVtemp in self.DesignVariables:
							DVtemp.best = DVtemp.value
			

	
	def run( self ):
		for DV in self.DesignVariables:
			DV.write()
			
		os.system( self.execute )
		
		self.Objective.get()	
		
		self.DesignPass = True
		for L in self.Limits:
			L.check()
			if L.good == False:
				self.DesignPass = False
			
			
	def optimize( self ):
		self.bestPoint( self.DesignVariables )
			
		for DV in self.DesignVariables:
			DV.value = DV.best
		self.run()

class DesignVariable:
	def __init__( self, templateFile, inputFile, tag, initialValue, minVal, maxVal, numSteps ):
		self.templateFile = templateFile
		self.inputFile = inputFile
		self.tag = tag
		self.initialValue = initialValue
		self.value = initialValue
		self.minVal = minVal
		self.maxVal = maxVal
		self.numSteps = numSteps
		self.best = 0
	
		
	def write( self ):
		with open( self.templateFile, "rt" ) as fin:
			with open( "temp", "wt") as fout:
				for line in fin:
					fout.write(line.replace( self.tag, str( self.value )))
				fin.close()
		os.system( "move temp "+ self.inputFile )
	
class Objective:
	def __init__( self, outputFile, tag, beforeOrAfter, MinOrMax ):
		self.outputFile = outputFile
		self.tag = tag
		self.beforeOrAfter = beforeOrAfter
		self.value=0.;
		self.MinOrMax = MinOrMax
		if self.MinOrMax == Max:
			self.best = -9e9
		else:
			self.best = 9e9
	
	def get( self ):
		with open( self.outputFile, "rt" ) as fin:
			for line in fin:
				location = line.find( self.tag )
				if location>=0:
					if ( self.beforeOrAfter == after ):
						line =  line[location:]
						numbers = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
						self.value = float( numbers[0] )
					if( self.beforeOrAfter == before ):
						line = line[:location]
						numbers = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
						self.value = float( numbers[-1] )				

class Limit:
	def __init__( self, outputFile, tag, beforeOrAfter, limit, MinOrMax ):
		self.outputFile = outputFile
		self.tag = tag
		self.beforeOrAfter = beforeOrAfter
		self.value = 0.
		self.limit = limit
		self.MinOrMax = MinOrMax
		self.good = False
	
	def check( self ):
		with open( self.outputFile, "rt" ) as fin:
			for line in fin: 
				location = line.find( self.tag )
				if location>=0:
					if ( self.beforeOrAfter == after ):
						line =  line[location:]
						numbers = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
						self.value = float( numbers[0] )
					if( self.beforeOrAfter == before ):
						line = line[:location]
						numbers = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
						self.value = float( numbers[-1] )
						
		if ( self.MinOrMax == Min and self.value >= self.limit ):
			self.good = True
		else:
			self.good = False
			
		if ( self.MinOrMax == Max and self.value <= self.limit ):
			self.good = True
		else:
			self.good = False
