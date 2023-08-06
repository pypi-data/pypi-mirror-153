import edge_core.datatypes.io_property_pb2 as io_prop
import edge_core.datatypes.data_source_property_pb2 as ds_prop
import edge_core.datatypes.sinker_batch_payload_pb2 as res_batch
import edge_core.datatypes.sinker_io_payload_pb2 as res_io
from edge_core.helpers.time import get_current_unixtime
from edge_core.helpers.dict_control import check_field
import numpy as np


def make_pb_io_value(value: any, data_type: io_prop.IoValue):
    io_value = io_prop.IoValue()
    if data_type == io_prop.DataType.SINT32:
        io_value.sint32_value = int(value)
    elif data_type == io_prop.DataType.SINT64:
        io_value.sint64_value = int(value)
    elif data_type == io_prop.DataType.UINT32:
        io_value.uint32_value = int(value)
    elif data_type == io_prop.DataType.UINT64:
        io_value.uint64_value = int(value)
    elif data_type == io_prop.DataType.FLOAT:
        io_value.float_value = float(value)
    elif data_type == io_prop.DataType.DOUBLE:
        io_value.double_value = float(value)
    elif data_type == io_prop.DataType.STRING:
        io_value.string_value = str(value)
    elif data_type == io_prop.DataType.BYTES:
        io_value.bytes_value = bytes(value)
    elif data_type == io_prop.DataType.BOOL:
        io_value.bool_value = bool(value)
    else:
        io_value.bool_value = bool(value)
    return io_value


pb_enum_tb = {
    'INT': io_prop.DataType.SINT32,
    'SINT32': io_prop.DataType.SINT32,
    'SINT64': io_prop.DataType.SINT64,
    'UINT32': io_prop.DataType.UINT32,
    'UINT64': io_prop.DataType.UINT64,
    'FLOAT': io_prop.DataType.FLOAT,
    'DOUBLE': io_prop.DataType.DOUBLE,
    'STR': io_prop.DataType.STRING,
    'STRING': io_prop.DataType.STRING,
    'BYTES': io_prop.DataType.BYTES,
    'BOOL': io_prop.DataType.BOOL
}


def str_to_data_type(str_data_type: str) -> io_prop.DataType:
    res = io_prop.DataType.UNDEFINED
    dt = str_data_type.upper()
    if dt in pb_enum_tb:
        res = pb_enum_tb[dt]
    return res


def str_to_io_type(str_io_type: str) -> io_prop.IoType:
    if str_io_type.upper() == 'OUTPUT':
        res = io_prop.IoType.OUTPUT
    else:
        res = io_prop.IoType.INPUT
    return res


def str_to_method_type(method_type: io_prop.MethodType) -> str:
    res = None
    if method_type == io_prop.MethodType.READ:
        res = 'READ'
    elif method_type == io_prop.MethodType.WRITE:
        res = 'WRITE'
    return res


def str_to_collection_type(str_collection_type: str) -> ds_prop.CollectionType:
    if str_collection_type.upper() == 'BATCH':
        res = ds_prop.CollectionType.BATCH
    elif str_collection_type.upper() == 'IO':
        res = ds_prop.CollectionType.IO
    elif str_collection_type.upper() == 'STREAM':
        res = ds_prop.CollectionType.STREAM
    else:
        res = ds_prop.CollectionType.IO
    return res


def str_to_dataset_type(str_dataset_type: str) -> io_prop.DatasetType:
    if str_dataset_type.upper() == 'SINGLE':
        res = io_prop.DatasetType.SINGLE
    elif str_dataset_type.upper() == 'MULTI':
        res = io_prop.DatasetType.MULTI
    else:
        res = io_prop.DatasetType.SINGLE
    return res


'''
message BatchResponseFromSinker
{
  MessageHeader header = 1;
  DataSourceProperty data_source = 2;
  repeated NestedIo nested_io = 3;
  ResponseResult result = 4;
}
'''


