#ifndef _IN_ZMQ_PUSH_OUTPUT_ADAPTER_H
#define _IN_ZMQ_PUSH_OUTPUT_ADAPTER_H

#include <csp/engine/OutputAdapter.h>
#include <csp_zeromq_adapter/PushSocket.h>
#include <csp_zeromq_adapter/StructWriter.h>

#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class PushOutputAdapter final : public OutputAdapter {
 public:
  PushOutputAdapter(Engine* engine, CspTypePtr& type, PushSocket& socket,
                    const Dictionary& messageMapper);
  ~PushOutputAdapter() {};
  const char* name() const override { return "PushOutputAdapter"; }

  void executeImpl() override;

 private:
  PushSocket& socket_;
  std::string topic_;
  StructWriter writer_;
};

}  // namespace csp_zeromq_adapter

#endif  //_IN_ZMQ_PUSH_OUTPUT_ADAPTER_H