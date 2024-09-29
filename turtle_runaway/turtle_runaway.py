import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # time, score 함수 설정
        self.time = 60
        self.score = 0

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        # 시간
        self.timer_drawer = turtle.RawTurtle(canvas)
        self.timer_drawer.hideturtle()
        self.timer_drawer.penup()

        # 게임 오버
        self.is_gameover = False
        self.game_over_drawer = turtle.RawTurtle(canvas)
        self.game_over_drawer.hideturtle()
        self.game_over_drawer.penup()
        

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=10):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        # renew_time() 함수 실행문 추가
        self.renew_time()
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)


    def step(self):
        # runner 거북이가 선 밖으로 나가지 못하게 수정.
        if self.runner.xcor() > 350 or self.runner.xcor() < -350:
            self.runner.right(180)
            self.runner.forward(10)
        if self.runner.ycor() > 350 or self.runner.ycor() < -350:
            self.runner.right(180)
            self.runner.forward(10)

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-280, 280)
        # 잡으면 점수를 획득하고 runner가 좌표상 대칭방향으로 도망감 
        if is_catched and not(self.is_gameover): # gameover시 점수 오름 방지.
            self.runner.setpos(-self.runner.xcor(), -self.runner.ycor())
            self.score += 100
        self.drawer.write(f'Is catched? {is_catched}\nScore: {self.score}', font=("System", 15, "bold"))
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)
    
    # 타이머 계산 및 시각화
    def renew_time(self):
        self.timer_drawer.undo()
        self.timer_drawer.penup()
        self.timer_drawer.setpos(200,280)
        self.timer_drawer.write(f'Time: {self.time}', font=("System", 20, "bold"))
        if self.time > 0:
            self.time -= 1
            self.canvas.ontimer(self.renew_time, 1000)
        else:
            self.game_over()
        
    
    # game over시 실행 함수
    def game_over(self):
        self.is_gameover = True
        self.game_over_drawer.penup()
        self.game_over_drawer.setpos(0,0)
        self.game_over_drawer.write('Game Over', align="center", font=("System", 30, "bold"))

    
class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
        
        

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title("Turtle Runaway")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("#5FC7D7")

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
    