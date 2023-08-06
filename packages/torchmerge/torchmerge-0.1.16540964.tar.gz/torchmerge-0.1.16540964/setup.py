# pylint: disable=C0321,C0103,C0301,E1305,E1121,C0302,C0330,C0111,W0613,W0611,R1705
# -*- coding: utf-8 -*-
"""


"""
import io, os, subprocess, sys
from setuptools import find_packages, setup

######################################################################################
root = os.path.abspath(os.path.dirname(__file__))



##### Version  #######################################################################
version ='0.1.16540964'
cmdclass= None
print("version", version)



##### Requirements ###################################################################
#with open('install/reqs_image.cmd') as fp:
#    install_requires = fp.read()
install_requires = ['pyyaml', 'python-box', 'fire', 'utilmy' ]



###### Description ###################################################################
#with open("README.md", "r") as fh:
#    long_description = fh.read()

def get_current_githash():
   import subprocess 
   # label = subprocess.check_output(["git", "describe", "--always"]).strip();   
   label = subprocess.check_output([ 'git', 'rev-parse', 'HEAD' ]).strip();      
   label = label.decode('utf-8')
   return label

githash = get_current_githash()


#####################################################################################
ss1 = """

 Merge mutiple models or embedding into a single one very easily
 in Pytorch.





## Usage

https://colab.research.google.com/drive/1vOFxEcLQdgCxCCJCkp-mxouTQ1f8F5FX?usp=sharing



### Example Short:

import os, random, numpy as np, pandas as pd ;from box import Box
from copy import deepcopy
import copy, collections
import torch
import torch.nn as nn
import torchvision


#############################################################################################
def test3d():    
    from box import Box ; from copy import deepcopy
    from torch.utils.data import DataLoader, TensorDataset
    

    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = {}

 
    ##################################################################
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly' 
        train_config                           = Box({})
        train_config.LR                        = 0.001
        train_config.SEED                      = 42
        train_config.DEVICE                    = 'cpu'
        train_config.BATCH_SIZE                = 64
        train_config.EPOCHS                    = 1
        train_config.EARLY_STOPPING_THLD       = 10
        train_config.VALID_FREQ                = 1
        train_config.SAVE_FILENAME             = './model.pt'
        train_config.TRAIN_RATIO               = 0.7
        train_config.VAL_RATIO                 = 0.2
        train_config.TEST_RATIO                = 0.1


    ####################################################################
    def load_DataFrame():
        return None


    def test_dataset_f_mnist(samples=100):
        from sklearn.model_selection import train_test_split
        from torchvision import transforms, datasets
        # Generate the transformations
        train_list_transforms = [transforms.ToTensor(),transforms.Lambda(lambda x: x.repeat(3, 1, 1))]

        dataset1 = datasets.FashionMNIST(root="data",train=True,
                                         transform=transforms.Compose(train_list_transforms),download=True,)
        
        #sampling the requred no. of samples from dataset 
        dataset1 = torch.utils.data.Subset(dataset1, np.arange(samples))
        X,Y    = [],  []
        for data, targets in dataset1:
            X.append(data)
            Y.append(targets)

        #Converting list to tensor format
        X,y = torch.stack(X),torch.Tensor(Y)

        train_r, test_r, val_r  = train_config.TRAIN_RATIO, train_config.TEST_RATIO,train_config.VAL_RATIO
        train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_r)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_r / (test_r + val_r))
        return (train_X, train_y, valid_X, valid_y, test_X , test_y)


    def prepro_dataset(self,df:pd.DataFrame=None):
        train_X ,train_y,valid_X ,valid_y,test_X, test_y = test_dataset_f_mnist(samples=100)
        return train_X ,train_y,valid_X ,valid_y,test_X,test_y


    
    ### modelA  ########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA               = {}   
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id  = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    modelA = me.model_create(ARG.modelA)
    


    ### modelB  ########################################################
    from torchvision import  models
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = {}   
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id  = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    modelB = me.model_create(ARG.modelB )




    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  
    ARG.merge_model           = {}
    ARG.merge_model.name      = 'modelmerge1'

    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim 

    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]  ### Common embedding is 768
    ARG.merge_model.architect.merge_custom     = None


    ### Custom head
    ARG.merge_model.architect.head_layers_dim  = [ 128, 1]    ### Specific task    
    ARG.merge_model.architect.head_custom      = None
  
  
    ARG.merge_model.dataset       = {}
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config


    model = me.MergeModel_create(ARG, model_create_list= [modelA, modelB ] )
    model.build()



    #### Run Model   ###################################################
    model.training(load_DataFrame, prepro_dataset) 

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)








 




"""
### git hash : https://github.com/arita37/myutil/tree/{githash}

