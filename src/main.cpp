#include "main.h"
#include "pros/serial.hpp"
#include "pros/apix.h"
#include <cstdio>
#include <string> 

void on_center_button() {
    static bool pressed = false;
    pressed = !pressed;
    if (pressed) {
        pros::lcd::set_text(2, "I was pressed!");
    } else {
        pros::lcd::clear_line(2);
    }
}

void initialize() {
	pros::lcd::initialize();

	pros::c::serctl(SERCTL_DISABLE_COBS, NULL);

	pros::Mutex maplock = pros::Mutex();
}

void disabled() {}
void competition_initialize() {}
void autonomous() {}



void opcontrol() {
	
	std::string a;
	
	

	std::cin >> a;
	
	pros::lcd::set_text(3, a);

	pros::delay(2000);

	for(int i = 65; i <= 100000; ){
		
		
		std::cout << "Creamier Cocks \n";

		std::string thingggggg = std::to_string(i);
		pros::lcd::set_text(4, thingggggg);

		// std::cout << a;

		//std::cin >> a;

		
		
		pros::delay(69);
	}



}