#include <csp/engine/PushInputAdapter.h>
#include <csp/python/Conversions.h>
#include <csp/python/Exception.h>
#include <csp/python/InitHelper.h>
#include <csp/python/PyAdapterManagerWrapper.h>
#include <csp/python/PyEngine.h>
#include <csp/python/PyInputAdapterWrapper.h>
#include <csp/python/PyOutputAdapterWrapper.h>
#include <csp_zeromq_adapter/AdapterManager.h>

namespace csp_zeromq_adapter {
using namespace csp;
using namespace csp::python;

csp::AdapterManager* create_zeromq_adapter_manager(
    PyEngine* engine, const Dictionary& properties) {
  return engine->engine()->createOwnedObject<ZeroMQAdapterManager>(properties);
};

static OutputAdapter* create_zeromq_pub_socket_output_adapter(
    csp::AdapterManager* manager, PyEngine* pyengine, PyObject* args) {
  PyObject* pyProperties;
  PyObject* pyType;

  auto* zmqManager = dynamic_cast<ZeroMQAdapterManager*>(manager);
  if (!zmqManager) CSP_THROW(TypeError, "Expected ZeroMQAdapterManager");

  if (!PyArg_ParseTuple(args, "OO!", &pyType, &PyDict_Type, &pyProperties))
    CSP_THROW(PythonPassthrough, "");

  auto& cspType = pyTypeAsCspType(pyType);

  return zmqManager->createPubOutputAdapter(
      cspType, fromPython<Dictionary>(pyProperties));
}

static InputAdapter* create_zeromq_sub_socket_input_adapter(
    csp::AdapterManager* manager, PyEngine* pyengine, PyObject* pyType,
    PushMode pushMode, PyObject* args) {
  auto& cspType = pyTypeAsCspType(pyType);

  PyObject* pyProperties;
  PyObject* type;

  auto* zmqManager = dynamic_cast<ZeroMQAdapterManager*>(manager);
  if (!zmqManager) CSP_THROW(TypeError, "Expected ZeroMQAdapterManager");

  if (!PyArg_ParseTuple(args, "O!O!", &PyType_Type, &type, &PyDict_Type,
                        &pyProperties))
    CSP_THROW(PythonPassthrough, "");

  return zmqManager->createSubInputAdapter(
      cspType, pushMode, fromPython<Dictionary>(pyProperties));
}

static OutputAdapter* create_zeromq_push_socket_output_adapter(
    csp::AdapterManager* manager, PyEngine* pyengine, PyObject* args) {
  PyObject* pyProperties;
  PyObject* pyType;

  auto* zmqManager = dynamic_cast<ZeroMQAdapterManager*>(manager);
  if (!zmqManager) CSP_THROW(TypeError, "Expected ZeroMQAdapterManager");

  if (!PyArg_ParseTuple(args, "OO!", &pyType, &PyDict_Type, &pyProperties))
    CSP_THROW(PythonPassthrough, "");

  auto& cspType = pyTypeAsCspType(pyType);

  return zmqManager->createPushOutputAdapter(
      cspType, fromPython<Dictionary>(pyProperties));
}

static InputAdapter* create_zeromq_pull_socket_input_adapter(
    csp::AdapterManager* manager, PyEngine* pyengine, PyObject* pyType,
    PushMode pushMode, PyObject* args) {
  auto& cspType = pyTypeAsCspType(pyType);

  PyObject* pyProperties;
  PyObject* type;

  auto* zmqManager = dynamic_cast<ZeroMQAdapterManager*>(manager);
  if (!zmqManager) CSP_THROW(TypeError, "Expected ZeroMQAdapterManager");

  if (!PyArg_ParseTuple(args, "O!O!", &PyType_Type, &type, &PyDict_Type,
                        &pyProperties))
    CSP_THROW(PythonPassthrough, "");

  return zmqManager->createPullInputAdapter(
      cspType, pushMode, fromPython<Dictionary>(pyProperties));
}

REGISTER_ADAPTER_MANAGER(_adapter_manager, create_zeromq_adapter_manager);
REGISTER_OUTPUT_ADAPTER(_pub_socket_output_adapter,
                        create_zeromq_pub_socket_output_adapter);
REGISTER_INPUT_ADAPTER(_sub_socket_input_adapter,
                       create_zeromq_sub_socket_input_adapter);
REGISTER_OUTPUT_ADAPTER(_push_socket_output_adapter,
                        create_zeromq_push_socket_output_adapter);
REGISTER_INPUT_ADAPTER(_pull_socket_input_adapter,
                       create_zeromq_pull_socket_input_adapter);

static PyModuleDef _cspzmqlibimpl_module = {PyModuleDef_HEAD_INIT,
                                            "_cspzmqlibimpl",
                                            "_cspzmqlibimpl c++ module",
                                            -1,
                                            NULL,
                                            NULL,
                                            NULL,
                                            NULL,
                                            NULL};

PyMODINIT_FUNC PyInit__cspzmqlibimpl(void) {
  PyObject* m;

  m = PyModule_Create(&_cspzmqlibimpl_module);
  if (m == NULL) return NULL;

  if (!InitHelper::instance().execute(m)) return NULL;

  return m;
}

}  // namespace csp_zeromq_adapter