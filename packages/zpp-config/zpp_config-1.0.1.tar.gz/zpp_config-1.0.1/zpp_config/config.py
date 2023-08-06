####################################################################
#/ Nom du projet: py-zpp_config                                   /#
#/ Nom du fichier: config.py                                      /#
#/ Type de fichier: fichier principal                             /#
#/ Fichier annexe:                                                /#
#/                                                                /#
#/ Auteur: ZephyrOff  (Alexandre Pajak)                           /#
#/ Version: 1.0                                                   /#
#/ Description: Module pour le chargement et la modification      /#
#/              de fichier de configuration                       /#
#/ Date: 01/06/2022                                               /#
####################################################################

import re
import ast
from os.path import isfile, exists


class Config():
	def __init__(self,file,separator=" = ", escape_line="#", auto_create=False, read_only=False):
		self.reg = r'\[[0-9A-Za-z-_ ]*\]'

		self.separator=separator
		self.escape_line = escape_line

		self.read_only = read_only

		if isfile(file) and exists(file):
			self.file = file
		else:
			if auto_create==False:
				print("Error: File not exists")
			else:
				with open(file,'w') as f:
					self.file = file

	#Str to real type
	def return_data(self, data):
		if data=="true" or data=="True":
			return True
		elif data=="false" or data=="False":
			return False
		else:
			try:
				 return ast.literal_eval(data)
			except:
				return data


	def indent_line(self,line):
		lineC = line.replace("\t","")
		line = ""
		l = ""
		for i, char in enumerate(lineC):
			if (char=="'" and lineC.count("'")%2==0) or (char=='"' and lineC.count('"')%2==0):
				if l==char:
					l=""
				else:
					l=char
			else:
				if len(l)==0 and i+1<len(lineC) and lineC[i]==" " and lineC[i+1]==" ":
					pass
				else:
					line+=char
		return line


	def list_section(self):
		if hasattr(self,'file'):
			with open(self.file) as f:
				sec_array = []
				for line in f.readlines():
					line = self.indent_line(line.strip())
					if re.match(self.reg,line):
						sec_array.append(line.replace("[","").replace("]",""))
				return sec_array


	def load(self,val=None,section=None):
		lock=False
		ban = False
		data = []
		sec = ''
		dict_data = {}

		if hasattr(self,'file'):
			if section!=None and section!="" and section not in self.list_section():
				return data

			with open(self.file) as f:
				for line in f.readlines():
					line = self.indent_line(line.strip())
					if ban==True and line.startswith("[") and line.endswith("]"):
						ban=False

					if line.startswith(self.escape_line+"[") and line.endswith("]"):
						ban=True
					elif line.startswith(self.escape_line):
						pass
					else:
						if ban==False:
							if section!=None:
								if section!="" and re.match(self.reg,line):
									if lock==False:
										if line=="["+section+"]":
											lock=True
											data = []
									else:
										lock=False
										break

								else:
									if lock==True:
										if len(line)!=0:
											if val==None:
												data.append(line)
											else:
												line = line.split(self.separator)
												if line[0]==val:
													return self.return_data(line[1])
									elif section=="":
										if len(line)!=0:
											if not line.startswith("[") and not line.endswith("]"):
												if val==None:
													data.append(line)
												else:
													line = line.split(self.separator)
													if line[0]==val:
														return self.return_data(line[1])
											else:
												break

							elif val!=None:
								if re.match(self.reg,line):
									sec = line.replace("[","").replace("]","")

								if len(line)!=0:
									line = line.split(self.separator)
									if line[0]==val:
										data.append(sec + self.separator + line[1])

							else:
								if len(line)!=0:
									if sec not in dict_data.keys():
										dict_data[sec] = {}
									if not re.match(self.reg,line):
										line = line.split(self.separator)
										dict_data[sec][line[0]] = self.return_data(line[1])
									else:
										sec = line.replace("[","").replace("]","")

				if val==None and section==None:
					return dict_data

				if len(data)!=0:
					for element in data:
						element=element.split(self.separator)
						dict_data[element[0]] = self.return_data(element[1])
					return dict_data

				return data


	def edit(self,line,val,key,temp):
		if len(line)!=0:
			if val!=None:
				lineT = line.split(self.separator)
				if lineT[0]==val:
					self.new_content.append(temp.replace(self.separator+lineT[1], self.separator+str(key)))
					return True
				else:
					self.new_content.append(temp)
					return True
		return False


	def change(self,val=None,key=None,section=None):
		if self.read_only==False:
			if val!=None and key!=None:
				if isinstance(key,str) or isinstance(key,list) or isinstance(key,int) or isinstance(key,float) or isinstance(key,bool) or isinstance(key,dict):
					if hasattr(self,'file'):
						with open(self.file) as f:
							self.new_content = []
							lock=False

							for line in f.readlines():
								temp = line.rstrip()
								line = self.indent_line(line.strip())
								if len(line)!=0:
									if section!=None:
										if section!="" and re.match(self.reg,line):
											if lock==False:
												if line=="["+section+"]":
													lock=True
											else:
												lock=False

										else:
											if lock==True:
												if self.edit(line,val,key,temp):
													continue
									else:
										if self.edit(line,val,key,temp):
											continue

									self.new_content.append(temp)
								else:
									self.new_content.append(temp)
						
						with open(self.file,"w") as f:
							f.write("\n".join(self.new_content))
		else:
			print("Read-only mode")


	def add(self,val=None,key=None,section=None):
		if self.read_only==False:
			exist = True
			new_content=None
			lock=False

			if hasattr(self,'file'):
				if section!=None and section!="" and section not in self.list_section():
					exist = False

				if val!=None and val!="" and key!=None and not (isinstance(key,str) or isinstance(key,list) or isinstance(key,int) or isinstance(key,float) or isinstance(key,bool) or isinstance(key,dict)):
					print("Key not supported")
					return

				with open(self.file) as f:
					if exist==False:
						new_content=f.read()
						if new_content[len(new_content)-1]=="\n":
							new_content+="\n["+section+"]"
						else:
							new_content+="\n\n["+section+"]"
						if val!=None and val!="" and key!=None:
							new_content+="\n"+val+self.separator+str(key)

					else:
						data = c.load()
						if section!=None:
							se_test = section
						else:
							se_test = ""

						if val!=None:
							se = data[se_test]
							if val in se.keys():
								print("Key already exist")
								return

						if val!=None and val!="" and key!=None:
							if section=="" or section==None:
								new_content=val+self.separator+str(key)+"\n"
								new_content+=f.read()
							else:
								new_content = []
								for line in f.readlines():
									line_temp = line.rstrip()
									line = self.indent_line(line.strip())
									if line_temp!="":
										if section!=None:
											if section!="" and re.match(self.reg,line):
												if lock==False:
													if line=="["+section+"]":
														if len(se.keys())==0:
															line_temp+="\n"+val+self.separator+str(key)
														lock=True
												else:
													lock=False

											else:
												if lock==True:
													if "\t" in line_temp:
														line_temp+="\n"+("\t"*line_temp.count('\t'))+val+self.separator+str(key)
														lock=False
													
									new_content.append(line_temp)

								new_content = "\n".join(new_content)

				if new_content!=None:
					with open(self.file,'w') as f:
						f.write(new_content)
		else:
			print("Read-only mode")


	def delete(self,val=None,section=None):
		if self.read_only==False:
			if hasattr(self,'file'):
				with open(self.file) as f:
					lock=False
					new_content=""
					sec = ""
					ban=False

					for line in f.readlines():
						lineT = line
						line = self.indent_line(line.strip())

						if line.startswith("[") and line.endswith("]"):
							ban=False
							sec = line.replace("[","").replace("]","")

						elif line.startswith(self.escape_line+"[") and line.endswith("]"):
							ban=True
							sec = line.replace(self.escape_line+"[","").replace("]","")

						if ban!=True:
							if section!=None and section!="":
								if section!="" and re.match(self.reg,line):
									if lock==False:
										if line=="["+section+"]":
											lock=True
											if val!=None:
												new_content+=lineT	
										else:
											new_content+=lineT	
									else:
										new_content+=lineT	
										lock=False
								else:
									if lock==True:
										if val==None:
											pass
										else:
											line = line.split(self.separator)
											if line[0]==val:
												pass
											else:
												new_content+=lineT
									else:
										new_content+=lineT
							else:
								if val!=None and sec=="":
									line = line.split(self.separator)
									if line[0]==val:
										pass
									else:
										new_content+=lineT
								else:
									new_content+=lineT
						else:
							new_content+=lineT

					if new_content!="":
						with open(self.file,'w') as f:
							f.write(new_content)
		else:
			print("Read-only mode")


	def disabled_line(self, section=None):
		dict_data = {}
		
		if hasattr(self,'file'):
			with open(self.file) as f:
				ban=False
				sec = ""

				for line in f.readlines():
					line = self.indent_line(line.strip())
					if len(line)!=0:
						if line.startswith("[") and line.endswith("]"):
							sec = line.replace("[","").replace("]","")
							if ban==True:
								ban=False

						if line.startswith(self.escape_line+"[") and line.endswith("]"):
							ban=True
							sec = line.replace(self.escape_line+"[","").replace("]","")

						elif line.startswith(self.escape_line):
							line = line[1:len(line)].split(self.separator)
							if sec not in dict_data.keys():
								dict_data[sec] = {}
							dict_data[sec][line[0]] = self.return_data(line[1])

						else:
							if ban==True:
								line = line.split(self.separator)
								if sec not in dict_data.keys():
									dict_data[sec] = {}
								dict_data[sec][line[0]] = self.return_data(line[1])
		return dict_data
