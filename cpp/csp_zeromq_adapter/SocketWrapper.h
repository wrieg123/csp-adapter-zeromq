#ifndef _IN_ZMQ_SOCKET_WRAPPER_H
#define _IN_ZMQ_SOCKET_WRAPPER_H

#include <csp/core/Exception.h>
#include <csp/core/Time.h>

#include <chrono>
#include <condition_variable>
#include <queue>
#include <thread>
#include <zmq.hpp>

namespace csp_zeromq_adapter {

using namespace csp;

class SocketWrapper {
 public:
  SocketWrapper(std::string uri, bool bind, bool connect, TimeDelta timeout);
  ~SocketWrapper() {};

  virtual void start();
  virtual void stop();
  void connectOrBindSocket(zmq::socket_t&);

  virtual void run() {};

  std::string uri_;
  bool bind_;
  bool connect_;
  std::chrono::milliseconds timeout_;

  std::unique_ptr<std::thread> thread_ptr_;
  bool engine_running_ = false;
};
}  // namespace csp_zeromq_adapter
#endif