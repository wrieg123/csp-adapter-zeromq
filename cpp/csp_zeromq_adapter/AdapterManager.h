#ifndef _IN_ZMQ_ADAPTER_MANAGER_H
#define _IN_ZMQ_ADAPTER_MANAGER_H

#include <csp/core/Time.h>
#include <csp/engine/AdapterManager.h>
#include <csp/engine/Dictionary.h>
#include <csp/engine/Engine.h>
#include <csp/engine/OutputAdapter.h>
#include <csp_zeromq_adapter/ContextManager.h>

#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class ZeroMQAdapterManager final : public AdapterManager {
 public:
  ZeroMQAdapterManager(Engine* engine, const Dictionary& properties);
  ~ZeroMQAdapterManager();

  const char* name() const override { return "ZeroMQAdapterManager"; }

  void start(DateTime starttime, DateTime endtime) override;
  void stop() override;

  OutputAdapter* createPubOutputAdapter(CspTypePtr& type,
                                        const Dictionary& properties);
  InputAdapter* createSubInputAdapter(CspTypePtr& type, PushMode pushMode,
                                      const Dictionary& properties);
  DateTime processNextSimTimeSlice(DateTime time) override;

 private:
  std::unique_ptr<ContextManager> ctx_mgr_ptr_;
};

}  // namespace csp_zeromq_adapter

#endif  //_IN_ZMQ_ADAPTER_MANAGER_H