long_description = f""" ``` """ + ss1 +  """```"""



### Packages  ########################################################
packages = ["torchmerge"] + ["torchmerge." + p for p in find_packages("torchmerge")]
#packages = ["torchmerge"] + ["torchmerge.viz" + p for p in find_packages("torchmerge.viz")]
packages = ["torchmerge"] + [ p for p in  find_packages(include=['torchmerge.*']) ]
print(packages)


scripts = [     ]



### CLI Scripts  ###################################################   
entry_points={ 'console_scripts': [

 ] }




##################################################################   
setup(
    name="torchmerge",
    description="utils",
    keywords='utils',
    
    author="Nono",    
    install_requires=install_requires,
    python_requires='>=3.7.5',
    
    packages=packages,

    include_package_data=True,
    #    package_data= {'': extra_files},

    package_data={
       '': ['*','*/*','*/*/*','*/*/*/*']
    },

   
    ### Versioning
    version=version,
    #cmdclass=cmdclass,


    #### CLI
    scripts = scripts,
  
    ### CLI pyton
    entry_points= entry_points,


    long_description=long_description,
    long_description_content_type="text/markdown",


    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: ' +
          'Artificial Intelligence',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: ' +
          'Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
      ]
)



def os_bash_append(cmd):
  """  Append to bashrc
  """
  try :
    fpath = os.path.expanduser("~/.bashrc")
    with open(fpath, "r") as bashrc:
        bashrc = "".join( bashrc.readlines())

    #if cmd in bashrc :
    #    return False   #### Already exist

    with open(fpath, "at") as bashrc:
        bashrc.write("\n"+ cmd +"\n")
    return True
  except Exception as e:
    print(e)  
    return False


#### Add environemment variables  torchmerge path
try :
    repopath = os.path.dirname( os.path.abspath(__file__).replace("\\", "/") )  + "/torchmerge/"
    if 'win' in sys.platform :
        os.system(f" set  torchmerge='{repopath}/' ")  ### Any new session
        os.system(f" setx torchmerge='{repopath}/' ")  ### Current session

    elif 'linux' in sys.platform :
        os_bash_append(f"""export torchmerge={repopath}/    """)
        os.system(f" export torchmerge={repopath}/ ")
        print(' source  ~/.bashrc  ')

    print(" $torchmerge  can be used as shortcut of the package library path for Command Line Usage")    

except :
    pass



def os_cmd_to_bashrc(cmd):
    try :
        if 'win' in sys.platform :
            os.system(f""" set  {cmd} """)  ### Any new session
            os.system(f""" setx {cmd} """)  ### Current session

        elif 'linux' in sys.platform :
            os_bash_append(f"""{cmd}""")
            print(' source  ~/.bashrc  ')

    except :
        pass








































"""
alias sspark='python /workspace/myutil/torchmerge/sspark/src/util_spark.py'


from setuptools import setup, find_packages


setup(
    name='xpdtools',
    version='0.2.0',
    packages=find_packages(),
    description='data processing module',
    zip_safe=False,
    package_data={'xpdan': ['config/*']},
    include_package_data=True,
    entry_points={'console_scripts': 'iq = xpdtools.raw_to_iq:main_cli'}
)


def main_cli(): fire.Fire(main)
    
    
"""





"""
:: Sets environment variables for both the current `cmd` window 
::   and/or other applications going forward.
:: I call this file keyz.cmd to be able to just type `keyz` at the prompt 
::   after changes because the word `keys` is already taken in Windows.

@echo off

:: set for the current window
set APCA_API_KEY_ID=key_id
set APCA_API_SECRET_KEY=secret_key
set APCA_API_BASE_URL=https://paper-api.alpaca.markets

:: setx also for other windows and processes going forward
setx APCA_API_KEY_ID     %APCA_API_KEY_ID%
setx APCA_API_SECRET_KEY %APCA_API_SECRET_KEY%
setx APCA_API_BASE_URL   %APCA_API_BASE_URL%

"""





