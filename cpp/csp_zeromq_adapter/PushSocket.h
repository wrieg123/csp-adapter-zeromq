#ifndef _IN_ZMQ_PUSH_SOCKET_H
#define _IN_ZMQ_PUSH_SOCKET_H

#include <csp/core/Exception.h>
#include <csp/core/Time.h>
#include <csp_zeromq_adapter/SocketWrapper.h>

#include <chrono>
#include <condition_variable>
#include <queue>
#include <thread>
#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class PushSocket final : public SocketWrapper {
 public:
  PushSocket(zmq::context_t& ctx, std::string uri, bool bind, bool connect,
             TimeDelta timeout);

  void push(const std::string& message);
  void start() override;

  void run() override;

 private:
  zmq::socket_t socket_;
  std::queue<zmq::message_t> queue_;
  std::mutex mutex_;
  std::condition_variable cond_;
};

}  // namespace csp_zeromq_adapter

#endif  //_IN_ZMQ_PUSH_SOCKET_H