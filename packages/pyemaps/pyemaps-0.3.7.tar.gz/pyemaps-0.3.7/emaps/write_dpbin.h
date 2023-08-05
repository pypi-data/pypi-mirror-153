// #define DPAR_MAX2 5000
// #define DPAR_MAX 1500
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <memory.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif
	// All visible library function prototypes go here.
	int dpwritebin(void);
	int dpwritebin_new(const char *, const char *);
	// void setdpheadernums(int *, int *, double *);
	int dpreadbinary(const char *, const char *);
	// __declspec( dllexport ) void setdpheadernums(int *, int *, double *);
	// __declspec( dllexport ) void dpreadbinary(void);
#ifdef __cplusplus
}
#endif
// extern void setdpheadernums(int, int, double);
// extern void setdpheaderuvw(double uvw[4][3]);

// extern void setdpheaderxy(double xy[4][2]);

// extern void setdpheadergmxr(double gmx[3][3], double gmr[3][3]);

// extern int openwritedpbin(void);

// extern int closewritedpbin(void);