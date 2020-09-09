import pygame
import math
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class spot:
	def __init__(self,row,col,size,n_rows):
		self.row=row;
		self.col=col;
		self.x=size*row;
		self.y=size*col;
		self.size=size;
		self.n_rows=n_rows;
		self.color=WHITE;

	def draw_rect(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.size,self.size))

	def make_start(self):
		self.color=ORANGE;

	def make_end(self):
		self.color=TURQUOISE;

	def make_wall(self):
		self.color=BLACK;

	def reset(self):
		self.color=WHITE;

	def get_pos(self):
		return self.row,self.col;

	def make_closed(self):
		self.color=RED;

	def __lt__(self, other):
		return False

	def make_neighbour(self):
		self.color=PURPLE

	def make_path(self):
		self.color=GREEN


def make_grid(width,n_rows):
	size= width // n_rows;
	grid=[];
	for i in range(n_rows):
		grid.append([])
		for j in range(n_rows):
			temp=spot(i,j,size,n_rows)
			grid[i].append(temp);
	return grid;

def draw_grid(win,grid,n_rows,width):
	size= width//n_rows;
	for i in range(n_rows):
		pygame.draw.line(win,GREY,(0,i*size),(width,i*size));
		pygame.draw.line(win,GREY,(i*size,0),(i*size,width));

def draw_board(win,width,grid,n_rows):
	win.fill(WHITE);
	for row in grid:
		for obj in row:
			obj.draw_rect(win);
	##pygame.draw.rect(win,RED,(384,384,16,16))
	draw_grid(win,grid,n_rows,width);
	pygame.display.update()

def spotpos(pos,width,n_rows):
	size=width//n_rows;
	x,y =pos;

	row=x//size;
	col=y//size;

	return row,col;


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def issafe(row,col,grid,n_rows):
	if((0<=row) and (row<n_rows) and (col>=0) and (col<n_rows) and grid[row][col].color!=BLACK):
		return True
		return False

def drawsp(draw,came_from,end):
	temp=end;
	while temp in came_from:
		temp.make_path();
		temp=came_from[temp];
		draw();

def algorithm(draw,start,end,grid,n_rows):
	pq=PriorityQueue()
	pq.put((0,start))
	g_score={obj:float("inf") for row in grid for obj in row}
	g_score[start]=0
	f_score={obj:float("inf") for row in grid for obj in row}
	f_score[start]=h(start.get_pos(),end.get_pos());
	came_from={}

	while not pq.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.QUIT

		temp=pq.get()[1];

		if(temp==end):
			drawsp(draw,came_from,end);
			end.make_end();
			return True



		neighbours=[[1,0],[-1,0],[0,1],[0,-1]]
		row,col=temp.get_pos();
		for nb in neighbours:
			if(issafe(row+nb[0],col+nb[1],grid,n_rows)):
				temp_g=g_score[temp]+1
				cnb=grid[row+nb[0]][col+nb[1]]
				if(g_score[cnb]>temp_g):
					g_score[cnb]=temp_g
					f_score[cnb]=temp_g+h(cnb.get_pos(),end.get_pos())
					came_from[cnb]=temp;
					pq.put((f_score[cnb],cnb))
					cnb.make_neighbour();
					
		draw();

		if(temp!=start):
			temp.make_closed();

		



def main():
	width = 800
	win = pygame.display.set_mode((width, width))
	pygame.display.set_caption("Path Finding Visualization")

	n_rows=50;
	grid=make_grid(width,n_rows);

	start=None;
	end=None;
	run=True;
	while(run):
		draw_board(win,width,grid,n_rows)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:
				pos=pygame.mouse.get_pos()
				row,col=spotpos(pos,width,n_rows);
				temp=grid[row][col];
				if not start and temp!=end:
					start=temp;
					temp.make_start();
				elif not end and temp!=start:
					end=temp;
					temp.make_end();

				elif temp!=start and temp!=end:
					temp.make_wall();

			elif pygame.mouse.get_pressed()[2]:
				pos=pygame.mouse.get_pos()
				row,col=spotpos(pos,width,n_rows);
				temp=grid[row][col];
				temp.reset();
				if temp==start:
					start=None

				elif temp==end:
					end=None;



			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_r:
					algorithm(lambda:draw_board(win,width,grid,n_rows),start,end,grid,n_rows)

				elif event.key==pygame.K_c:
					start=None
					end=None
					grid=make_grid(width,n_rows);


	pygame.QUIT;

main()



