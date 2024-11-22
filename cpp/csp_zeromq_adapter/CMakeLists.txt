set(ZMQ_HEADERS
    AdapterManager.h
    ContextManager.h
    GenericPushInputAdapter.h
    PubOutputAdapter.h
    PubSocket.h
    SocketWrapper.h
    StructWriter.h
    SubSocket.h
)

set(ZMQ_SOURCE
    AdapterManager.cpp
    ContextManager.cpp
    GenericPushInputAdapter.cpp
    PubOutputAdapter.cpp
    PubSocket.cpp
    SocketWrapper.cpp
    StructWriter.cpp
    SubSocket.cpp

    ${ZMQ_HEADERS}
)

# Library
find_package(cppzmq)
add_library(cspzmqlibimpl SHARED ${ZMQ_SOURCE} adapterimpl.cpp)
target_link_libraries(cspzmqlibimpl PRIVATE ${CSP_LIBRARY} ${CSP_ADAPTER_UTILS_LIBRARY} cppzmq protobuf)
install(
    TARGETS cspzmqlibimpl
    RUNTIME DESTINATION ${CSPZMQ_RUNTIME_INSTALL_SUBDIR}
    LIBRARY DESTINATION lib/
)