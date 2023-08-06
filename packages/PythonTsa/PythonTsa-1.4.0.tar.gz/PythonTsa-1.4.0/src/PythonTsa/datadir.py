def getdtapath():
      """ path of Ptsdata"""
      import os
      import sys
      import PythonTsa 
      dtapath=os.path.dirname(PythonTsa.__file__)
      if sys.platform=='win32':
         newdtapath=dtapath+'\\Ptsadata\\'
      elif sys.platform=='darwin':   
            newdtapath=dtapath+'/Ptsadata/'
      elif sys.platform=='linux':   
            newdtapath=dtapath+'/Ptsadata/'
      else:
            print('Sorry, your platform should be Windows, Mac or Linux !')
            
      return newdtapath