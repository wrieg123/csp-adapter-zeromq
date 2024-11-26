#ifndef _IN_ZMQ_CONTEXT_MANAGER_H
#define _IN_ZMQ_CONTEXT_MANAGER_H

#include <csp/core/Time.h>
#include <csp/engine/Dictionary.h>
#include <csp/engine/Engine.h>
#include <csp/engine/InputAdapter.h>
#include <csp/engine/OutputAdapter.h>
#include <csp_adapter_zeromq/GenericPushInputAdapter.h>
#include <csp_adapter_zeromq/PubOutputAdapter.h>
#include <csp_adapter_zeromq/PubSocket.h>
#include <csp_adapter_zeromq/PullSocket.h>
#include <csp_adapter_zeromq/PushOutputAdapter.h>
#include <csp_adapter_zeromq/PushSocket.h>
#include <csp_adapter_zeromq/SubSocket.h>

#include <unordered_map>
#include <zmq.hpp>

namespace csp_adapter_zeromq {

using namespace csp;

class ContextManager {
 public:
  ContextManager(Engine* engine, int io_threads);
  ~ContextManager();

  void start();
  void stop();

  OutputAdapter* registerPubOutputAdapter(CspTypePtr& type,
                                          const Dictionary& properties);
  InputAdapter* registerSubInputAdapter(CspTypePtr& type, PushMode pushMode,
                                        const Dictionary& properties);
  OutputAdapter* registerPushOutputAdapter(CspTypePtr& type,
                                           const Dictionary& properties);
  InputAdapter* registerPullInputAdapter(CspTypePtr& type, PushMode pushMode,
                                         const Dictionary& properties);

 private:
  inline const Dictionary& getConnectionDetails(const Dictionary& properties);
  inline const Dictionary& getMessageMapper(const Dictionary& properties);

 private:
  Engine* engine_;
  zmq::context_t ctx_;
  // Socket lookups by host
  std::unordered_map<std::string, std::unique_ptr<PubSocket>>
      pub_output_adapters_;
  std::unordered_map<std::string, std::unique_ptr<SubSocket>>
      sub_input_adapters_;
  std::vector<std::unique_ptr<PushSocket>> push_socket_adapters_;
  std::vector<std::unique_ptr<PullSocket>> pull_socket_adapters_;
};

}  // namespace csp_adapter_zeromq

#endif  // _IN_ZMQ_CONTEXT_MANAGER_H