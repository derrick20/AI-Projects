import time

variables = {}
adjacencies = {}

def make_graph(edges_file, regions_file):
   with open(regions_file) as f: # set
      for line in f:
         r = [i for i in line.split()][0]
         #print(r)
         variables[r] = ["R", "G", "B"]
         adjacencies[r] = [] # start out with empty adj list
  # print(variables)
   #print(adjacencies)
   with open(edges_file) as f: # set up graph edges
      for line in f:
         r1, r2 = [i for i in line.split()]
         adjacencies[r1].append(r2)
         adjacencies[r2].append(r1)



def backtracking_search(adjacencies):
   return recursive_backtrack({}, adjacencies)
   
def recursive_backtrack(assignment, adjacencies):
   if is_complete(variables, assignment, adjacencies):
      return assignment
   var = select_unassigned_var(variables, assignment, adjacencies)
   for value in variables[var]: # the RGB choices - we will modify this later, to shrink the choices. For now be inefficient
      if is_valid(var, value, assignment, adjacencies):
        # assignment[var] = None # remove the assignment of that color, since it was invalid
     # else:
         assignment[var] = value
         result = recursive_backtrack(assignment, adjacencies)
         if result != None:
            return result
         else:
            assignment[var] = None # this means that it ended up not working, so we need to try others
   return None
   
def select_unassigned_var(variables, assignment, adjacencies):
   min_constraints = 1000
   LCV = list(variables.keys())[0] # pick the first variable arbitrarily
   for var in variables:
      count = 0
      if var not in assignment: # they haven't been assigned a color
         for adj in adjacencies[var]: # see how many of its neighbors are constrained
            if adj not in assignment or assignment[adj] == None: # hasn't been assigned, so this will constrain it
               count += 1
         if count < min_constraints:
            min_constraints = count #'''
            LCV = var
   return LCV
   '''for v in variables:
      if v not in assignment:
         return v # means it hasn't been assigned, simple forward checking'''
   return None
   
def is_complete(variables, assignment, adjacencies):
   for var in variables:
      for adj in adjacencies[var]:
         if adj not in assignment or var not in assignment or assignment[adj] == assignment[var]:
            return False
      if var not in assignment: # if it had no adjs
         return False
   return True


def is_valid(var, value, assignment, adjacencies):
   for adj in adjacencies[var]:
      if adj in assignment and value == assignment[adj]:
         return False # if it wasn't in assignment it's fine
   return True 
       
      
def main():
   edges_file = "edges_liang_d"
   regions_file = "regions_liang_d"
   make_graph(edges_file, regions_file)
   cur_time = time.time()
   print(backtracking_search(adjacencies)) # print solution
   next_time = time.time()
   print(next_time - cur_time)




if __name__ == '__main__':
    main()