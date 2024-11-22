#ifndef _IN_ZMQ_PUB_OUTPUT_ADAPTER_H
#define _IN_ZMQ_PUB_OUTPUT_ADAPTER_H

#include <csp/engine/Dictionary.h>
#include <csp/engine/Engine.h>
#include <csp/engine/OutputAdapter.h>
#include <csp_zeromq_adapter/PubSocket.h>
#include <csp_zeromq_adapter/StructWriter.h>

#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class PubOutputAdapter final : public OutputAdapter {
 public:
  PubOutputAdapter(Engine* engine, CspTypePtr& type, PubSocket& socket,
                   const std::string& topic, const Dictionary& messageMapper);
  ~PubOutputAdapter() {};
  const char* name() const override { return "PubOutputAdapter"; }

  void executeImpl() override;

 private:
  PubSocket& socket_;
  std::string topic_;
  StructWriter writer_;
};

}  // namespace csp_zeromq_adapter

#endif  //_IN_ZMQ_PUB_OUTPUT_ADAPTER_H