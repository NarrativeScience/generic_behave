{ nsnix, buildUtils, nsPythonPackage, nsPythonPackages, pythonPackages, pkgs, }:

nsPythonPackage {
  name = "ns_behave";
  repo = "generic_behave";
  pathInRepo = "test_utils/behave";
  propagatedBuildInputs = with pythonPackages; [
    ansicolor
    behave
    boto3
    click
    coloredlogs
    jsonpath
    nsPythonPackages.ns_selenium
    nsPythonPackages.ns_requests
  ];
}