class EncodeBatchResponseFromSinker:
    def __init__(self, caller):
        self._now = get_current_unixtime()
        self._response = res_batch.BatchResponseFromSinker()
        self._response.header.timestamp = self._now
        self._response.header.caller_name = caller

    def build_data_source_from_dict(self, data_source_property: dict):
        data_source = ds_prop.DataSourceProperty()
        data_source.data_source_id = check_field(data_source_property, 'data_source_id')
        data_source.node_id = check_field(data_source_property, 'node_id')
        data_source.sinker_name = check_field(data_source_property, 'sinker_name')
        data_source.source_type = check_field(data_source_property, 'source_type')
        data_source.collection_type = check_field(data_source_property, 'collection_type')
        return data_source

    def set_data_source(self, data_source_property: ds_prop.DataSourceProperty):
        self._response.set_data_source.CopyFrom(data_source_property)

    def build_io_property_from_dict(self, io_property: dict):
        prop = io_prop.IoProperty()
        prop.edge_id = check_field(io_property, 'edge_id')
        prop.data_source_id = check_field(io_property, 'data_source_id')
        prop.io_name = check_field(io_property, 'io_name')
        prop.sinker_name = check_field(io_property, 'sinker_name')
        prop.dataset_type = check_field(io_property, 'dataset_type')
        prop.io_type = check_field(io_property, 'io_type')
        prop.data_type = check_field(io_property, 'data_type')
        prop.IoIds.id1 = check_field(io_property, 'id1')
        prop.IoIds.id2 = check_field(io_property, 'id2')
        prop.IoIds.id3 = check_field(io_property, 'id3')
        prop.IoIds.id4 = check_field(io_property, 'id4')
        prop.recoding = check_field(io_property, 'recoding')
        return prop

    def _cast_types_for_list(self, data_type, set_data):
        try:
            cast_dict = {
                io_prop.DataType.SINT32: np.int32,
                io_prop.DataType.SINT64: np.int64,
                io_prop.DataType.UINT32: np.uint32,
                io_prop.DataType.UINT64: np.uint64,
                io_prop.DataType.FLOAT: np.float32,
                io_prop.DataType.DOUBLE: np.float64
            }
            is_array = True if isinstance(set_data, np.ndarray) else False
            is_number = True if data_type in cast_dict else False
            set_data_list = []
            if is_number:
                if not is_array:
                    set_data = np.array(set_data)
                set_data_list = set_data.astype(cast_dict[data_type]).tolist()
            else:
                if is_array:
                    set_data = set_data.tolist()

                if data_type == io_prop.DataType.STRING:
                    set_data_list = [str(raw) for raw in set_data]
                elif data_type == io_prop.DataType.BYTES:
                    set_data_list = [bytes(raw) for raw in set_data]
                elif data_type == io_prop.DataType.BOOL:
                    set_data_list = [bool(raw) for raw in set_data]
            return set_data_list
        except Exception as e:
            print(str(e))
            raise SystemError('An Occurred exception while _cast_types_for_list')

    def make_multi_io_value_array(self, io_property, data_type, set_data):
        set_data_list = self._cast_types_for_list(data_type, set_data)
        if data_type == io_prop.DataType.SINT32:
            io_property.sint32_array.extend(set_data_list)
        elif data_type == io_prop.DataType.SINT64:
            io_property.sint64_array.extend(set_data_list)
        elif data_type == io_prop.DataType.UINT32:
            io_property.uint32_array.extend(set_data_list)
        elif data_type == io_prop.DataType.UINT64:
            io_property.uint64_array.extend(set_data_list)
        elif data_type == io_prop.DataType.FLOAT:
            io_property.float_array.extend(set_data_list)
        elif data_type == io_prop.DataType.DOUBLE:
            io_property.double_array.extend(set_data_list)
        elif data_type == io_prop.DataType.STRING:
            io_property.string_array.extend(set_data_list)
        elif data_type == io_prop.DataType.BYTES:
            io_property.bytes_array.extend(set_data_list)
        elif data_type == io_prop.DataType.BOOL:
            io_property.bool_array.extend(set_data_list)
        else:
            raise ValueError('Not Support data type')

    def build_nested_io_from_dict(self, io_property: dict, io_value: any, timestamp):
        try:
            nested_io = res_batch.NestedIo()
            nested_io.io_property.CopyFrom(self.build_io_property_from_dict(io_property))
            nested_io.get_value.CopyFrom(self.build_io_property_from_dict(io_property))
            res_dataset = res_io.ResponseDataset()
            if isinstance(io_value, list):
                res_dataset.multi_io_value.ts_array.extend(timestamp)
                self.make_multi_io_value_array(res_dataset.multi_io_value, nested_io.io_property.data_type, io_value)
            else:
                res_dataset.single_io_value.timestamp = self._now if timestamp is not None else timestamp
                res_dataset.single_io_value.io_value = make_pb_io_value(io_value, nested_io.io_property.data_type)
            return nested_io
        except Exception as e:
            print(str(e))
            raise SystemError('An Occurred exception while build_nested_io_from_dict')

    def set_nested_ios(self, nested_ios: [res_batch.NestedIo]):
        self._response.nested_io.extend(nested_ios)

    def response_result(self, status_code, status_message):
        self._response.result.status_code = status_code
        self._response.result.status_message = status_message
    #
    #     for io in response.nested_io:
    #         io.io_property.dataset_type = io_prop.DatasetType.MULTI
    #         io.get_value.multi_io_value.ts_array.extend(ts_list)
    #         ch = io.io_property.ids.id1
    #         self.make_multi_io_value_array(io.get_value.multi_io_value, io.io_property.data_type,
    #                                        io_data_array[ch])
    #     res_result = DeviceResponse(status_code=DeviceStatusCode.DEVICE_COMM_SUCCESS)
    #     return response
    #
    # except Exception as e:
    # self._log.critical(f'An exception occurred while make send pb payload : {str(e)}')
    # response.result.CopyFrom(DeviceResponse(status_code=DeviceStatusCode.SYSTEM_ERROR).get_result())
    # return response
