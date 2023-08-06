#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

static PyObject * distance(PyObject * self, PyObject * args)
{

    double ori_x = 0.0;
    double ori_y = 0.0;
    double dest_x = 0.0;
    double dest_y = 0.0;

    if (!PyArg_ParseTuple(args, "dddd", &ori_x, &ori_y, &dest_x, &dest_y))
        Py_RETURN_NONE;

    double result = sqrt((ori_x - dest_x) * (ori_x - dest_x) + (ori_y - dest_y) * (ori_y - dest_y));

    return Py_BuildValue("d", result);

}

static PyMethodDef math_methods[] = {
    {
        "distance",
        (PyCFunction)(void(*)(void))distance,
        METH_VARARGS,
         ""
     },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef math_def = {
    PyModuleDef_HEAD_INIT,
    "math",
    NULL,
    -1,
    math_methods
};

PyMODINIT_FUNC
PyInit_math(void)
{
    return PyModule_Create(&math_def);
}
