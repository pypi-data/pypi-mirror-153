'''
Created on 25.05.2022

@author: maxwellgerber

see https://gist.github.com/maxwellgerber/4caae07161ea66123de4d6c374387786

'''
from itertools import combinations, permutations, chain
import datetime

class FunctionalDependencySet:
    '''
    a functional dependency set
    '''

    def __init__(self, attributes:str="",title:str="",description:str="",useSetNotation:bool=False,debug:bool=False):
        '''
        constructor
        
        Args:
            attributes(str): a string of attribute variable names of the scheme
            title(str): a title for this functional Dependency Set
            description(str): a description for this functional Dependency Set
            useSetNotation(bool): should the dependencies be shown in setNotation?
            debug(bool): if True switch debugging on
        '''
        self.title=title
        self.description=description
        self.useSetNotation=useSetNotation
        self.debug=debug
        self.isodate=datetime.datetime.now().isoformat()
        #list of FDs of the scheme. An FD is stored as a tuple (x, y), meaning x -> y
        self.dependencies = []

        #set of attributes of the scheme
        self.attributes = set()
        self.attribute_map={}

        self.isdecomposed = False
        
        for attr in attributes:
            self.add_attribute(attr)
            
            
    def __str__(self):
        '''
        return my text representation
        '''
        text=self.stringify_dependencies()
        return text
    
    def set_list_as_text_list(self,set_list:list,delim:str=''):
        '''
        convert a list of sets to a list of strings using the given delimiter
        
        Args:
            set_list(list): list of sets
            delim(str): the delimiter to use
            
        Returns:    
            list: of stringified sets
        '''
        text_list=[]
        for a_set in set_list: 
            text_list.append(self.stringify_set(a_set,delim=delim))
        text_list=sorted(text_list)
        return text_list
    
    def stringify_set(self,pSet,delim=''):
        '''
        return a string representation of the given set using the given delimiter
        
        Args:
            pSet(set): the set to stringify
            delim(str): the delimiter to use
        '''
        sortedElements=sorted([str(elem) for elem in pSet])
        text=delim.join(sortedElements)          
        return text
    
    def stringify_dependencies(self):
        '''
        stringifies the set of dependencies
        '''
        if self.useSetNotation:
            groupDelim=', '
            depDelim=', '
            openBrace='{'
            closeBrace='}'
            arrow=' → '
        else:
            groupDelim=','
            depDelim=''
            openBrace=''
            closeBrace=''
            arrow='→' 
        #text='{'+ ', '.join('{' + ', '.join(attr for attr in sorted(dep[0])) + '}' + ' → ' + '{' + ', '.join(attr for attr in sorted(dep[1])) + '}' for dep in self.dependencies) + '}'
        text='{'
        delim=''
        for left,right in self.dependencies:
            leftAttrs=self.stringify_set(left,depDelim)
            rightAttrs=self.stringify_set(right,depDelim)
            text+=f"{delim}{openBrace}{leftAttrs}{closeBrace}{arrow}{openBrace}{rightAttrs}{closeBrace}"
            delim=groupDelim
        text+="}"
        return text
     
    def add_attribute(self, attr_var:str,attr_english_name:str=None,attr_german_name:str=None):
        '''
        add attribute to the attribute set of the scheme

        Args:
            attr_var(string): attribute variable name to be added to the scheme
            attr_english_name(string): the name of the attribute in english
            attr_german_name(string): the name of the attribute in german
        '''
        if attr_english_name is None:
            attr_english_name=attr_var
        if attr_german_name is None:
            attr_german_name=attr_english_name
        attr=Attribute(attr_var,attr_english_name,attr_german_name)
        self.attributes.add(attr_var)
        self.attribute_map[attr_var]=attr
    
    def add_dependency(self, pre, post):
        '''
        add dependency to the dependency list of the scheme

        Args:
            pre(set): attributes that initiate the FD (left of the arrow)
            post(set): attributes that are determined by the FD (right of the arrow)
        '''
        for i in chain(pre,post):
            if i not in self.attributes:
                # exception when an attribute is used that is not in the list of attributes of the dependency
                raise Exception(f"Attribute {i} does not exist")
        self.dependencies.append((set(pre),set(post)))
        
    def remove_dependency(self, pre, post):
        '''
        remove depedency from the dependency list of the scheme

        Args:
            pre(str): attributes that initiate the FD (left of the arrow)
            post(str): attributes that are determined by the FD (right of the arrow)
        '''
        for i in chain(pre, post):
            if i not in self.attributes:
                # exception when an attribute is used that is not in the list of attributes of the dependency
                raise Exception(f"Attribute {i} does not exist")
        self.dependencies.remove((set(pre), set(post)))


    def get_attr_closure(self, attr, withSort:bool=False):
        '''
        get the close of the given attribute
        
        Args:
            attr(str): the name of the attribute to calculate the closure for
            
        Returns:
            set: the closure of the attribute 
        '''
        #closure set is build up iteratively, until it does not expand anymore
        closure = set(attr)
        #set of previos iteration
        last = set()
        while closure != last:
            last = closure.copy()
            #check all FDs whether their initiators are part of the closure
            #and add closure of the respective FD to the calculating closure
            for dep in self.dependencies:
                if dep[0].issubset(closure):
                    closure.update(dep[1])
        if withSort:
            closure=sorted(closure)          
        return closure
    
    def attribute_combinations(self):
        '''
        generator for keys
        '''
        for i in range(1, len(self.attributes)+1):
            for keys in combinations(self.attributes, i):
                yield keys
        
    def find_candidate_keys(self):
        '''
        find candidate keys of the scheme
        '''
        ans = []
        #check closures of all attributes and attribute combinations iteratively
        #smaller candidate keys added first
        for keys in self.attribute_combinations():
            if(self.get_attr_closure(keys) == self.attributes):
                k = set(keys)
                #no subset of currently checked key is already in
                if not any([x.issubset(k) for x in ans]):
                    ans.append(k)
        return ans
    
    def decompose(self):
        '''
        decomposition algorithm
        '''
        self.isdecomposed = True
        self.tables = [self.attributes]
        for dep in self.dependencies:
            for attr_set in self.tables:
                #newset contains the unity of attributes of the FD
                newset = dep[0].symmetric_difference(dep[1])
                #if newset is real subset, extra attributes still exist
                #--> need to break it up
                if newset.issubset(attr_set) and newset != attr_set:
                    ## print("Splitting {} into {} and {}".format(attr_set, attr_set.difference(dep[1]), newset))
                    #split attributes of the FD closure off the attribute set
                    attr_set.difference_update(dep[1])

                    #add new BCNF set to list of attribute sets
                    self.tables.append(newset)
        return self.tables
        
    def decompose_all(self):
        ## Messy sets and tuples to get rid of duplicates, eew
        tables_possibilities = []
        
        for ordering in permutations(self.dependencies):
            tbl = [self.attributes.copy()]
            
            for dep in ordering:
                for attr_set in tbl:
                    newset = dep[0].symmetric_difference(dep[1])
                    if newset.issubset(attr_set) and newset != attr_set:
                        attr_set.difference_update(dep[1])
                        tbl.append(newset)
                        
            tbl = [tuple(x) for x in tbl]
            tables_possibilities.append(tuple(tbl))
            
        return set(tables_possibilities)
        
    def is_lossy(self):
        '''
        check for lossyness
        
        Returns:
            bool: True if if one of my dependencies is not preserved
        '''
        if not self.isdecomposed:
            raise Exception("Can't tell if lossy if the FD hasn't beend decomposed yet")
        for dep in self.dependencies:
            if not self.is_preserved(dep):
                return True
        return False
        
    def is_preserved(self, dep):
        '''
        check wether the given dependency is preserved
        
        Returns:
            bool: True if 
        '''
        pre = dep[0].symmetric_difference(dep[1])
        for attr_set in self.tables:
            if pre == attr_set:
                return True
        return False

    def calculate_fds_in_subset(self, subset):
        '''
        calculate all dependencies in a subset. Also includes dependencies for which
        attribute parts are missing because they are not in the subset. Does not include
        original dependencies that have lost all there attributes in precondition or closure

        '''
        subset_dependencies = []
        for dep in self.dependencies:
            new_dep_pre = set()
            new_dep_post = set()
            #check whether attributes occur in pre or post of the original FD
            for attr in dep[0]:
                if attr in subset:
                    new_dep_pre.add(attr)
            for attr in dep[1]:
                if attr in subset:
                    new_dep_post.add(attr)
            #only add new dependency if none of both sides is empty
            if new_dep_pre != set() and new_dep_post != set():
                subset_dependencies.append((new_dep_pre, new_dep_post))
        return subset_dependencies


    def is2NF(self):
        '''
        calculates whether the FD set is in 2NF: Every attribute has to depend on the whole CK.
        Check for every attribute whether ther is a part of any of the CKs which has the attribute in its closure
        '''
        ckeys = self.find_candidate_keys()
        # check every non-ck-attribute
        for attr in self.attributes:
            skip = False
            for ckey in ckeys:
                for ckey_part in ckey:
                    if attr == ckey_part:
                        skip = True
                        
            if skip == True:
                continue

            # check every key candidate
            for ckey in ckeys:
                # check every subset of keys (not yet)
                for ckey_part in ckey:
                    ckey_part_closure = self.get_attr_closure(ckey_part)
                    if attr in ckey_part_closure:
                        return False
        return True
    
    def is3NF(self):
        '''
        calculates whether the FD set is in 3NF: There are no dependencies between non-key attributes
        '''
        ckeys = self.find_candidate_keys()

        for dep in self.dependencies:

            # get all attributes of an fd
            dep_attributes = set()
            dep_attributes.update(dep[0])
            dep_attributes.update(dep[1])
            dep_has_ckey_attr = False

            # check all attributes of the fd whether at least one of them is contained in a ckey
            for attr in dep_attributes:
                for ckey in ckeys:
                    if set(attr).issubset(ckey):
                        dep_has_ckey_attr = True
                        break
            if not dep_has_ckey_attr:
                return False
        return True
        
    def generate_cluster(self,shape:str='box',indent:str='  '):
        '''
        graphviz digraph subgraph (cluster) generation for this functional dependency set
        
        Args:
            shape(str): the shape to use - default: box
            indent(str): indentation - default: two spaces
        Return:
            str: graphviz markup
        '''
        markup=''
        # sort dependencies by largest pre
        dependencies = self.dependencies.copy()
        dependencies.sort(key=lambda dep: len(dep[0]), reverse=True)

        # collect attributes that are only on the right side
        only_post = self.attributes.copy()
        # generate clusters
        cluster_markup = ''
        for dep in dependencies:
            pre, post = dep
            only_post -= pre
            cluster_name=''.join(sorted(pre))
            cluster_markup += f'{indent}subgraph cluster_{cluster_name}{{\n'
            cluster_markup += f'{indent} label="{cluster_name}"\n'
            for attrVar in sorted(pre):
                attr = self.attribute_map[attrVar]
                cluster_markup += f'{indent}{indent}{attrVar} [shape={shape} label="{attr}"]\n'
            cluster_markup += f'{indent}}}\n'
        
        # generate arrows
        arrow_markup = ''
        for dep in dependencies:
            pre, post = dep
            for attrVar in sorted(post):
                arrow_markup += f'{indent}{sorted(pre)[0]}->{attrVar}\n'

        # create markup for only post attributes
        only_post_markup = ''
        for attrVar in sorted(only_post):
            attr = self.attribute_map[attrVar]
            only_post_markup += f'{indent}{attrVar} [shape={shape} label="{attr}"]\n'

        # concatenate markup
        markup += only_post_markup
        markup += cluster_markup
        markup += arrow_markup
        return markup

    def as_graphviz(self,withCluster:bool=True):
        '''
        
        convert me to a graphviz markup e.g. to try out in 
        
        http://magjac.com/graphviz-visual-editor/
        or 
        http://diagrams.bitplan.com
        
        Return:
            str: the graphviz markup for this functional DependencySet
        '''
        markup=f"#generated by {__file__} on {self.isodate}\n"
        markup+="digraph functionalDependencySet{"
        # add title see https://stackoverflow.com/a/6452088/1497139
        markup+=f'''
  // title
  labelloc="t";
  label="{self.title}"
'''
        if not withCluster:
            markup+="// Attribute variables \n"   
            for attrVar in sorted(self.attributes):
                attr=self.attribute_map[attrVar]
                markup+=(f"""  {attrVar} [ shape=box label="{attr}"] \n""")
        else:
            markup+=self.generate_cluster()
        markup+="}"
        return markup

    def left_reduction(self):
        '''
        executes a left reduction on the dependencies from this fdset
        '''
        remaining_deps = self.dependencies.copy()
        while remaining_deps:
            dep = remaining_deps.pop(0)
            pre, post = dep
            for attr in sorted(pre):
                if post <= self.get_attr_closure(pre - {attr}):
                    self.remove_dependency(pre, post)
                    self.add_dependency(pre - {attr}, post)
                    pre = pre - {attr}

    def right_reduction(self):
        '''
        executes a right reduction on the dependencies from this fdset
        '''
        remaining_deps = self.dependencies.copy()
        while remaining_deps:
            dep = remaining_deps.pop(0)
            pre, post = dep
            for attr in sorted(post):
                self.remove_dependency(pre, post)
                self.add_dependency(pre, post - {attr})
                if {attr} <= set(self.get_attr_closure(pre)):
                    post = post - {attr}
                else:
                    self.remove_dependency(pre, post - {attr})
                    self.add_dependency(pre, post)

    def remove_empty_fds(self):
        '''
        remove empty fds of form "A → {}" from this fdset
        '''
        for dep in self.dependencies:
            pre, post = dep
            if post == set():
                self.remove_dependency(pre, post)

    def combine_fds(self):
        '''
        executes a left reduction for this fdset
        '''
        combined_dependencies = []
        while self.dependencies:
            pre, post = self.dependencies.pop(0)
            new_post = post
            for dep in self.dependencies:
                if dep[0] == pre:
                    new_post = new_post | dep[1]
                    self.remove_dependency(dep[0], dep[1])
            combined_dependencies.append((pre, new_post)) 
        self.dependencies = combined_dependencies

    def canonical_cover(self):
        '''
        determines the canonical cover of this fdset

        4 substeps with respective functions

        https://git.rwth-aachen.de/i5/teaching/dbis-vl/-/raw/main/6-RelDesign/6-RelationaleEntwurfstheorie.pdf#page=39
        '''
        self.left_reduction()
        self.right_reduction()
        self.remove_empty_fds()
        self.combine_fds()

    def add_attributes(self):
        '''
        add attributes of new relation scheme
        '''
        pass

    def add_fds_of_attribute_subset(self):
        '''
        add fds of the original relation that are buildable with the attribute subset
        '''
        pass

    def create_new_fdsets(self):
        '''
        create fdsets from the dependencies resulting from the canonical cover

        Return:
            list[FunctionalDependencySet]: list of fdsets created from the dependencies resulting from the canonical cover
        '''
        deps = self.dependencies.copy()
        i = 1
        new_fdsets = []
        while deps:
            tmp = deps.pop(0)
            pre, post = tmp
            new_attributes = pre | post
            new_deps = [tmp]
            for dep in deps:
                if dep[0] | dep[1] <= new_attributes:
                    new_deps.append(dep)
                    deps.remove(dep)
            fds = FunctionalDependencySet(new_attributes, 'R' + str(i))
            i += 1
            for dep in new_deps:
                fds.add_dependency(dep[0], dep[1])
            new_fdsets.append(fds)
        return new_fdsets

    def synthesize(self):
        '''
        synthesize algorithm
        
        see https://git.rwth-aachen.de/i5/teaching/dbis-vl/-/raw/main/6-RelDesign/6-RelationaleEntwurfstheorie.pdf#page=76
        and Kemper page 197

        Return:
            list[FunctionalDependencySet]: list of synthesized fdsets deriving from this fdset
        '''
        keys = self.find_candidate_keys()
        self.canonical_cover()
        fdsets = self.create_new_fdsets()
        fdsets_with_key = self.create_optional_key_scheme(keys, fdsets)
        reduced_fdsets = self.remove_subset_relations(fdsets_with_key)
        return reduced_fdsets

    def create_optional_key_scheme(self, keys, fdsets):
        '''
        creates a new fdset if key is not subset of any of the existing sets attributes

        Return:
            list[FunctionalDependencySet]: The list of fdsets with relation that has key candidate of original scheme
        '''
        for key in keys:
            for fds in fdsets:
                if set(key) <= fds.attributes:
                    return fdsets
        key = set(keys[0])
        fds = FunctionalDependencySet(key, 'R' + str(len(fdsets) + 1))
        m = len(key)//2
        fds.add_dependency(sorted(key)[:m], sorted(key)[m:])
        fdsets.append(fds)
        return fdsets

    def remove_subset_relations(self, fdsets):
        '''
        removes fdsets with attributes that are a subset of another fdset

        Return:
            list[FunctionalDependencySet]: The reduced list of fdsets
        '''
        if self.debug:
            print(fdsets)
        for fds in fdsets.copy():
            attributes = fds.attributes
            conflict = next((fdset for fdset in fdsets if fds.title != fdset.title and attributes <= fdset.attributes), None)
            if conflict is not None:
                fdsets.remove(fds)
        return fdsets

class Attribute:
    '''
    an Attribute e.g. 
        Example: Attribute('A', 'Wikidata identifier', 'Wikidata-Schlüssel')
    '''
    def __init__(self, var_name:str, english_name:str, german_name:str):
        '''
        constructor

        Args:
            var_name(str): the Variable name
            english_name(str): the english name
            german_name(str): the german name
 
        '''
        self.var_name=var_name
        self.german_name=german_name
        self.english_name=english_name
        
    def __str__(self):
        text=f"{self.var_name}≡{self.english_name}≡{self.german_name}"
        return text