#include "main.h"
#include "pros/serial.hpp"
#include "pros/apix.h"
#include <cstdio>
#include <string> 


void initialize() {
	pros::c::serctl(SERCTL_DISABLE_COBS, NULL);
	pros::Mutex maplock = pros::Mutex();
	pros::delay(3000);
}

void disabled() {}
void competition_initialize() {}
void autonomous() {}



void opcontrol() {

	


	while (true) {
		std::cout << "Go Cocks \n";
		pros::delay(10);
	}



}

