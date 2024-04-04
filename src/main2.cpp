#include "main.h"
#include "pros/serial.hpp"
#include "pros/apix.h"
#include <cstdio>
#include <cmath>
#include "pros/llemu.hpp"
#include "pros/misc.h"
#include "pros/motors.h"
#include "pros/rotation.hpp"
#include "pros/rtos.hpp"
#include <string>

#define BLW_PORT 13
#define MLW_PORT 14
#define FLW_PORT 15
#define BRW_PORT 16
#define MRW_PORT 17
#define FRW_PORT 18

#define RIK_PORT 3
#define LIK_PORT 4
#define IDX_PORT 5
#define TFW_PORT 6
#define BFW_PORT 7
#define RTW_PORT 8
#define MTW_PORT 9
#define LTW_PORT 10

#define RWG_PORT 7
#define LWG_PORT 8





pros::Controller controller(pros::E_CONTROLLER_MASTER);


pros::Motor BLW (BLW_PORT, true);
pros::Motor MLW (MLW_PORT, true);
pros::Motor FLW (FLW_PORT, true);
pros::Motor BRW (BRW_PORT);
pros::Motor MRW (MRW_PORT);
pros::Motor FRW (FRW_PORT);
pros::Motor RIK (RIK_PORT, true);
pros::Motor LIK (LIK_PORT);
pros::Motor IDX (IDX_PORT);
pros::Motor TFW (TFW_PORT);
pros::Motor BFW (BFW_PORT, true);

pros::Rotation RTW (RTW_PORT);
pros::Rotation MTW (MTW_PORT, true);
pros::Rotation LTW (LTW_PORT);

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
	double left_x, left_y, right_x;
	while (true) {
		left_x = controller.get_analog(ANALOG_LEFT_X);
		left_x = fabs(left_x) > 20 ? left_x : 0;
		left_y = controller.get_analog(ANALOG_LEFT_Y);
		left_y = fabs(left_y) > 20 ? left_y : 0;
		right_x = controller.get_analog(ANALOG_RIGHT_X);
		right_x = fabs(right_x) > 20 ? right_x : 0;

		FRW = left_y - left_x - right_x;
		FLW = left_y + left_x + right_x;
		MRW = left_y - right_x;
		BLW = left_y - left_x + right_x;
		BRW = left_y + left_x - right_x;
		MLW = left_y + right_x;


		if (controller.get_digital_new_press(DIGITAL_A)) {
			snap_photo();
		}

		pros::delay(10);
	}
}
