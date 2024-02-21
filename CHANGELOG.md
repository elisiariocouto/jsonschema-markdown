## 0.3.1 (2024/02/21)

### Bug Fixes

-  Not all definitions must have a properties element (#7) ([c60d170a](https://github.com/elisiariocouto/jsonschema-markdown/commit/c60d170aeb5e43e3dc9f0b26ad04512bcc938955))


### Documentation

-  Update README.md with new usage message. ([39dc652c](https://github.com/elisiariocouto/jsonschema-markdown/commit/39dc652ca7fcb4f1812a5d735ed979d75a4c68f3))


### Features

- **cli:** Add support for title override with -t/--title option. ([0418a470](https://github.com/elisiariocouto/jsonschema-markdown/commit/0418a4709197c0c407e440f8037667cb48598dc4))


### Miscellaneous Tasks

-  Add black and ruff on GitHub Actions. ([45cbcd23](https://github.com/elisiariocouto/jsonschema-markdown/commit/45cbcd2353036d3d8f34691b4799ea0b2c02d81b))
-  Fix ruff check command. ([90560832](https://github.com/elisiariocouto/jsonschema-markdown/commit/905608329f795b75e7f23ed54fc6e0df01e86b7c))


## 0.3.0 (2024/02/15)

### Bug Fixes

- **ci:** Docker Hub username is not a secret. ([03b353e5](https://github.com/elisiariocouto/jsonschema-markdown/commit/03b353e5a384cd1e02dd1d40379e756bf9f6e921))
-  Remove version and timestamp from footer. ([ec648170](https://github.com/elisiariocouto/jsonschema-markdown/commit/ec6481709bac3a9f451cea86929ec4b88c92f694))
-  Fix oneOf, anyOf and allOf labels in table. ([aad51fdf](https://github.com/elisiariocouto/jsonschema-markdown/commit/aad51fdf39ff8e0fa948ee1628e1914141ee2924))
-  Fix number/integer limits calculation. ([fd3bfd03](https://github.com/elisiariocouto/jsonschema-markdown/commit/fd3bfd03b9cfba12dfa93d17197260282eb126fa))


### Documentation

-  Add docker instructions. ([81db236b](https://github.com/elisiariocouto/jsonschema-markdown/commit/81db236b6692036ad1a7154c0002e65f921896f2))
-  Add links to Docker Hub and GitHub Container Registry. ([7e17ba8d](https://github.com/elisiariocouto/jsonschema-markdown/commit/7e17ba8d97dc53604a2a6a3bc675fb9eb2a36435))
-  Typo in Docker Hub link. ([158b366b](https://github.com/elisiariocouto/jsonschema-markdown/commit/158b366bf4006b6bd29bcc75e15fc2535fe1b800))


### Features

-  Add string length and format. ([a01d4920](https://github.com/elisiariocouto/jsonschema-markdown/commit/a01d4920318c3909245b326117d416daaa52df2e))
-  Add support for examples. ([8b332edc](https://github.com/elisiariocouto/jsonschema-markdown/commit/8b332edcff1973f2cf78dcb3f30b66ccce564730))


### Miscellaneous Tasks

-  Bump versions, bump Python to 3.9. ([3c2c2271](https://github.com/elisiariocouto/jsonschema-markdown/commit/3c2c2271d707293272199173522c87ee1ad46a2c))
-  Update docs on README.md. ([2df2f9df](https://github.com/elisiariocouto/jsonschema-markdown/commit/2df2f9df9b02ac7abec7125078ae0028a7388b3c))


### Testing

-  Add basic test script. ([5b534c5c](https://github.com/elisiariocouto/jsonschema-markdown/commit/5b534c5c863f6b1e264edfe9c613bc2a2e55c6e1))


## 0.2.1 (2023/10/23)

### Bug Fixes

- **Dockerfile:** Use multi-stage builds to decrease image size. ([b8cf5ea9](https://github.com/elisiariocouto/jsonschema-markdown/commit/b8cf5ea910ea0f4fe8ecb47ca06e0d47f626d466))


### Features

-  Add Dockerfile to run CLI. (#4) ([c7d53140](https://github.com/elisiariocouto/jsonschema-markdown/commit/c7d5314020ab377054a91475fbf9063d84653e87))
-  Add support for supplying '-' as a shortcut to read schema from STDIN. ([41805154](https://github.com/elisiariocouto/jsonschema-markdown/commit/4180515496ebb929f5e0d7a90dc5b6dcc4de5f5b))


### Miscellaneous Tasks

-  Update dependencies. ([ef818ff9](https://github.com/elisiariocouto/jsonschema-markdown/commit/ef818ff979b0bc805559a0e8c002b658a773ac91))


### Ci

-  Add docker build and push job. ([7fdb2114](https://github.com/elisiariocouto/jsonschema-markdown/commit/7fdb2114ef2821c81b534695058d45bd69baceb8))


## 0.2.0 (2023/10/21)

### Bug Fixes

-  Add newline if footer is used. ([a84bf23d](https://github.com/elisiariocouto/jsonschema-markdown/commit/a84bf23df326773a335922be41c886ff7f3b4fd0))


### Features

-  Add flags for experimental ref resolver and debug messages. ([3d070935](https://github.com/elisiariocouto/jsonschema-markdown/commit/3d07093561bef99aa53431d1c43f51406a73d515))


### Miscellaneous Tasks

-  Update dependencies. ([afceabeb](https://github.com/elisiariocouto/jsonschema-markdown/commit/afceabeb5cce2f870759a4cc2b350a149f632a6b))


### Refactor

-  Recursive schema parser should be easier to read, do not expand $ref, use ref key instead of title for definition links. ([48fc0d03](https://github.com/elisiariocouto/jsonschema-markdown/commit/48fc0d03471064e20a4bbb998546cd12d942e7be))


## 0.1.8 (2023/08/31)

### Bug Fixes

-  Add newline if footer is used. ([98b9f393](https://github.com/elisiariocouto/jsonschema-markdown/commit/98b9f3936a2ac03397fd50002e4e4057769c5c23))


## 0.1.7 (2023/08/11)

### Bug Fixes

-  Only add Definitions section if JSON schema contains definitions. ([732818dc](https://github.com/elisiariocouto/jsonschema-markdown/commit/732818dc01aaf1c34a4e1b9ed6eaa06b77db3f81))


### Features

-  Add footer with timestamp and jsonschema-markdown version to generated markdown. Add CLI flag to opt-out. ([5af92798](https://github.com/elisiariocouto/jsonschema-markdown/commit/5af927986006f89e2409c65512c4cdd1282e155e))


## 0.1.6 (2023/08/09)

### Bug Fixes

-  Strip beginning and end of markdown of spaces and newlines, leave only one newline at the end. ([d1b55aa3](https://github.com/elisiariocouto/jsonschema-markdown/commit/d1b55aa3b7887e8ba96133eaa2b50fa9812af82e))


## 0.1.5 (2023/08/08)

### Bug Fixes

-  Fix anchor links, GitHub and GitLab render them in lowercase. ([0b134283](https://github.com/elisiariocouto/jsonschema-markdown/commit/0b13428312cc4a806d7d5982d8699ae3f518be2f))


### Miscellaneous Tasks

-  Remove unused files. ([02f2af57](https://github.com/elisiariocouto/jsonschema-markdown/commit/02f2af573c5a2a2ab1021908d0a140decde2f948))
-  Add instructions and contributing guide. ([004eb80a](https://github.com/elisiariocouto/jsonschema-markdown/commit/004eb80af41a21974c45131f94d7b243bfd14615))


## 0.1.4 (2023/08/08)

### Miscellaneous Tasks

-  Add license, repo, classifiers and keywords to pyproject.toml. ([c9c03905](https://github.com/elisiariocouto/jsonschema-markdown/commit/c9c0390599b4a09e1c0e1e30536f0f4d555e5a16))


## 0.1.3 (2023/08/08)

### Features

-  Add support for more array and object types, add support for integers. ([0fa66300](https://github.com/elisiariocouto/jsonschema-markdown/commit/0fa663004904122af4c83213a7c62a49cafe8539))


## 0.1.2 (2023/08/08)

### Bug Fixes

-  Handle instances with no properties. ([41b60285](https://github.com/elisiariocouto/jsonschema-markdown/commit/41b602857c66d954eb79750b5f1b70baccfa1639))


## 0.1.1 (2023/08/08)

### Features

-  Add support for nullables. ([963578b5](https://github.com/elisiariocouto/jsonschema-markdown/commit/963578b5f8353f9ee24da75eee4ea9426bf35a1e))


### Miscellaneous Tasks

-  Publish to PyPI only on tags. ([6be56b09](https://github.com/elisiariocouto/jsonschema-markdown/commit/6be56b092246dbb9d32bbcfafcdfafbf9a6a02c5))


## 0.1.1 (2023/08/08)

### Features

-  Add support for nullables. ([963578b5](https://github.com/elisiariocouto/jsonschema-markdown/commit/963578b5f8353f9ee24da75eee4ea9426bf35a1e))


### Miscellaneous Tasks

-  Publish to PyPI only on tags. ([6be56b09](https://github.com/elisiariocouto/jsonschema-markdown/commit/6be56b092246dbb9d32bbcfafcdfafbf9a6a02c5))
