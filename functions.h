// functions.h
#include <iostream>
#include <Python.h>

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

int callfunction()
{

    
    std::cout << "got inside functions" << std::endl;
    Py_Initialize();
    PyObject* module = PyImport_ImportModule("undobottonhandle");
    PyObject* function = PyObject_GetAttrString(module, "click_coordinates");
    PyObject* result = PyObject_CallObject(function, NULL);
        if (result != NULL) {
        // Do something with the result
        Py_DECREF(result);
    } else {
        // Handle error case
        PyErr_Print();
    }

    // Clean up
    Py_DECREF(function);
    Py_DECREF(module);
    Py_Finalize();

    return 0;
    
}

