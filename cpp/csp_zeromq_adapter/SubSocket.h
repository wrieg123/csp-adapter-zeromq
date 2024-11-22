#ifndef _IN_ZMQ_SUB_SOCKET_H
#define _IN_ZMQ_SUB_SOCKET_H

#include <csp/core/Time.h>
#include <csp/engine/Engine.h>
#include <csp/engine/InputAdapter.h>
#include <csp_zeromq_adapter/GenericPushInputAdapter.h>
#include <csp_zeromq_adapter/SocketWrapper.h>

#include <chrono>
#include <thread>
#include <unordered_map>
#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class SubSocket final : public SocketWrapper {
 public:
  SubSocket(Engine* engine, zmq::context_t& ctx, std::string host, bool bind,
            bool connect, TimeDelta timeout);
  ~SubSocket() {};

  void start() override;

  void addAdapter(std::string, GenericPushInputAdapter*);

  void run() override;

 private:
  Engine* engine_;
  zmq::context_t& ctx_;
  std::vector<std::pair<zmq::socket_t, GenericPushInputAdapter*>>
      input_adapters_;
};

}  // namespace csp_zeromq_adapter
#endif  //_IN_ZMQ_SUB_SOCKET_H