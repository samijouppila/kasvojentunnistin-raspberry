// Initialize a pins to perform Serial Communication for receive
// the result of the printf on PC (USB Virtual Com)
// I suggest to use TeraTerm on PC.
// TeraTerm configuration must be: 9600-8-N-1 FlowControl None
 
/* EXAMPLE */
#include "mbed.h"
#include "hcsr04.h"
 
//D12 TRIGGER D11 ECHO
Serial pc(USBTX,USBRX);


	
	
	


HCSR04 sensor(D12, D11); 
int main() 
{
    while(1) 
    {
 
		long distance = sensor.distance(); 

		if(distance < 60) {
			pc.printf("1");
		
	}
	
		else {
			pc.printf("0");
	}
	
	wait(0.2);
		
	 

    }
}