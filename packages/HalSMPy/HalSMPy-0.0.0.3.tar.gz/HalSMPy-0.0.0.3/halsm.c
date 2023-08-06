#include <Python.h>
#include <HalSM.h>

//String Library

char* Decimal2Str(long long number) {
    char* out=calloc(40,sizeof(char));
    sprintf(out,"%d",number);
    return out;
}

char* Double2Str(double d) {
    char* out=calloc(22,sizeof(char));
    sprintf(out,"%lf",d);
    return out;
}

char* Decimal2HexStr(long long number) {
    char* out=calloc(34,sizeof(char));
    sprintf(out,"%llx",number);
    return out;
}

long long ParseDecimal(char* number) {
    return strtoll(number,NULL,0);    
}

double ParseDouble(char* number) {
    return strtod(number,NULL);
}

//String Library

//Load Shared Library

void* loadsharedlibrary_load(char* path)
{
    return NOTHALSMNULLPOINTER;
}

void* loadsharedlibrary_getAddressByName(void* library,char* name)
{
    return NOTHALSMNULLPOINTER;
}

void loadsharedlibrary_close(void* library)
{
    
}

//Load Shared Library

//Memory Managment Library

void* mem_alloc(unsigned int size)
{
    return malloc(size);
}

void* c_alloc(unsigned int size,unsigned int n)
{
    return calloc(size,n);
}

void* re_alloc(void* ptr,unsigned int size)
{
    return realloc(ptr,size);
}

void free_mem(void* ptr)
{
    free(ptr);
}

//Memory Managment Library

//System Library

void system_exit(int status)
{
    exit(status);
}

//System Library

PyObject* print_func;
PyObject* print_err_func;
PyObject* input_func;
PyObject* read_file_func;
PyObject* listModules;
char* path_modules;
HalSMMemoryManagmentLibrary hsmmml={&mem_alloc,&c_alloc,&re_alloc,&free_mem};
HalSMSystemLibrary hsysl={&system_exit};
HalSMStringLibrary hsl={&Decimal2Str,&Decimal2HexStr,&Double2Str,&ParseDecimal,&ParseDouble};
HalSMLoadSharedLibrary hlsl={&loadsharedlibrary_load,&loadsharedlibrary_getAddressByName,&loadsharedlibrary_close};

HalSM* hsm;

void halsm_print_func(char* text) {
    PyObject* args=PyTuple_Pack(1,PyUnicode_FromString(text));
    PyObject_CallObject(print_func,args);
}

void halsm_print_err_func(char* err) {
    
}

char* halsm_input_func(char* text) {
    return "";
}

char* halsm_read_file_func(char* path) {
    return "";
}

static PyObject* halsm_module_HalSM_init(PyObject* self,PyObject* args) {
    if (!PyArg_ParseTuple(args,"OOOOOs",&listModules,&print_func,&print_err_func,&input_func,&read_file_func,&path_modules))
        return NULL;
    hsm=HalSM_init(HalSMArray_init(&hsmmml),&halsm_print_func,&halsm_print_err_func,&halsm_input_func,&halsm_read_file_func,path_modules,&hlsl,&hsl,&hsmmml,&hsysl);
    return Py_BuildValue("i",0);
}

static PyObject* halsm_module_HalSM_compile(PyObject* self,PyObject* args) {
    char* code;
    if (!PyArg_ParseTuple(args,"s",&code))
        return NULL;
    HalSM_compile_without_path(hsm,code);
    return Py_BuildValue("i",0);
}

static PyMethodDef halsm_module_funcs[]= {
    {
        "init",
        (PyCFunction)halsm_module_HalSM_init,
        METH_VARARGS,
        "init(listModules:list,print_func:method,print_err_func:method,input_func:method,read_file_func:method,path_modules:str): init HalSM Class"
    },
    {
        "compile",
        (PyCFunction)halsm_module_HalSM_compile,
        METH_VARARGS,
        "compile(code:str): Compile HalSM code"
    },
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef halsm_module= {
    PyModuleDef_HEAD_INIT,
    "HalSM",
    "HalSM Python Library",
    -1,
    halsm_module_funcs
};

PyMODINIT_FUNC PyInit_HalSM(void) {
    return PyModule_Create(&halsm_module);
}