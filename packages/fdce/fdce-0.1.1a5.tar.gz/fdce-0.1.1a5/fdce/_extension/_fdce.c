#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

double d_1, d_2, c1, c2, c3;
int n, m, v, m_min;
int N, M;

#define GET1(arr, i) *((double *)PyArray_GETPTR1(arr, i))
#define GET3(arr, i, j, k) *((double *)PyArray_GETPTR3(arr, i, j, k))
#define SET3(arr, i, j, k, val) PyArray_SETITEM(arr, PyArray_GETPTR3(arr, i, j, k), PyFloat_FromDouble(val))

#define MIN(a, b) (a < b ? a : b)

void _get_coeff(float x_0, PyArrayObject* a, int ord, PyArrayObject* coeff_arr){
	N = PyArray_DIM(a, 0);
	M = ord + 1;
	SET3(coeff_arr, 0, 0, 0, 1);

	c1 = 1;
	for (n = 1; n < N; n++){
		c2 = 1;
		m_min = MIN(n, M);
		for (v = 0; v< n; v++){
			c3 = GET1(a, n) - GET1(a, v);
			c2 = c2 * c3;
			if (n < M) SET3(coeff_arr, n, n - 1, v, c2);
			for (m = 0; m < m_min; m++){
				d_1 = GET3(coeff_arr, m, n -1, v);
				d_2 = m == 0 ? 0 : GET3(coeff_arr, m - 1, n - 1, v);
				SET3(coeff_arr, m, n, v, ((GET1(a, n) - x_0) * d_1 - m * d_2) / c3);
			}
		}
		for (m = 0; m < m_min; m++){
			d_1 = m == 0? 0 : GET3(coeff_arr, m - 1, n - 1, n - 1);
			d_2 = GET3(coeff_arr, m, n - 1, n - 1);
			SET3(coeff_arr, m, n, n, (c1 / c2) * (m * d_1 - (GET1(a, n - 1) - x_0) * d_2));
		}
		c1 = c2;
	}
}

PyObject* get_coeff(PyObject* self, PyObject* args){
	PyObject *a, *coeff_arr;
	float x_0;
	int ord;

	if (!PyArg_ParseTuple(args, "dO!iO!", &x_0, &PyArray_Type, &a, &ord, &PyArray_Type, &coeff_arr))
		return NULL;

	a = PyArray_FROM_OTF(a, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
	coeff_arr = PyArray_FROM_OTF(coeff_arr, NPY_DOUBLE, NPY_ARRAY_INOUT_ARRAY);

	_get_coeff(x_0, (PyArrayObject*)a, ord, (PyArrayObject*)coeff_arr);

	Py_DECREF(a);
	Py_DECREF(coeff_arr);
	Py_INCREF(Py_None);
	return Py_None;
}


static PyMethodDef _fdce_methods[] = {
	{"get_coeff", get_coeff, METH_VARARGS, "Get coefficients"},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef _fdce_module = {
	PyModuleDef_HEAD_INIT,
	"_fdce",
	NULL,
	-1,
	_fdce_methods
};

PyMODINIT_FUNC PyInit__fdce(void){
	PyObject *m = PyModule_Create(&_fdce_module);
	if (m == NULL)
		return NULL;
	import_array();
	return m;
}
