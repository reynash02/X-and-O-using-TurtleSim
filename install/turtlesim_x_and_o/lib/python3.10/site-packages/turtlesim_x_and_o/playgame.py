import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute,SetPen
import math

class XandOGame(Node):
    def __init__(self):
        super().__init__('playgame')
        self.board=[['' for _ in range(3)]for _ in range(3)]
        self.player='X'
        self.teleport=self.create_client(TeleportAbsolute,'turtle1/teleport_absolute')
        self.setpen=self.create_client(SetPen,'turtle1/set_pen')
        while not self.teleport.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Teleport Absolute Service')
        while not self.setpen.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Set Pen Service')

    def teleport_turtle(self,x,y,theta=0.0):
        req=TeleportAbsolute.Request()
        req.x=float(x)
        req.y=float(y)
        req.theta=float(theta)
        future=self.teleport.call_async(req)
        rclpy.spin_until_future_complete(self,future)
        self.get_logger().info(f'Teleporting turtle to ({x}, {y})')
        
    def set_pen(self,r,g,b,width,off):
        req=SetPen.Request()
        req.r=r
        req.g=g
        req.b=b
        req.width=width
        req.off=off
        future=self.setpen.call_async(req)
        rclpy.spin_until_future_complete(self,future)
        self.get_logger().info(f'Setting pen color to ({r}, {g}, {b}), width={width}, pen {"off" if off else "on"}')
    
    def columns(self,x):
        self.set_pen(0,0,0,2,1)
        self.teleport_turtle(x,11)
        self.set_pen(0,0,0,2,0)
        self.teleport_turtle(x,0)
        self.set_pen(0,0,0,2,1)
    
    def rows(self,y):
        self.teleport_turtle(0,y)
        self.set_pen(0,0,0,2,0)
        self.teleport_turtle(11,y)
        self.set_pen(0,0,0,2,1)

    def draw_x(self,x,y):
        self.set_pen(0,0,0,2,1)
        self.teleport_turtle(x,y)
        self.set_pen(255,0,0,2,0)
        self.teleport_turtle(x-0.5,y-0.5)
        self.teleport_turtle(x+0.5,y+0.5)
        self.set_pen(255,0,0,2,1)
        self.teleport_turtle(x-0.5,y+0.5)
        self.set_pen(255,0,0,2,0)
        self.teleport_turtle(x+0.5,y-0.5)
        self.set_pen(0,0,0,2,1)

    def draw_o(self,x,y):
        self.set_pen(0,0,0,2,1)
        self.teleport_turtle(x,y)
        x0=x+0.5*math.cos(0)
        y0=y+0.5*math.sin(0)
        self.set_pen(255,255,255,2,1)
        self.teleport_turtle(x0,y0)
        self.set_pen(255,255,255,2,0)
        for angle in range(0,360,10):
            rad=math.radians(angle)
            x1=x+0.5*math.cos(rad)
            y1=y+0.5*math.sin(rad)
            self.teleport_turtle(x1,y1)
        self.set_pen(0,0,255,2,1)
    
    def get_turtle_coordinates(self,row,col):
        x=col*3.66+1.83
        y=11-(row*3.66+1.83)
        return x,y

    def make_move(self,row,col):
        if self.board[row][col]=='':
            self.board[row][col]=self.player
            x,y=self.get_turtle_coordinates(row,col)
            if self.player=='X':
                self.draw_x(x,y)
            else:
                self.draw_o(x,y)
        else:
            self.get_logger().info("Move is invalid. Try again")
    
    def switch_player(self):
        if self.player=='X':
            self.player='O'
        else:
            self.player='X'
    
    def check_win(self):
        for row in self.board:
            if row[0]==row[1]==row[2]!='':
                return True
        for col in range(3):
            if self.board[0][col]==self.board[1][col]==self.board[2][col]!='':
                return True
        if self.board[2][0]==self.board[1][1]==self.board[0][2]!='':
            return True
        if self.board[0][0]==self.board[1][1]==self.board[2][2]!='':
            return True
        return False

    def check_draw(self):
        for row in self.board:
            if '' in row:  # If there is an empty cell, it's not a draw
                return False
        return True  # No empty cells left, so it's a draw
    
    def play_game(self):
        while rclpy.ok():
            row=int(input('Enter row (0,1,2)='))
            col=int(input('Enter column (0,1,2)='))
            self.make_move(row,col)
            if self.check_win():
                print(f"Player {self.player} wins")
                break
            elif self.check_draw():
                print ("Its a draw")
                break
            self.switch_player()

def main(args=None):
    rclpy.init(args=args)
    node=XandOGame()
    node.columns(3.66)
    node.columns(7.32)
    node.rows(3.66)
    node.rows(7.32)
    node.play_game()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()
        
