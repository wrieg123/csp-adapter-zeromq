#include <csp_adapter_zeromq/StructWriter.h>

namespace csp_adapter_zeromq {

StructWriter::StructWriter(CspTypePtr& type, const Dictionary& messageMapper) {
  utils::MsgProtocol protocol =
      utils::MsgProtocol(messageMapper.get<std::string>("protocol"));
  switch (protocol) {
    case utils::MsgProtocol::JSON:
      msg_writer_ = std::make_shared<utils::JSONMessageWriter>(messageMapper);
      break;

    case utils::MsgProtocol::RAW_BYTES:
      break;

    default:
      CSP_THROW(NotImplemented,
                "msg protocol "
                    << protocol
                    << " not currently supported for csp_adapter_zeromqs");
      break;
  }

  if (!isRawBytes())
    data_mapper_ = utils::OutputDataMapperCache::instance().create(
        type, *messageMapper.get<DictionaryPtr>("field_map"));
  else if (type->type() != CspType::Type::STRING)
    CSP_THROW(TypeError,
              "RAW_BYTES output expected ts[str] got ts type " << type->type());
};

std::pair<const void*, size_t> StructWriter::write(
    const TimeSeriesProvider* sourcets) {
  msg_writer_->processTick(*data_mapper_, sourcets);
  return msg_writer_->finalize();
}

}  // namespace csp_adapter_zeromq