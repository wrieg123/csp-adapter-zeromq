#ifndef _IN_ZMQ_PULL_SOCKET_H
#define _IN_ZMQ_PULL_SOCKET_H

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

class PullSocket final : public SocketWrapper {
 public:
  PullSocket(Engine* engine, zmq::context_t& ctx,
             GenericPushInputAdapter* adapter, std::string uri, bool bind,
             bool connect, TimeDelta timeout);
  ~PullSocket() {};

  void start() override;

  void run() override;

 private:
  Engine* engine_;
  zmq::context_t& ctx_;
  zmq::socket_t socket_;
  GenericPushInputAdapter* input_adapter_;
  int timeout_ms_;
};

}  // namespace csp_zeromq_adapter

#endif  //_IN_ZMQ_PULL_SOCKET_H