import tkinter as tk
from tkinter import font
from tkinter import messagebox
import random

# Inisialisasi jendela utama aplikasi
root = tk.Tk()
root.title("Tic Tac Toe")
root.resizable(False, False)
bold_large_font = font.Font(family="Arial", size=20, weight="bold")
bold_font = font.Font(family="Arial", size=11, weight="bold")

#Variable Global
# Papan permainan Tic Tac Toe disimbolkan dengan list berukuran 9
board = [" " for _ in range(9)]
buttons = []  # Menyimpan tombol-tombol untuk papan Tic Tac Toe
player_turn = "X"  # Menyimpan giliran pemain (X atau O)
mode = tk.StringVar(value="2 Player")  # Variabel untuk menyimpan mode permainan
difficulty = tk.StringVar(value="Easy")  # Variabel untuk menyimpan tingkat kesulitan
player_1_score = 0
player_2_score = 0
ai_score = 0

# Warna
BG_COLOR = "#0D92F4"  # Warna latar belakang
FG_COLOR = "#ffffff"  # Warna teks
BOARD_COLOR = "#d1d1d1"  # Warna board
BUTTON_COLOR = "#FF7F3E" # Warna button
BUTTON_TEXT_COLOR = "#ffffff"  # Warna teks tombol

#root warna
root.configure(bg=BG_COLOR)

def show_welcome_page():
    #Menampilkan halaman selamat datang.
    welcome_frame = tk.Frame(
        root, 
        bg=BG_COLOR
    )
    
    welcome_frame.pack(
        expand=True, 
        fill=tk.BOTH
    )

    # Teks selamat datang
    welcome_label = tk.Label(
        welcome_frame, 
        text="Selamat Datang\nDi Game XOX", 
        font=bold_large_font,
        bg=BG_COLOR, 
        fg=FG_COLOR
    )

    welcome_label.pack(
        padx=20, 
        anchor='center'
    )

    # Informasi kelompok
    welcome_label = tk.Label(
        welcome_frame, 
        text="Kelompok 2", 
        font=bold_large_font,
        fg=BUTTON_TEXT_COLOR,
        bg=BUTTON_COLOR
    )
    
    welcome_label.pack(
        pady=10, 
        anchor='center'
    )

    # Tombol untuk memulai permainan
    start_button = tk.Button(
        welcome_frame, 
        text="Mulai Game",
        font=bold_font, 
        command=lambda: start_game(welcome_frame),
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR,
        width=12
    )

    start_button.pack(pady=75, anchor='center')

def start_game(welcome_frame):
    #Awalan Game Memulai
    welcome_frame.destroy()
    create_game_interface()

def reset_board():
    #Mengatur ulang papan permainan dan giliran pemain ke awal
    global board, player_turn
    board = [" " for _ in range(9)]  # Mengosongkan papan
    player_turn = "X"  # Giliran dimulai dari X
    for button in buttons:
        button.config(
            text=" ", 
            state="normal",
            bg=BOARD_COLOR, 
            fg=BUTTON_TEXT_COLOR
        )  # Reset tampilan tombol

def update_difficulty_options(*args):
    #Menampilkan atau menyembunyikan opsi tingkat kesulitan berdasarkan mode permainan
    if mode.get() == "vs AI":
        difficulty_label.grid(row=1, column=0)
        difficulty_menu.grid(row=1, column=1)
    else:
        difficulty_label.grid_remove()
        difficulty_menu.grid_remove()

def is_winner(player):
    #Mengecek apakah pemain yang diberikan telah memenangkan permainan
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Baris
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Kolom
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    # Cek setiap kondisi menang
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def is_draw():
    #Mengecek apakah permainan berakhir seri (papan penuh tanpa pemenang)
    return " " not in board

def ai_move_easy():
    #Langkah AI tingkat mudah: memilih posisi acak yang tersedia
    available_moves = [i for i, cell in enumerate(board) if cell == " "]
    move = random.choice(available_moves)
    board[move] = "O"
    buttons[move].config(
        text="O",
        fg="white",
        state="disabled"
    )

def ai_move_medium():
    #Langkah AI tingkat menengah: mengecek langkah kemenangan atau pertahanan
    # AI mencoba untuk menang
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if is_winner("O"):
                buttons[i].config(
                    text="O",
                    fg="white", 
                    state="disabled"
                )
                return
            board[i] = " "
    
    # AI mencoba untuk mencegah kemenangan lawan
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if is_winner("X"):
                board[i] = "O"
                buttons[i].config(
                    text="O",
                    fg="white", 
                    state="disabled"
                )
                return
            board[i] = " "

    # Jika tidak ada langkah menang atau blokir, AI memilih langkah acak
    ai_move_easy()

def ai_move_hard():
    #Langkah AI tingkat sulit: memilih langkah terbaik menggunakan Minimax
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"
    buttons[move].config(
        text="O", 
        fg="white",
        state="disabled"
    )

def minimax(board, depth, is_maximizing):
    #Algoritma Minimax untuk menentukan langkah terbaik bagi AI di tingkat sulit
    if is_winner("O"):
        return 1
    elif is_winner("X"):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    #Menentukan langkah AI berdasarkan tingkat kesulitan yang dipilih
    if difficulty.get() == "Easy":
        ai_move_easy()
    elif difficulty.get() == "Medium":
        ai_move_medium()
    else:
        ai_move_hard() == "Hard"

