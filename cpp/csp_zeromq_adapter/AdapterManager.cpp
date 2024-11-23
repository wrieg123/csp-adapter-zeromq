#include <csp_zeromq_adapter/AdapterManager.h>

namespace csp_zeromq_adapter {

ZeroMQAdapterManager::ZeroMQAdapterManager(Engine* engine,
                                           const Dictionary& properties)
    : AdapterManager(engine) {
  int io_threads = static_cast<int>(properties.get<double>("io_threads"));
  ctx_mgr_ptr_ = std::make_unique<ContextManager>(engine, io_threads);
};

ZeroMQAdapterManager::~ZeroMQAdapterManager() {}

void ZeroMQAdapterManager::start(DateTime starttime, DateTime endtime) {
  // In the background start the ZMQ context manager
  ctx_mgr_ptr_->start();
}

void ZeroMQAdapterManager::stop() {
  // Stop and join the background thread(s)
  ctx_mgr_ptr_->stop();
}

OutputAdapter* ZeroMQAdapterManager::createPubOutputAdapter(
    CspTypePtr& type, const Dictionary& properties) {
  return ctx_mgr_ptr_->registerPubOutputAdapter(type, properties);
}

InputAdapter* ZeroMQAdapterManager::createSubInputAdapter(
    CspTypePtr& type, PushMode pushMode, const Dictionary& properties) {
  return ctx_mgr_ptr_->registerSubInputAdapter(type, pushMode, properties);
}

OutputAdapter* ZeroMQAdapterManager::createPushOutputAdapter(
    CspTypePtr& type, const Dictionary& properties) {
  return ctx_mgr_ptr_->registerPushOutputAdapter(type, properties);
}

InputAdapter* ZeroMQAdapterManager::createPullInputAdapter(
    CspTypePtr& type, PushMode pushMode, const Dictionary& properties) {
  return ctx_mgr_ptr_->registerPullInputAdapter(type, pushMode, properties);
}

DateTime ZeroMQAdapterManager::processNextSimTimeSlice(DateTime time) {
  return DateTime::NONE();
}

}  // namespace csp_zeromq_adapter