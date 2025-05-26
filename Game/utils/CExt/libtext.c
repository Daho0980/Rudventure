#include <Python.h>
#include <locale.h>


static PyObject* joineach(PyObject* self, PyObject* args) {
    PyObject *mainline, *subline;

    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &mainline, &PyList_Type, &subline)) {
        return NULL;
    }

    Py_ssize_t mainlineLen = PyList_Size(mainline);
    Py_ssize_t sublineLen  = PyList_Size(subline) ;
    Py_ssize_t maxLen      = (mainlineLen>sublineLen)? mainlineLen: sublineLen;

    PyObject *output = PyList_New(maxLen * 2);
    if (!output) return NULL;

    PyObject *emptyStr = PyUnicode_FromString("");
    if (!emptyStr) {
        Py_DECREF(output);
        return NULL;
    }

    Py_INCREF(emptyStr);
    PyObject *sep = emptyStr;

    for (Py_ssize_t i = 0; i < maxLen; ++i) {
        PyObject *mainItem = (i<mainlineLen)? PyList_GetItem(mainline, i): emptyStr;
        PyObject *subItem  = (i<sublineLen )? PyList_GetItem(subline,  i): emptyStr;

        Py_INCREF(mainItem);
        Py_INCREF(subItem) ;

        PyList_SetItem(output, i*2    , mainItem);
        PyList_SetItem(output, (i*2)+1, subItem) ;
    }

    PyObject *result = PyUnicode_Join(sep, output);

    Py_DECREF(sep)     ;
    Py_DECREF(emptyStr);
    Py_DECREF(output)  ;

    if (!result) return NULL;

    return result;
}


static PyMethodDef LibtextMethods[] = {
    {
        "joineach",
        joineach,
        METH_VARARGS,
        "Returns the string of the two lists in sequence."
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef libtextmodule = {
    PyModuleDef_HEAD_INIT,
    "libtext",
    "Text processing C extension",
    -1,
    LibtextMethods
};

PyMODINIT_FUNC PyInit_libtext(void) { return PyModule_Create(&libtextmodule); }