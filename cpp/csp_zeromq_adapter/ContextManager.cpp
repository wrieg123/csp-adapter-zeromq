#include <csp_zeromq_adapter/ContextManager.h>

namespace csp_zeromq_adapter {

ContextManager::ContextManager(Engine* engine, int io_threads)
    : engine_(engine), ctx_(io_threads) {};

ContextManager::~ContextManager() {};

void ContextManager::start() {
  for (const auto& pair : pub_output_adapters_) pair.second->start();
  for (const auto& pair : sub_input_adapters_) pair.second->start();
}

void ContextManager::stop() {
  for (const auto& pair : pub_output_adapters_) pair.second->stop();
  for (const auto& pair : sub_input_adapters_) pair.second->stop();
}

OutputAdapter* ContextManager::registerPubOutputAdapter(
    CspTypePtr& type, const Dictionary& properties) {
  const Dictionary& connectionDetails = getConnectionDetails(properties);
  const Dictionary& messageMapper = getMessageMapper(properties);

  std::string topic = properties.get<std::string>("topic");
  std::string host = connectionDetails.get<std::string>("uri");

  if (pub_output_adapters_.find(host) == pub_output_adapters_.end())
    pub_output_adapters_[host] = std::make_unique<PubSocket>(
        ctx_, host, connectionDetails.get<bool>("bind"),
        connectionDetails.get<bool>("connect"),
        connectionDetails.get<TimeDelta>("timeout"));

  return engine_->createOwnedObject<PubOutputAdapter>(
      type, *pub_output_adapters_[host].get(), topic, messageMapper);
}

InputAdapter* ContextManager::registerSubInputAdapter(
    CspTypePtr& type, PushMode pushMode, const Dictionary& properties) {
  const Dictionary& connectionDetails = getConnectionDetails(properties);
  const Dictionary& messageMapper = getMessageMapper(properties);

  std::string topic = properties.get<std::string>("topic");
  std::string host = connectionDetails.get<std::string>("uri");

  if (sub_input_adapters_.find(host) == sub_input_adapters_.end())
    sub_input_adapters_[host] = std::make_unique<SubSocket>(
        engine_, ctx_, host, connectionDetails.get<bool>("bind"),
        connectionDetails.get<bool>("connect"),
        connectionDetails.get<TimeDelta>("timeout"));

  GenericPushInputAdapter* inputAdapter =
      engine_->createOwnedObject<GenericPushInputAdapter>(type, pushMode,
                                                          messageMapper);

  sub_input_adapters_[host]->addAdapter(topic, inputAdapter);

  return inputAdapter;
}

inline const Dictionary& ContextManager::getConnectionDetails(
    const Dictionary& properties) {
  return *properties.get<DictionaryPtr>("connection_details");
}

inline const Dictionary& ContextManager::getMessageMapper(
    const Dictionary& properties) {
  return *properties.get<DictionaryPtr>("msg_mapper");
}

}  // namespace csp_zeromq_adapter