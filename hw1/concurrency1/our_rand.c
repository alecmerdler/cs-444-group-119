/*
 * Modified from rdrand_test.c provided on class website
 */

#include <stdio.h>
#include <time.h>
#include "mt19937ar.h"

int our_rand(int min, int max)
{
	unsigned int eax;
	unsigned int ebx;
	unsigned int ecx;
	unsigned int edx;

	int r;

	char vendor[13];

	eax = 0x01;

	__asm__ __volatile__(
	                     "cpuid;"
	                     : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx)
	                     : "a"(eax)
	                     );

	if(ecx & 0x40000000){
		//use rdrand
		printf("using rdrand: \n");
		unsigned int tmp = 0;
		__asm__ __volatile__(
				     "rdrand %0;"
				     : "=r" (tmp)
				     );
		r = tmp % (max - min + 1) + min;

	}
	else{
		//use mt19937
		printf("using mt19937\n");
		unsigned long s = time(NULL);
		init_genrand(s);
		r = (genrand_int32() % (max - min + 1)) + min;
	}

	return r;
}
