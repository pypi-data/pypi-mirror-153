# File: /gtklara/state.py
# Project: gtklara
# File Created: 06-06-2022 10:35:50
# Author: Clay Risser
# -----
# Last Modified: 06-06-2022 14:51:28
# Modified By: Clay Risser
# -----
# Risser Labs LLC (c) Copyright 2022
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


class State:
    def __init__(self, value=None, bindings=[]):
        self._value = value
        self._bindings = {}
        for binding in bindings:
            self.bind(binding)

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        self.sync()

    def sync(self):
        for key, binding in self._bindings.items():
            binding(self._value)

    def bind(self, binding):
        key = str(id(binding))
        self._bindings[key] = binding
        self.sync()

        def unbind():
            if key in self._bindings:
                del self._bindings[key]
                self.sync()

        return unbind
