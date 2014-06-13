#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>
#include <cmath>

#include <sys/stat.h>

#include "PrimaryBeam.h"
#include "DataIO.h"
#include "definitions.h"

#ifndef __COORDS_H__
#define __COORDS_H__

using std::vector;
using std::ifstream;
using std::stringstream;
using std::sin;
using std::asin;
using std::cos;
using std::cerr;
using std::cout;
using std::endl;

#define pi M_PI

class Coords
{
private:
	struct stat statbuffer;
public:
	Coords(const char* coordfile);
	Coords(double* x, double* y, double* weight, int nstack);
	~Coords();
	void computeCoords(DataIO* ms, PrimaryBeam& pb);

public:
	int nPointings;
	float** omega_x;
	float** omega_y;
	float** omega_z;
	float** dx;
	float** dy;
	double* x_raw;
	double* y_raw;
	double* weight_raw;
	int nStackPoints_raw;
	float** x;
	float** y;
	float** weight;
	int* nStackPoints;
	int nStackPointsVisible;
};

#endif
