{ nsnix, buildUtils, nsPythonPackage, nsPythonPackages, pythonPackages, pkgs, }:

nsPythonPackage {
  name = "ns_requests";
  repo = "generic_behave";
  pathInRepo = "test_utils/requests";
  propagatedBuildInputs = with pythonPackages; [];
}
