import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Game")
        self.root.geometry("500x570")
        self.root.configure(bg='#f0f0f0')

        self.board = []
        self.empty_pos = (2, 2)
        self.moves = 0
        self.image_pieces = []
        

        if not os.path.exists('puzzle_images'):
            os.makedirs('puzzle_images')

        self.create_widgets()
        self.load_and_split_image()
##############################################################
    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="8-Puzzle", 
                                  font=("Arial", 24, "bold"),
                                  bg='#f0f0f0',
                                  fg='#2c3e50')
        self.title_label.pack(pady=10)
        
        self.moves_label = tk.Label(self.root, text="Number of movements: 0", 
                                  font=("Arial", 14),
                                  bg='#f0f0f0',
                                  fg='#34495e')
        self.moves_label.pack(pady=5)
       
        self.game_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.game_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.game_frame, 
                                 compound='center',
                                 relief='solid',
                                 borderwidth=0,
                                 command=lambda x=i, y=j: self.move_tile(x, y))
                button.grid(row=i, column=j, padx=0, pady=0)
                row.append(button)
            self.buttons.append(row)
        
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        top_row = tk.Frame(buttons_frame, bg='#f0f0f0')
        top_row.pack(fill='x')
        
        self.new_image_button = tk.Button(top_row, 
                                        text="Choose New Image", 
                                        command=self.choose_new_image, 
                                        font=("Arial", 12, "bold"),
                                        bg='#3498db',
                                        fg='white',
                                        activebackground='#2980b9',
                                        width=15,
                                        height=2,
                                        relief='flat')
        self.new_image_button.pack(side='left', expand=True, fill='x', padx=1)
        
        self.show_image_button = tk.Button(top_row, 
                                        text="Show Original Image", 
                                        command=self.show_original_image, 
                                        font=("Arial", 12, "bold"),
                                        bg='#9b59b6',
                                        fg='white',
                                        activebackground='#8e44ad',
                                        width=15,
                                        height=2,
                                        relief='flat')
        self.show_image_button.pack(side='left', expand=True, fill='x', padx=1)
        
        self.reset_button = tk.Button(top_row, 
                                    text="Reset Game", 
                                    command=self.reset_game, 
                                    font=("Arial", 12, "bold"),
                                    bg='#2ecc71',
                                    fg='white',
                                    activebackground='#27ae60',
                                    width=15,
                                    height=2,
                                    relief='flat')
        self.reset_button.pack(side='left', expand=True, fill='x', padx=1)
        
        bottom_row = tk.Frame(buttons_frame, bg='#f0f0f0')
        bottom_row.pack(fill='x', pady=1)
        
        self.solve_button = tk.Button(bottom_row, 
                                    text="Auto Solve (DFS)", 
                                    command=lambda: self.solve_puzzle('dfs'), 
                                    font=("Arial", 12, "bold"),
                                    bg='#e74c3c',
                                    fg='white',
                                    activebackground='#c0392b',
                                    width=15,
                                    height=2,
                                    relief='flat')
        self.solve_button.pack(side='left', expand=True, fill='x', padx=1)
        
        self.bfs_button = tk.Button(bottom_row, 
                                    text="Auto Solve (BFS)", 
                                    command=lambda: self.solve_puzzle('bfs'), 
                                    font=("Arial", 12, "bold"),
                                    bg='#f39c12',
                                    fg='white',
                                    activebackground='#d35400',
                                    width=15,
                                    height=2,
                                    relief='flat')
        self.bfs_button.pack(side='left', expand=True, fill='x', padx=1)
##############################################################
    def load_and_split_image(self, image_path=None):
        if image_path is None:
            image_path = 'puzzle_images/default.jpg'
            if not os.path.exists(image_path):
                messagebox.showinfo("Notice", "Please place an image named 'default.jpg' in the puzzle_images folder")
                return
        
        self.current_image_path = image_path
            
        image = Image.open(image_path)
        image = image.resize((300, 300))
            
        piece_width = image.width / 3
        piece_height = image.height / 3
            
        self.image_pieces = []
        for i in range(3):
            for j in range(3):
                left = j * piece_width
                top = i * piece_height
                right = left + piece_width
                bottom = top + piece_height
                
                piece = image.crop((left, top, right, bottom))
                photo = ImageTk.PhotoImage(piece)
                self.image_pieces.append(photo)

        self.board_space()
