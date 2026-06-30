# Bind Spacebar
win.listen()
win.onkeypress(flap, "space")

reset_pipe()

# Main Engine Loop
while True:
    win.update()
    time.sleep(0.01) # Frame timing cap

    # Move Bird
    bird_speed += gravity
    bird.sety(bird.ycor() + bird_speed)

    # Move Pipes
    top_pipe.setx(top_pipe.xcor() - 3)
    bottom_pipe.setx(bottom_pipe.xcor() - 3)

    # Reset pipes when off screen & award points
    if top_pipe.xcor() < -220:
        reset_pipe()
        score += 1
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))

    # Boundary Floor / Ceiling Collision
    if bird.ycor() < -240 or bird.ycor() > 240:
        break

    # Pipe Solid Boundary Box Checking
    if top_pipe.xcor() - 35 < bird.xcor() < top_pipe.xcor() + 35:
        if bird.ycor() > top_pipe.ycor() - 150 or bird.ycor() < bottom_pipe.ycor() + 150:
            break

# End of Game Loop State
pen.goto(0, 0)
pen.write("GAME OVER", align="center", font=("Arial", 30, "bold"))
win.mainloop()
