#include <csp_adapter_zeromq/PushSocket.h>

#include <iostream>

namespace csp_adapter_zeromq {

PushSocket::PushSocket(zmq::context_t& ctx, std::string uri, bool bind,
                       bool connect, TimeDelta timeout)
    : SocketWrapper(uri, bind, connect, timeout),
      socket_(ctx, zmq::socket_type::push) {}

void PushSocket::push(const std::string& message) {
  std::unique_lock<std::mutex> lock(mutex_);
  queue_.push(zmq::message_t(message));
  cond_.notify_one();
}

void PushSocket::start() {
  connectOrBindSocket(socket_);

  SocketWrapper::start();
}

void PushSocket::run() {
  while (engine_running_) {
    std::unique_lock<std::mutex> lock(mutex_);

    if (cond_.wait_for(lock, timeout_, [this]() {
          return !queue_.empty() && engine_running_;
        })) {
      auto& message = queue_.front();
      socket_.send(message, zmq::send_flags::dontwait);

      queue_.pop();
    }
  }
}

}  // namespace csp_adapter_zeromq