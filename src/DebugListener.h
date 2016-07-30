#include "taglib/tdebuglistener.h"

class PytaglibDebugListener : public TagLib::DebugListener
{
    public:
    void printMessage(const TagLib::String &msg);
};
