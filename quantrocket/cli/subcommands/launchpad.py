# Copyright 2017 QuantRocket - All Rights Reserved
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

def add_subparser(subparsers):
    _parser = subparsers.add_parser("launchpad", description="QuantRocket IB Launchpad CLI", help="quantrocket launchpad -h")
    _subparsers = _parser.add_subparsers()

    parser = _subparsers.add_parser("start", help="start the IB gateway")
    parser.add_argument("service", metavar="SERVICE_NAME", help="The name of the IB Gateway service, e.g. ibg1")
    parser.set_defaults(func=None)