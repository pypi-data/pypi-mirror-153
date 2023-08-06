# CHANGELOG

## 2.2.1 - 2022-5-27

* Stop mock generation from saving `auth` kwarg.

## 2.2.0 - 2022-5-10

* add `allow_missing_outputs` as a config.
* fix self.kwargs leaking from one test to the next.

## 2.1.2 - 2022-4-20

* Add missing requirement python-dateutil.

## 2.1.1 - 2022-4-13

* Handle BytesIO in request comparison.

## 2.1.0 - 2022-4-12

* added validate_headers and validate_json configs.  
* handle url as a kwarg or arg. 

## 1.0.6 - 2022-03-28

* fixed issue with kwargs from BasicRestEndpoint persisting through multiple tests

## 1.0.0 - 2022-02-04
* Added --mock option to mock requests for the tests.
* restructured the code so that it can be imported into plugins more easily.

## 0.1.0 - 2022-01-27
* First release.


