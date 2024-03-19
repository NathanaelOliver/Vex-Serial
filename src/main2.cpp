#include "main.h"
#include "pros/serial.hpp"
#include "pros/apix.h"
#include <cstdio>
#include <string> 
#include <cmath>

int count = 0;

void snap_photo() {
	std::cout << "snapshot\n";
	count += 1;
	pros::lcd::set_text(1, "photo count: " + std::to_string(count));
}

void exit() {
	std::cout << "exit\n";
}

void initialize() {
	pros::lcd::initialize();
	pros::lcd::register_btn1_cb(snap_photo);
	pros::lcd::register_btn2_cb(exit);
	pros::c::serctl(SERCTL_DISABLE_COBS, NULL);
	pros::Mutex maplock = pros::Mutex();
	
}

void disabled() {}

void competition_initialize() {}

void autonomous() {}



void opcontrol() {
	while (true) {
		pros::delay(10);
	}
}
