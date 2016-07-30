#include "taglib/tdebuglistener.h"

class PytaglibDebugListener : public TagLib::DebugListener
{
    public:
        virtual void printMessage(const TagLib::String &msg);
};
