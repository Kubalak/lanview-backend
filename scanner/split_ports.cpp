#include "Python.h"
#include <stdio.h>
#include <vector>
#include <utility>

static PyObject* _get_ports(std::vector<int>& ports){

    // std::vector<std::pair<int,int>> range;
    // std::vector<int> select;

    PyObject* selected = NULL, *ranges = NULL;
    selected = PyList_New(0);
    ranges = PyList_New(0);
    if(selected == NULL || ranges == NULL){
        if(selected != NULL)
            Py_CLEAR(selected);
        
        if(ranges != NULL)
            Py_CLEAR(selected);
        return NULL;
    }

    long unsigned int i = 0;
    while(i < ports.size()){
        unsigned long int j = i + 1;
        while (j < ports.size() && ports[j] - ports[j - 1] == 1)
            j++;
            
        if (j == i + 1){
            if(PyList_Append(selected, PyLong_FromLong(ports[i])) == -1){
                Py_CLEAR(selected);
                Py_CLEAR(ranges);
                return NULL;
            }
            i++;
        }
        else{
            PyObject* tuple = PyTuple_Pack(2, PyLong_FromLong(ports[i]), PyLong_FromLong(ports[j-1]));
            if(tuple == NULL){
                Py_CLEAR(selected);
                Py_CLEAR(ranges);
                return NULL;
            }
            
            if(PyList_Append(ranges, tuple) == -1){
                Py_CLEAR(selected);
                Py_CLEAR(ranges);
                Py_CLEAR(tuple);
                return NULL;
            }
            i = j;
        }
    }

    PyObject* result = PyDict_New();

    if(result == NULL){
        Py_CLEAR(selected);
        Py_CLEAR(ranges);
        return NULL;
    }

    // if(selected == NULL || ranges == NULL || result == NULL)
    //     return NULL;
    
    // for(long unsigned int i(0); i < select.size(); i++)
    //     if(PyList_SetItem(selected, i, PyLong_FromLong(select[i])) == -1)
    //         return NULL;

    // for(long unsigned int i(0); i < range.size(); i++){
    //     PyObject* tuple = PyTuple_Pack(2, PyLong_FromLong(range[i].first), PyLong_FromLong(range[i].second));
        
    //     if(tuple == NULL)
    //         return NULL;

    //     if(PyList_SetItem(ranges, i, tuple) == -1)
    //         return NULL;
    // }

    if(PyDict_SetItemString(result, "select", selected) == -1)
        return NULL;
    
    if(PyDict_SetItemString(result, "range", ranges) == -1)
        return NULL;
    
    return result;
}



static PyObject* make_ports(PyObject* self, PyObject* args){
    PyObject* portslist;
    std::vector<int> ports;
    int ports_len;

    if(!PyArg_ParseTuple(args, "O", &portslist))
        return NULL;

    ports_len = PyList_Size(portslist);
    
    if(ports_len < 0)
        return NULL;


    for(int i = 0; i < ports_len; i++) {
        PyObject* item;
        item = PyList_GetItem(portslist, i);
        if(item && PyLong_Check(item)) 
            ports.push_back((int)PyLong_AsLong(item));
        else
            printf("Warning: Item on index %d is not long (int)!", i);  
        
        // if(PyList_SetItem(result, i, PyLong_FromLong(ports[i]))== -1)
        //     return NULL;
    }
    
    return _get_ports(ports);
}


static PyMethodDef SplitMethods[] = {
    {"splitp", make_ports, METH_VARARGS, "Split ports method check"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef splitmodule = {
    PyModuleDef_HEAD_INIT,
    "splitp",
    "Module definiton for split method",
    -1,
    SplitMethods
};

PyMODINIT_FUNC PyInit_splitp(void){
    PyObject* module = PyModule_Create(&splitmodule);

    return module;
}