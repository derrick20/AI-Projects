# Derrick Liang 10/9/18

class Board():

   def __init__(self):
      self.size = 6 # could change this later
      self.pieces = []    

   def add(self, piece):
      self.pieces.append(piece)
   # piece = (row, col, orientation, length)   

   def pop(self):
      # Your code goes here
      return (0, '')
  
   def __str__(self):
      grid = [6][6]
      for i in range(pieces):
         p = pieces[i]
         row = p[0]
         col = p[1]
         if p[2] == 'h':
            for c in range(col, col + length): # pieces[1] is the column, where you keep placing for how long the length is
               grid[row][c] = i # set that position to a certain index to signify one block type
         elif p[2] == 'v':
            for r in range(row, row + length): # pieces[1] is the column, where you keep placing for how long the length is
               grid[r][col] = i
      print(grid)

def main():
   b = Board()
   b.add( (2, 0, 'v', 3) )
   print(b) 
      
if __name__ == '__main__':
   main()