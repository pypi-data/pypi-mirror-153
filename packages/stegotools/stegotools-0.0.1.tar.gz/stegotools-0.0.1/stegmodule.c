#define PY_SSIZE_T_CLEAN
#include <Python.h>

static struct PyModuleDef stegmodule = {
	PyModuleDef_HEAD_INIT,
		"stego",
		NULL, // docstring
		0, // no state
		NULL // no methods
};
static PyObject* bytes_xor(PyObject *a, PyObject *b)
{
	Py_buffer va, vb;
	PyObject *result = NULL;

	va.len = -1;
	vb.len = -1;
	if (PyObject_GetBuffer(a, &va, PyBUF_SIMPLE) != 0 ||
			PyObject_GetBuffer(b, &vb, PyBUF_SIMPLE) != 0) {
		PyErr_Format(PyExc_TypeError, "can't xor %.100s with %.100s",
				Py_TYPE(a)->tp_name, Py_TYPE(b)->tp_name);
		goto done;
	}
	if(va.len != vb.len)
	{
		PyErr_Format(PyExc_ValueError, "can't xor bytes of unequal length");
		goto done;
	}

	result = PyBytes_FromStringAndSize(NULL, va.len);
	if (result != NULL) {
		char* rd = PyBytes_AS_STRING(result);
		char* ad = PyBytes_AS_STRING(a);
		char* bd = PyBytes_AS_STRING(b);
		for(Py_ssize_t i = 0; i < va.len; i++)
		{
			rd[i] = ad[i] ^ bd[i];
		}
	}
done:
	if (va.len != -1)
		PyBuffer_Release(&va);
	if (vb.len != -1)
		PyBuffer_Release(&vb);
	return result;
}
static PyObject* bytes_or(PyObject *a, PyObject *b)
{
	Py_buffer va, vb;
	PyObject *result = NULL;

	va.len = -1;
	vb.len = -1;
	if (PyObject_GetBuffer(a, &va, PyBUF_SIMPLE) != 0 ||
			PyObject_GetBuffer(b, &vb, PyBUF_SIMPLE) != 0) {
		PyErr_Format(PyExc_TypeError, "can't or %.100s with %.100s",
				Py_TYPE(a)->tp_name, Py_TYPE(b)->tp_name);
		goto done;
	}
	if(va.len != vb.len)
	{
		PyErr_Format(PyExc_ValueError, "can't or bytes of unequal length");
		goto done;
	}

	result = PyBytes_FromStringAndSize(NULL, va.len);
	if (result != NULL) {
		char* rd = PyBytes_AS_STRING(result);
		char* ad = PyBytes_AS_STRING(a);
		char* bd = PyBytes_AS_STRING(b);
		for(Py_ssize_t i = 0; i < va.len; i++)
		{
			rd[i] = ad[i] | bd[i];
		}
	}
done:
	if (va.len != -1)
		PyBuffer_Release(&va);
	if (vb.len != -1)
		PyBuffer_Release(&vb);
	return result;
}
static PyObject* bytes_and(PyObject *a, PyObject *b)
{
	Py_buffer va, vb;
	PyObject *result = NULL;

	va.len = -1;
	vb.len = -1;
	if (PyObject_GetBuffer(a, &va, PyBUF_SIMPLE) != 0 ||
			PyObject_GetBuffer(b, &vb, PyBUF_SIMPLE) != 0) {
		PyErr_Format(PyExc_TypeError, "can't and %.100s with %.100s",
				Py_TYPE(a)->tp_name, Py_TYPE(b)->tp_name);
		goto done;
	}
	if(va.len != vb.len)
	{
		PyErr_Format(PyExc_ValueError, "can't and bytes of unequal length");
		goto done;
	}

	result = PyBytes_FromStringAndSize(NULL, va.len);
	if (result != NULL) {
		char* rd = PyBytes_AS_STRING(result);
		char* ad = PyBytes_AS_STRING(a);
		char* bd = PyBytes_AS_STRING(b);
		for(Py_ssize_t i = 0; i < va.len; i++)
		{
			rd[i] = ad[i] & bd[i];
		}
	}
done:
	if (va.len != -1)
		PyBuffer_Release(&va);
	if (vb.len != -1)
		PyBuffer_Release(&vb);
	return result;
}
PyObject* PyInit_stego()
{
	PyBytes_Type.tp_as_number->nb_xor = (binaryfunc) bytes_xor;
	PyBytes_Type.tp_as_number->nb_or = (binaryfunc) bytes_or;
	PyBytes_Type.tp_as_number->nb_and = (binaryfunc) bytes_and;
	return PyModule_Create(&stegmodule);
}
