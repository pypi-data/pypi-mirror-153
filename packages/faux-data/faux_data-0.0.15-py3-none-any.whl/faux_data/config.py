#    Copyright 2022 @jack-tee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
Module for environment level config.
"""

import os

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "weigh-in-service")
DEPLOYMENT_MODE = os.environ.get("FAUX_DATA_DEPLOYMENT_MODE",
                                 "local")  # or cloud_function

TEMPLATE_BUCKET = os.environ.get("FAUX_DATA_TEMPLATE_BUCKET", "")
TEMPLATE_LOCATION = os.environ.get("FAUX_DATA_TEMPLATE_LOCATION", "")
