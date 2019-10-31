import turtle
import math
import random
import os

#setup the screen
window = turtle.Screen()
window.setup(800,800)
window.bgcolor("black")
window.bgpic("gifs/space-bg.gif")
window.title("Space Invaders")
window.addshape("gifs/invader.gif")
window.addshape("gifs/player.gif")


#draw borders
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("black")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#set the score to 0
score = 0

#draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,270)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left" ,font=("Arial",14,"normal"))
score_pen.hideturtle()



#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("gifs/player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15
enemyspeed = 5

#choose a number of enemies
number_of_enemies = 6
#create an empty list of enemies
enemies = []
#add enemies to list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("gifs/invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200,200) #enemies spawn randomly
    y = random.randint(100,250)
    enemy.setposition(x,y)

#create our bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

#define bullet state
#ready -> ready to fire
#fire -> bullet firing
bulletstate = "ready"
bulletspeed = 35


#Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    os.system("mpg123 laser.mp3&")
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor()+10
        bullet.setposition(x,y)
        bullet.showturtle()

def iscollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 25:
        return True
    else:
        return False

def enemySpeedUp():
    global enemyspeed
    enemyspeed += 5

def enemySpeedDown():
    global enemyspeed
    enemyspeed -= 5


#create keyboard actions
turtle.listen()
turtle.onkey(move_left,"Left")
turtle.onkey(move_right,"Right")
turtle.onkey(fire_bullet,"space")

#main game loop
while True:
    for enemy in enemies:
        #moving enemies
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #move the enemy back and down
        if enemy.xcor() > 280:
            #move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1
        if(enemy.ycor() <= -300):
            enemy.hideturtle()
            enemy.penup()
            x = random.randint(-200,200)
            y = random.randint(100,250)
            enemy.setposition(x,y)

        #disappear when reach bottom limit
        if(enemy.xcor() <= -300):
            enemy.hideturtle()


        #check if bullet touch the enemy
        if iscollision(bullet,enemy):
            os.system("mpg123 explosion.mp3&")
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-400)
            #reset the enemy
            x = random.randint(-200,200)
            y = random.randint(100,250)
            enemy.setposition(x,y)
            #update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left" ,font=("Arial",14,"normal"))
            enemyspeed = 5 + score/60
            bulletspeed = 35 + score/20


        #check if enemy catch us (we loose)
        if iscollision(player,enemy):
            player.hideturtle()
            enemy.hideturtle()
            print ("GAME OVER")
            window.clear()
            exit()

    #move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #check if bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
