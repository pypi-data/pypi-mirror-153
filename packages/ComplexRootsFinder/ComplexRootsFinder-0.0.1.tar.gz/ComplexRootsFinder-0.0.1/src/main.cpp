#include <iostream>
#include <cmath>
#include <complex>
#include <vector>
#include "fparser.hh"
#define _USE_MATH_DEFINES

const double pi = 4 * atan(1), dt = 0.005;
FunctionParser_cd fp;

int curves_order(double x0, double y0, double a)
{
	double angle_temp, sum = 0, p;
	std::complex<double>z, f, temp;
	for (double t = dt; t < 2 * pi; t += dt) {
		p = std::max(abs(cos(t)), abs(sin(t)));
		z = { x0 + a * cos(t) / p, y0 + a * sin(t) / p };
		f = fp.Eval(&z);
		angle_temp = abs(std::arg(f) - std::arg(temp));
		if (angle_temp > pi) {
			angle_temp = 2 * pi - angle_temp;
		}
		if (temp.imag() * f.real() > temp.real() * f.imag()) {
			angle_temp *= -1;
		}
		sum += angle_temp;
		temp = f;
	}
	return round(sum / (2 * pi));
}

void FindRoots(double a, double eps, double x0, double y0, std::vector<std::complex<double>> &roots)
{
	double sum = 0;
	if (curves_order(x0, y0, a) >= 1)
	{
		if (a < eps)
		{
			bool is_find = false;
			for (auto el : roots)
			{
				if (fabsl(real(el) - x0) <= 2 * eps && fabsl(imag(el) - y0) <= 2 * eps)
				{
					is_find = true;
					break;
				}
			}
			if (!is_find)
				roots.emplace_back(round(x0 / eps) * eps, round(y0 / eps) * eps);
		}
		else
		{
			FindRoots(a / 2 + eps / 4, eps, x0 + a / 2, y0 + a / 2, roots);
			FindRoots(a / 2 + eps / 4, eps, x0 + a / 2, y0 - a / 2, roots);
			FindRoots(a / 2 + eps / 4, eps, x0 - a / 2, y0 + a / 2, roots);
			FindRoots(a / 2 + eps / 4, eps, x0 - a / 2, y0 - a / 2, roots);
		}
	}
}

std::vector<std::complex<double>> find_complex_roots(std::string function, double r, double x0, double y0, double eps)
{
	fp.Parse(function, "z");
	std::complex<double>z = { x0, y0 };
	std::vector<std::complex<double>> roots;
	FindRoots(r, eps, x0, y0, roots);
	return roots;
}

// int main()
// {
// 	setlocale(LC_ALL, "Russian");
// 	double r, x0, y0, eps;
// 	std::string function;
// 	std::cout << "Радиус ";
// 	std::cin >> r;
// 	std::cout <<"Начальная координата ";
// 	std::cin >> x0 >> y0;
// 	std::cout << "Точность ";
// 	std::cin >> eps;
// 	std::cout << "Функция F(z) = ";
// 	std::cin >> function;
// 	std::vector<std::complex<double>> roots = find_complex_roots(function, r, x0, y0, eps);
// 	for (int i = 0; i < roots.size(); i++) {
// 		std::cout << roots[i]<<std::endl;
// 	}
// 	return 0;
// }

#ifndef _DEBUG
	
	// Needed for export to Python
	#include <pybind11/pybind11.h>
	#include <pybind11/stl.h>
	#include <pybind11/complex.h>

	namespace py = pybind11;

	PYBIND11_MODULE(ComplexRootsFinder, module_handle) {
		
		module_handle.doc() = "Cross-platform Python wrapper for ComplexRootsFinder С++ library. Developed at MEPhI in 2022.";
		
		module_handle.def("FindComplexRoots", &find_complex_roots, "returns a list of complex roots of a given function in a square with given center coordinates and given radius with given eps precision", py::arg("function"), py::arg("r"), py::arg("x0"), py::arg("y0"), py::arg("eps"));

	}

#endif // !_DEBUG