#include "fileref_factory.hpp"
#include <taglib/fileref.h>
#include <taglib/tiostream.h>
#include <taglib/audioproperties.h>
#include <Python.h>


namespace TagLib {
FileRef* make_fileref(PyObject* path_obj) noexcept {
    if (!path_obj) return nullptr;
    try {
#ifdef _WIN32        // Windows: convert Python str to wchar_t*
        wchar_t* wchar_path = PyUnicode_AsWideCharString(path_obj, nullptr);
        if (!wchar_path) {
            PyErr_Clear();
            return nullptr;
        }
        FileRef* file_ref = new FileRef(FileName(wchar_path), true, TagLib::AudioProperties::ReadStyle::Average);
        PyMem_Free(wchar_path);
        return file_ref;
#else
        // Unix: encode Python str to UTF-8 bytes
        PyObject* utf8_bytes = PyUnicode_AsUTF8String(path_obj);
        if (!utf8_bytes) {
            PyErr_Clear();
            return nullptr;
        }
        const char* utf8_path = PyBytes_AsString(utf8_bytes);
        FileRef* file_ref = new FileRef(utf8_path, true, TagLib::AudioProperties::ReadStyle::Average);
        Py_DECREF(utf8_bytes);
        return file_ref;
#endif
    } catch (...) {
        return nullptr;
    }
}
}