#include <csp_adapter_zeromq/PubSocket.h>

namespace csp_adapter_zeromq {

PubSocket::PubSocket(zmq::context_t& ctx, std::string uri, bool bind,
                     bool connect, TimeDelta timeout)
    : SocketWrapper(uri, bind, connect, timeout),
      socket_(ctx, zmq::socket_type::pub) {}

void PubSocket::push(const std::string& topic, const std::string& message) {
  std::unique_lock<std::mutex> lock(mutex_);
  queue_.push(std::make_pair(zmq::message_t(topic), zmq::message_t(message)));
  cond_.notify_one();
}

void PubSocket::start() {
  connectOrBindSocket(socket_);

  SocketWrapper::start();
}

void PubSocket::run() {
  while (engine_running_) {
    std::unique_lock<std::mutex> lock(mutex_);

    if (cond_.wait_for(lock, timeout_, [this]() {
          return !queue_.empty() && engine_running_;
        })) {
      auto& [topic, message] = queue_.front();
      socket_.send(topic, zmq::send_flags::sndmore);
      socket_.send(message);

      queue_.pop();
    }
  }
}

}  // namespace csp_adapter_zeromq