'''
Created on Nov 18, 2018

@author: ppoddar
'''
import sys
import os
import yaml
from argparse import ArgumentParser

class ResourceType():
    def __init__(self):
        self.data = {}
    
    def kind(self):
        return self.data['kind']
    
    def load(self, yaml_file):
        self.data = yaml.load(yaml_file) 
        if not 'kind' in self.data:
            raise ValueError('resource definition {0} is missing "kind" attribute'.format(yaml_file.name))       
        else:
            print 'loaded definition of {0} from {1}'.format(self.data['kind'], yaml_file.name)

    def validate(self, instance):
        for k in self.data:
            if not k in instance:
                raise ValueError('instance is missing {0}'.format(k))

class ResoureRepository:
    def __init__(self):
        self.repo = {}
    
    def load(self, repodir):
        if not os.path.isdir(repodir):
            raise ValueError('''Resource definition directory {0}
                does not exist'''.format(repodir))
            
        files = [f for f in os.listdir(repodir) if f.endswith('.yml')] 
        for f in files:
            full_path = os.path.join(repodir, f)
            with open(full_path, 'r') as definition:
                rsrc_type = ResourceType()
                rsrc_type.load(definition)
                kind = rsrc_type.kind()
                if kind in self.repo:
                    raise ValueError('kind {0} already exists')
                self.repo[kind] = rsrc_type
                
    def hasKind(self, kind):
        return kind in self.repo
    
    def get_type(self, kind):
        if kind in self.repo:
            return self.repo[kind]
        else:
            raise ValueError('resource type {0} not found'.format(kind))

class Resource():
    def __init__(self):
        self.data = {}
    
    def load(self, yaml_file):
        self.data = yaml.load(yaml_file)
        if not self.data:
            raise ValueError('no resource read from {0}'.format(yaml_file.name))       
        if not 'kind' in self.data:
            raise ValueError('resource {0} is missing "kind" attribute'.format(yaml_file.name))       
    def kind(self):
        return self.data['kind']

if __name__=='__main__':
    parser = ArgumentParser("kubernetes tool")
    parser.add_argument('--repos', dest='repo', 
        required=False,
        default='repo',
        help='directory of *.yml files that define each reource')
    parser.add_argument('files', 
        metavar='files', nargs='+',
        help='resource files')
    
    args = parser.parse_args(sys.argv[1:])
#    print 'parsed arguments {0}'.format(args)
    
    repo = ResoureRepository()
    repo.load(os.path.join(os.getcwd(), args.repo))
    for f in args.files:
        with open(f, 'r') as data_file:
            rsrc = Resource()
            rsrc.load(data_file)
            repo.get_type(rsrc.kind()).validate(rsrc.data)
            print 'loaded {0} from {1}'.format(rsrc.kind(), f)
    
    