##############################################################
    def board_space(self):
        while True:
            numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            random.shuffle(numbers)
            self.board = []
            for i in range(3):
                row = []
                for j in range(3):
                    num = numbers[i*3 + j]
                    row.append(num)
                    if num == 8:
                        self.empty_pos = (i, j)
                        self.buttons[i][j].config(image="", bg='#ecf0f1')
                    else:
                        self.buttons[i][j].config(image=self.image_pieces[num], bg='white')
                self.board.append(row)
            if self.is_solvable():
                break
##############################################################
    def move_tile(self, row, col):
        if (abs(row - self.empty_pos[0]) == 1 and col == self.empty_pos[1]) or \
           (abs(col - self.empty_pos[1]) == 1 and row == self.empty_pos[0]):
            
            self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[row][col]
            self.board[row][col] = 8
            
            if self.board[self.empty_pos[0]][self.empty_pos[1]] != 8:
                self.buttons[self.empty_pos[0]][self.empty_pos[1]].config(
                    image=self.image_pieces[self.board[self.empty_pos[0]][self.empty_pos[1]]],
                    bg='white')
            else:
                self.buttons[self.empty_pos[0]][self.empty_pos[1]].config(
                    image="",
                    bg='#ecf0f1')
            
            self.buttons[row][col].config(image="", bg='#ecf0f1')
            self.empty_pos = (row, col)
            
            self.moves += 1
            self.moves_label.config(text=f"Number of movements: {self.moves}")
            
            if self.check_win():
                messagebox.showinfo("Congratulations!", f"You won! Number of movements: {self.moves}")
                self.reset_game()
