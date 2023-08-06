# Changelog
All notable changes to this project will be documented in this file.

See [python-semantic-release](https://github.com/relekang/python-semantic-release) for commit
guidelines and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--next-version-placeholder-->

## v0.8.4 (2022-06-06)
### Fix
* Adds flags to lists to supress warnings on python-gitlab api lists(#31) ([`22e246a`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/22e246a09738dc6e9fdec34e55faa6e1cdbe6b53))
* Updates call to the API on issues statistics ([#33](https://gitlab.com/felipe_public/badges-gitlab/-/issues/33)) ([`6289f12`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/6289f12f4127c5c378d5fa497fbb0e174222118c))
* Updates dependencies, fixing python-gitlab ([#31](https://gitlab.com/felipe_public/badges-gitlab/-/issues/31)) ([`804d5ba`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/804d5bae72dfc0fbc9a296619661cfe7a5e6aed7))

## v0.8.3 (2021-10-16)
### Fix
* Change definition of color for test result badges ([#29](https://gitlab.com/felipe_public/badges-gitlab/-/issues/29)) ([`0845f4c`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/0845f4cf012bf050e17b771bd7bf527c28991e06))
* Minor typo in badges test complete svg ([#30](https://gitlab.com/felipe_public/badges-gitlab/-/issues/30)) ([`82e567b`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/82e567b8385e31bc40d1f7d9e83977553191a219))
* Includes back the xmltodict ([#28](https://gitlab.com/felipe_public/badges-gitlab/-/issues/28)) ([`57aa4bb`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/57aa4bb904c1c34d96c8f5719c45afa223b045aa))

## v0.8.2 (2021-10-11)
### Fix
* Bug with parsing xml without testsuites ([#26](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/26)) ([`f4b621c`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/f4b621ce1365326383601c536c34adbadaa8a4c3))

## v0.8.1 (2021-09-12)
### Fix
* Bug with parsing xml with one testsuite only ([#25](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/25)) ([`6be7060`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/6be7060fe1e5eb33e6d2ffadb7169160159e8264))
* Adds incrementing func for stats tests dict ([#25](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/25)) ([`41417d1`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/41417d1d327d0e511f07ff1ff84760aeb5fc9db9))

### Documentation
* Update docs to include asdoi projects (#24). ([`7ffe89a`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/7ffe89a46f76a7ce1515f705b3bd656d3872ff36))

## v0.8.0 (2021-05-26)
### Feature
* Include documentation using sphinx ([`6eb6b3f`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/6eb6b3f8512e1e0ee4a97eeb283f401f49c9fcc8))

## v0.7.0 (2021-05-23)
### Feature
* Adds support for downloading shields.io badges ([#13](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/13)) ([`1a2a606`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/1a2a606c25d3cc62315a41863a169bc6e9d712e1))
* **deps:** Adds requests as dependencu ([#13](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/13)) ([`eb410ed`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/eb410ed1ffc1a5e5a9aa47aa4ad7c7447cbdbee8))

### Documentation
* Update documentation to feature #13 ([`52d6879`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/52d6879ac81121a6e03ae2c54d4f02b482f5b92d))

## v0.6.0 (2021-05-20)
### Feature
* Creates the option for printing static badges from lists ([#14](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/14)) ([`1a3491b`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/1a3491b1a57bc0f731df71a2d8d4f4761cebceb2))

### Documentation
* Readme updated with static badges feature ([#14](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/14)) ([`3876ba3`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/3876ba35b07e8065452e560fbefb3beea8d4f549))

## v0.5.1 (2021-05-19)
### Fix
* Naming of the junit_xml key in the pyproject.toml ([#21](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/21)) ([`004c255`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/004c255864aef4d53bda42ea362c6d23047302f3))

### Documentation
* Update setup.py ([`2513d97`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/2513d970f9b055675de2f5479856604a7774f430))

## v0.5.0 (2021-05-19)
### Feature
* Includes support for configuring in pyproject.toml ([#20](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/20)) ([`132f160`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/132f1608dfb8dbfbe0c4ca59c7b0341f47c91a64))
* **deps:** Includes toml as dependency ([#20](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/20)) ([`a6101dc`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/a6101dc11ebceed0236828031072f12ebe8ccee7))

### Documentation
* Update readme with information about pyproject.toml ([#20](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/20)) ([`c8d1785`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/c8d17852bacc703755387b0f52ef5221cada19d1))

## v0.4.0 (2021-05-17)
### Feature
* Includes the option to generate badges for tests results ([#2](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/2)) ([`2ca6d26`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/2ca6d26348a8a08ff8ddb54155ea06572b721d66))

## v0.3.0 (2021-05-15)
### Feature
* Includes command line option for printing version ([#11](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/11)) ([`54606f5`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/54606f5c6672f29cdf94dfd13f8ecb3166bdf80a))

### Fix
* Changes the badges' labels to lower case ([#6](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/6)) ([`1b2e1a2`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/1b2e1a28a39514854453092b5971041781b1aa85))

### Documentation
* Project documentation is updated in readme ([`2a5df92`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/2a5df92a6df768d2097f197219fe124c7fdb350b))

## v0.2.0 (2021-05-13)
### Feature
* Implementes semantic versioning in the package ([#15](https://gitlab.com/felipe_public/badges-gitlab/-/merge_requests/15)) ([`7e9169a`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/7e9169ab975d55d83868316d209760a062b72bda))
* **deps:** Includes dependencies ([`268af3b`](https://gitlab.com/felipe_public/badges-gitlab/-/commit/268af3b5e8cff829a35d3de99dc8e87054488309))