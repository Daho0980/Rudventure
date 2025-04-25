#include <Python.h>
#include <wchar.h>
#include <locale.h>
#include <limits.h>
#include <string.h>


static PyObject* actualLen(PyObject* self, PyObject* args) {
    PyObject   *inpStr;
    const char *str   ;

    if ( !PyArg_ParseTuple(args, "O!", &PyUnicode_Type, &inpStr) ) {
        PyErr_SetString(PyExc_TypeError, "Expected string as arguments.");

        return NULL;
    }

    str = PyUnicode_AsUTF8(inpStr);

    int width = 0;

    wchar_t    wideChar;
    mbstate_t  state   ;

    const char *p = str;

    memset(&state, 0, sizeof state);

    size_t len;
    while ( (len=mbrtowc(&wideChar, p, MB_LEN_MAX, &state))>0 ) {
        int w = wcwidth(wideChar);
        if ( w >= 0 ) width += w;

        p += len;
    }

    return PyLong_FromLong(width);
}

static PyObject* joineach(PyObject* self, PyObject* args) {
    PyObject *mainline, *subline;

    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &mainline, &PyList_Type, &subline)) {
        PyErr_SetString(PyExc_TypeError, "Expected two lists as arguments.");

        return NULL;
    }

    Py_ssize_t mainlineLen = PyList_Size(mainline);
    Py_ssize_t sublineLen  = PyList_Size(subline) ;

    Py_ssize_t maxLen = mainlineLen>sublineLen? mainlineLen: sublineLen;

    PyObject *output = PyList_New(maxLen * 2);
    if (!output) return NULL;

    PyObject *emptyStr = PyUnicode_New(0, 0);
    if (!emptyStr) {
        Py_DECREF(output);

        return NULL;
    }

    for (Py_ssize_t i = 0; i < maxLen; ++i) {
        PyObject *mainItem = (i < mainlineLen) ? PyList_GetItem(mainline, i) : emptyStr;
        PyObject *subItem  = (i < sublineLen ) ? PyList_GetItem(subline,  i) : emptyStr;

        Py_INCREF(mainItem);
        Py_INCREF(subItem) ;

        PyList_SetItem(output, i * 2    , mainItem);
        PyList_SetItem(output, i * 2 + 1, subItem );
    }

    PyObject *sep    = PyUnicode_New(0, 0)        ;
    PyObject *result = PyUnicode_Join(sep, output);

    Py_DECREF(sep)     ;
    Py_DECREF(emptyStr);
    Py_DECREF(output)  ;

    return result;
}

static PyMethodDef LibtextMethods[] = {
    {
        "actualLen",
        actualLen,
        METH_VARARGS,
        "Returns the actual display width of a string."
    },
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

PyMODINIT_FUNC PyInit_libtext(void) {
    setlocale(LC_CTYPE, "");
    return PyModule_Create(&libtextmodule);
};