def update_score_display():
    #Untuk update score
    if mode.get() == "2 Player":
        score_label.config(
            font=bold_font,
            text=f"Skor Player 1: {player_1_score} | Player 2: {player_2_score}"
        )
    elif mode.get() == "vs AI":
        score_label.config(
            font=bold_font,
            text=f"Skor Player: {player_1_score} | AI: {ai_score}"
        )

def player_move(index):
    global player_turn, player_1_score, player_2_score, ai_score

    if board[index] == " ":
        # Set the board and disable the button
        board[index] = player_turn
        buttons[index].config(
            text=player_turn,
            fg="white", 
            state="disabled"
        )

        if mode.get() == "2 Player":
            # Mode: 2 Player
            if is_winner(player_turn):
                if player_turn == "X":
                    player_1_score += 1
                else:
                    player_2_score += 1

                update_score_display()
                
                # Cek jika skor mencapai 5
                if player_1_score == 5 or player_2_score == 5:
                    winner = "Player 1" if player_1_score == 5 else "Player 2"
                    messagebox.showinfo("Game Over", f"{winner} Wins the Game!")
                    reset_game()
                    return

                messagebox.showinfo("Tic Tac Toe", f"Player {player_turn} Wins!")
                reset_board()
                return

            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()
                return

        elif mode.get() == "vs AI":
            # Mode: vs AI
            if is_winner(player_turn):
                if player_turn == "X":
                    player_1_score += 1
                    update_score_display()

                    # Cek jika skor Player mencapai 5
                    if player_1_score == 5:
                        messagebox.showinfo("Game Over", "Congratulations! You Win the Game!")
                        reset_game()
                        return

                messagebox.showinfo("Tic Tac Toe", "Player Wins!")
                reset_board()
                return

            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()
                return

        # Switch turn
        player_turn = "O" if player_turn == "X" else "X"

        # AI move if in AI mode
        if mode.get() == "vs AI" and player_turn == "O":
            ai_move()

            # Check if AI wins
            if is_winner("O"):
                ai_score += 1
                update_score_display()

                # Cek jika skor AI mencapai 5
                if ai_score == 5:
                    messagebox.showinfo("Game Over", "AI Wins the Game! Better luck next time!")
                    reset_game()
                    return

                messagebox.showinfo("Tic Tac Toe", "AI Wins!")
                reset_board()
                return

            # Check if it's a draw after AI's move
            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()

            # Switch back to player turn
            player_turn = "X"

def reset_game():
    #Mengatur ulang permainan
    global player_1_score, player_2_score, ai_score
    player_1_score = 0
    player_2_score = 0
    ai_score = 0
    update_score_display()
    reset_board()

def create_game_interface():
    #Membuat antarmuka utama permainan
    global difficulty_label, difficulty_menu, score_label

    tk.Label(
        root, 
        text="Mode      :", 
        bg=BG_COLOR, 
        fg=FG_COLOR,
        font=bold_font
        ).grid(
            row=0, 
            column=0
    )
    
    mode_menu = tk.OptionMenu(
        root, 
        mode, 
        "2 Player", 
        "vs AI"
    )

    mode_menu.config(
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    )

    mode_menu.grid(
        row=0, 
        column=1,
        pady=5
    )

    # Pilihan tingkat kesulitan AI
    difficulty_label = tk.Label(
        root, 
        text="Difficulty :",
        bg=BG_COLOR, 
        fg=FG_COLOR,
        font=bold_font
    )

    difficulty_menu = tk.OptionMenu(
        root, 
        difficulty, 
        "Easy", 
        "Medium", 
        "Hard"
    )

    difficulty_menu.config(
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    )

    difficulty_label.grid(
        row=1, 
        column=0,
        pady=8
    )

    difficulty_menu.grid(
        row=1, 
        column=1
    )

    # Update opsi berdasarkan mode
    mode.trace_add(
        "write", 
        lambda *args: (
            reset_game(), 
            update_difficulty_options()
        )
    )

    update_difficulty_options()

    # Label untuk skor
    score_label = tk.Label(
        root, 
        text=f"Skor Player 1: {player_1_score} | Player 2: {player_2_score}",
        bg=BG_COLOR, 
        fg=FG_COLOR,
        font=bold_font
    )

    score_label.grid(
        row=7, 
        column=0, 
        columnspan=3, 
        pady=10
    )

    # Membuat papan Tic Tac Toe
    for i in range(9):
        button = tk.Button(
            root, 
            text=" ", 
            width=10, 
            height=4,
            command=lambda i=i: player_move(i),
            bg=BOARD_COLOR, 
            fg=BUTTON_TEXT_COLOR
        )

        button.grid(
            row=(i // 3) + 2, 
            column=i % 3,
            padx=3,
            pady=3
        )
        
        buttons.append(button)

    # Tombol reset permainan
    tk.Button(
        root, 
        text="Reset Game", 
        command=reset_game,
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
        ).grid(
            row=60, 
            column=0, 
            columnspan=3,
            pady=4
        )

# Menampilkan halaman selamat datang saat program dimulai
show_welcome_page()

root.mainloop()