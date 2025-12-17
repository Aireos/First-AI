# include <iostream>
#include <list>
using namespace std;

list<int> screen_update( int paddle_position, int ball_position, int ball_velocity, int screen_size) {
    list <int> new_screen(screen_size, 0);
    
    // Update ball position
    ball_position += ball_velocity;
    
    // Check for wall collisions
    if (ball_position <= 0 || ball_position >= screen_size - 1) {
        ball_velocity = -ball_velocity; // Reverse direction
        ball_position += ball_velocity; // Update position after collision
    }
    
    // Check for paddle collision
    if (ball_position == paddle_position) {
        ball_velocity = -ball_velocity; // Reverse direction
        ball_position += ball_velocity; // Update position after collision
    }
    
    // Update screen with ball position
    new_screen[ball_position] = 1; // Represent the ball with '1'
    
    return new_screen;
}