# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
import logging
from . import fastdeploy_cpp2py_export as fastdeploy_c

try:
    OrtBackendOption = fastdeploy_c.OrtBackendOption
except:
    def OrtBackendOption():
       raise Exception("[DeployKit] This package didn't compile with onnxruntime backend.")

class OrtBackend:
    """ Initialization for onnxruntime Backend
    Arguments:
        model_file: Path of model file, if the suffix of this file is ".onnx", will be loaded as onnx model; otherwise will be loaded as Paddle model.
        params_file: Path of parameters file, if loaded as onnx model or there's no parameter for Paddle model, set params_file to empty.
        verbose: Wheter to open Paddle2ONNX log while load Paddle model
    """

    def __init__(self, model_file, params_file="", option=None, verbose=False):
        try:
            self.backend = fastdeploy_c.OrtBackend()
        except:
            logging.error(
                "[ERROR] Cannot import OrtBackend from fastdeploy, please make sure you are using library is prebuilt with onnxruntime."
            )
        if option is None:
            option = fastdeploy_c.OrtBackendOption()
        if model_file.strip().endswith(".onnx"):
            self.backend.load_onnx(model_file.strip(), option)
        else:
            self.backend.load_paddle(model_file.strip(),
                                     params_file.strip(), option, verbose)

    def infer(self, inputs):
        input_names = list()
        input_arrays = list()
        for k, v in inputs.items():
            input_names.append(k)
            input_arrays.append(inputs[k])
        return self.backend.infer(input_names, input_arrays)


try:
    TrtBackendOption = fastdeploy_c.TrtBackendOption
except:
    def TrtBackendOption():
       raise Exception("[DeployKit] This package didn't compile with tensorrt backend.")


class TrtBackend:
    """ Initialization for tensorrt Backend
    Arguments:
        model_file: Path of model file, if the suffix of this file is ".onnx", will be loaded as onnx model; otherwise will be loaded as Paddle model.
        params_file: Path of parameters file, if loaded as onnx model or there's no parameter for Paddle model, set params_file to empty.
        verbose: Wheter to open Paddle2ONNX log while load Paddle model
    """

    def __init__(self, model_file, params_file="", option=None, verbose=False):
        try:
            self.backend = fastdeploy_c.TrtBackend()
        except:
            logging.error(
                "[ERROR] Cannot import TrtBackend from deploykit, please make sure you are using library is prebuilt with TensorRT."
            )
        if option is None:
            option = TrtBackendOption()
        if model_file.strip().endswith(".onnx"):
            self.backend.load_onnx(model_file.strip(), option)
        else:
            self.backend.load_paddle(model_file.strip(),
                                     params_file.strip(), option, verbose)

    def infer(self, inputs):
        input_names = list()
        input_arrays = list()
        for k, v in inputs.items():
            input_names.append(k)
            input_arrays.append(inputs[k])
        return self.backend.infer(input_names, input_arrays)
