/**
 * MIT License
 * 
 * Copyright (c) 2018 Sigmur
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
**/

/*
* ------------------------------------------------
* 28/09/2018 - servo_driver.ino
* ------------------------------------------------
* External libaries :
* DirectIO - https://github.com/mmarchetti/DirectIO
* ------------------------------------------------
* - Setup arduino as a servomotor handler on its 6 PWM pins (3, 5, 6, 9, 10, 11)
* - For the machine, we need servos just to open/close filters & drop a card, so no rotation data is required
* - To open/close a servo, send a 16bit integer on pin 0 using pin 1 as clock
* - For each active bit, it will open a servo at the corresponding position
* - If more than 6 bits are up uppon reception, the arduino will shift the 6 used bits and send rest to next arduino
* ------------------------------------------------
* - Ex : Receiving 10154
*      - 0010 0111 1010 1010 => binary form
*	   - On this arduino, use 6 first bits : 0010 01
*	   - Open servos at index 3 and 5 (4th and 6th servos)
*      - Shift number to remove those datas : 
*      - 0010 0111 1010 1010 => 1110 1010 1000 0000
*      - Send new number to next arduino
* ------------------------------------------------
*/

#include <DirectIO.h>
#include <Servo.h>

#define ANGLE_CLOSE			0	//Closed at 0° rotation
#define ANGLE_OPEN			60	//Open at 60° rotation
#define SERVO_PIN_1			3
#define SERVO_PIN_2			5
#define SERVO_PIN_3			6
#define SERVO_PIN_4			9
#define SERVO_PIN_5			10
#define SERVO_PIN_6			11

/* Transmission & reception :
	Transmission :
		Begin, get first bit of int16 to send
		Rise/Drop TX, to fit the bit
		Rise clock
		Wait X ms, benchmark to find good value
		Drop clock
		Repeat TRANSMISSION_SIZE - 1 times with next bits
	Reception :
		Begin, no transmission, clock = LOW
		Clock is rising : start reading transmission
			Read RX
		Clock is dropping, wait for next rise
		Clock is rising again and will do TRANSMISSION_SIZE - 1 times
		On each rise, read RX
*/

#define TRANSMISSION_SIZE	16	//16 bit, max 16 servos
#define CLOCK_DELAY			5	//5 ms (TBD)

#define PIN_RX_CLOCK		1	//Reception clock
#define PIN_RX				0	//Reception pin
#define PIN_TX_CLOCK		13	//Transmission clock
#define PIN_TX				12	//Transmission pin

const int servo_angles[2] = {ANGLE_CLOSE, ANGLE_OPEN};
const int servo_pins[6] = {SERVO_PIN_1, SERVO_PIN_2, SERVO_PIN_3, SERVO_PIN_4, SERVO_PIN_5, SERVO_PIN_6};
Servo servos[6];

//Transmission & reception datas
Input<PIN_RX_CLOCK> reception_clock;
Input<PIN_RX> reception;
Output<PIN_TX_CLOCK> transmission_clock;
Output<PIN_TX> transmission;

bool last_state = false;
int8_t reception_index = 0;
int16_t reception_data = 0;

//--------------------------------------------
// Servo update
//--------------------------------------------

void updateServos(int16_t states)
{
	for (int8_t i = 0; i < 6; i++)
		servos[i].write(servo_angles[(states & (1 << 0))];
}

//--------------------------------------------
// I/O
//--------------------------------------------

void send(int16_t data)
{
	if (transmission_clock != LOW)
		return ;
	
	for (int8_t i = 0; i < TRANSMISSION_SIZE; i++)
	{
		transmission = ((data & (1 << i)) == 0) ? LOW : HIGH; //Transmit 1 if current bit is high, 0 if not
		transmission_clock = HIGH; //Set clock to high
		delay(CLOCK_DELAY); //Wait a bit for other side to read data
		transmission_clock = LOW; //Drop the clock for next transmission
	}
}

void listen()
{
	if (last_state == reception_clock || reception_index >= TRANSMISSION_SIZE)
		return ; //Nothing to do

	if (last_state == LOW && reception_clock == HIGH) //New data to read
		reception_data |= 1UL << reception_index++;
	
	last_state = reception_clock; //Update
}

//--------------------------------------------
// Main
//--------------------------------------------

void setup()
{
	//Init servos
	for (int8_t i = 0; i < 6; i++)
	{
		servos[i].attach(servo_pins[i]);
		servos[i].write(ANGLE_CLOSE);
	}
}

void loop()
{
	if (reception_index == TRANSMISSION_SIZE)
	{ //Just finished a reception, can use reception_data to toggle servos
		updateServos(reception_data); //Toggle servos
		if (reception_data >= 64) //Bit 7 active, send to next arduino
			send(reception_data >> 6); //Move 6 bits to the right, 64 become 1 so servo 7 is first of next board
			//https://www.arduino.cc/reference/en/language/structure/bitwise-operators/bitshiftright/
		//Reset reception
		reception_index = 0;
		reception_data = 0;
	}
	
	listen();
}
