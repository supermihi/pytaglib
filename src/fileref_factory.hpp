#pragma once
#include <Python.h>

namespace TagLib {
    class FileRef;
    //! Create a TagLib::FileRef from a Python path object (str).
    /*!
     * This method provides a platform-independent interface to the Cython taglib extension.
     *
     * \param path_obj A Python str object representing the file path.
     * \return A pointer to a TagLib::FileRef, or nullptr on failure.
     *
    */
    FileRef* make_fileref(PyObject* path_obj) noexcept;
}