##############################################################
    def check_win(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != i*3 + j:
                    return False
        return True
##############################################################
    def reset_game(self):
        self.moves = 0
        self.moves_label.config(text="Number of movements: 0")
        self.board_space()
##############################################################
    def choose_new_image(self):
        
        file_path = filedialog.askopenfilename(
            title="Choose Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.load_and_split_image(file_path)
            self.moves = 0
            self.moves_label.config(text="Number of movements: 0")
##############################################################
    def show_original_image(self):
        if (self.current_image_path):
            preview_window = tk.Toplevel()
            preview_window.title("Original Image")
            image = Image.open(self.current_image_path)
            image = image.resize((400, 400))
            photo = ImageTk.PhotoImage(image)
            preview_window.photo = photo
            label = tk.Label(preview_window, image=photo)
            label.pack(padx=10, pady=10)
##############################################################
    def get_board_state(self):
        state = []
        for row in self.board:
            state.extend(row)
        return tuple(state)
##############################################################
    def get_possible_moves(self, empty_pos):
        moves = []
        row, col = empty_pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                moves.append((new_row, new_col))
        return moves
##############################################################
    def make_move(self, from_pos, to_pos):
        new_board = []
        for row in self.board:
            new_board.append(row[:])
            
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        new_board[from_row][from_col], new_board[to_row][to_col] = \
        new_board[to_row][to_col], new_board[from_row][from_col]
        
        return new_board
##############################################################
    def is_goal_state(self, board):
        goal = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(i*3 + j)
            goal.append(row)
        
        for i in range(3):
            for j in range(3):
                if isinstance(board, tuple):
                    if board[i*3 + j] != goal[i][j]:
                        return False
                else:
                    if board[i][j] != goal[i][j]:
                        return False
        return True
##############################################################
    def manhattan_distance(self, state):
        distance = 0
        board = [list(state[i:i+3]) for i in range(0, 9, 3)]
        
        for i in range(3):
            for j in range(3):
                if board[i][j] != 8:
                    target_row = board[i][j] // 3
                    target_col = board[i][j] % 3
                    distance += abs(target_row - i) + abs(target_col - j)
        return distance
##############################################################
    def dfs_solve(self):
        start_state = self.get_board_state()
        stack = [(self.manhattan_distance(start_state), start_state, self.empty_pos, [])]
        visited = {start_state}
        
        max_depth = 50
        steps = 0
        
        print("بدء البحث عن الحل...")
        
        while stack:
            _, current_state, empty_pos, path = stack.pop()
            steps += 1
            
            if len(path) > max_depth:
                continue
            
            if self.is_goal_state(current_state):
                print(f"تم إيجاد الحل! عدد الخطوات: {len(path)}")
                return path
            
            possible_moves = self.get_possible_moves(empty_pos)
            moves_with_scores = []
            
            for move in possible_moves:
                current_board = [list(current_state[i:i+3]) for i in range(0, 9, 3)]
                move_row, move_col = move
                empty_row, empty_col = empty_pos
                
                current_board[empty_row][empty_col] = current_board[move_row][move_col]
                current_board[move_row][move_col] = 8
                
                new_state = tuple(item for row in current_board for item in row)
                
                if new_state not in visited:
                    score = self.manhattan_distance(new_state)
                    moves_with_scores.append((score, move, new_state))
            
            moves_with_scores.sort()
            
            for score, move, new_state in reversed(moves_with_scores):
                if new_state not in visited:
                    visited.add(new_state)
                    new_path = path + [(empty_pos, move)]
                    stack.append((score, new_state, move, new_path))
        
        print(f"لم يتم العثور على حل بعد {steps} محاولة!")
        return None
##############################################################
    def bfs_solve(self):
        start_state = self.get_board_state()
        queue = [(start_state, self.empty_pos, [])]
        visited = {start_state}
        
        while queue:
            current_state, empty_pos, path = queue.pop(0)
            
            if self.is_goal_state(current_state):
                return path
            
            possible_moves = self.get_possible_moves(empty_pos)
            
            for move in possible_moves:
                current_board = [list(current_state[i:i+3]) for i in range(0, 9, 3)]
                move_row, move_col = move
                empty_row, empty_col = empty_pos
                
                # تنفيذ الحركة
                current_board[empty_row][empty_col] = current_board[move_row][move_col]
                current_board[move_row][move_col] = 8
                
                new_state = tuple(item for row in current_board for item in row)
                
                if new_state not in visited:
                    visited.add(new_state)
                    new_path = path + [(empty_pos, move)]
                    queue.append((new_state, move, new_path))
        
        return None
##############################################################
    def is_solvable(self):
        flat_board = [num for row in self.board for num in row]
        inv_count = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if flat_board[i] != 8 and flat_board[j] != 8 and flat_board[i] > flat_board[j]:
                    inv_count += 1
        return inv_count % 2 == 0
##############################################################
    def solve_puzzle(self, algorithm='dfs'):
        print("Current board state:")
        for row in self.board:
            print(row)
        print(f"Empty position: {self.empty_pos}")
        
        if not self.is_solvable():
            print("Puzzle is not solvable!")
            messagebox.showinfo("Notice", "This state is not solvable!")
            return
        
        print(f"Puzzle is solvable, searching using {algorithm.upper()}...")
        
        if algorithm == 'dfs':
            solution = self.dfs_solve()
        elif algorithm == 'bfs':
            solution = self.bfs_solve()
        else:
            messagebox.showerror("Error", "Unknown algorithm!")
            return
        
        if solution:
            messagebox.showinfo("Solution Found", f"Solution found with {len(solution)} moves")
            self.animate_solution(solution)
        else:
            messagebox.showinfo("No Solution", "No solution found")
##############################################################
    def animate_solution(self, solution):
        if not solution:
            return
        
        def execute_move(moves, index):
            if index < len(moves):
                from_pos, to_pos = moves[index]
                self.move_tile(to_pos[0], to_pos[1])
                self.root.after(500, execute_move, moves, index + 1)
        
        execute_move(solution, 0)

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop() 