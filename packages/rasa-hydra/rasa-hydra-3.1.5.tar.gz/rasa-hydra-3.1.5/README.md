# Rasa-Hydra (Forked from Rasa)

Rasa-Hydra is forked from the official Rasa repo and maintained by the Hydra team. Rasa is an open source machine learning framework to automate text-and voice-based conversations. With Rasa-Hydra, you can build chatbots on:
- Facebook Messenger
- Slack
- Microsoft Bot Framework
- Rocket.Chat
- Mattermost
- Telegram
- Twilio
- Your own custom conversational channels

or voice assistants as:
- Alexa Skills
- Google Home Actions

Rasa-Hydra's primary purpose is to help you build contextual, layered
conversations with lots of back-and-forth. To have a real conversation,
you need to have some memory and build on things that were said earlier.
Rasa-Hydra lets you do that in a scalable way.

### Development Internals
### Running the Tests
In order to run the tests, make sure that you have the development requirements installed:
```bash
export PIP_USE_PEP517=false
pip3 install -r requirements-dev.txt
pip3 install -e .
make prepare-tests-ubuntu # Only on Ubuntu and Debian based systems
make prepare-tests-macos  # Only on macOS
```

Then, run the tests:
```bash
make test
```

They can also be run at multiple jobs to save some time:
```bash
make test -j [n]
```

Where `[n]` is the number of jobs desired. If omitted, `[n]` will be automatically chosen by pytest.

### Steps to release a new version
Releasing a new version is quite simple, as the packages are build and distributed by travis.

*Terminology*:
* patch release (third version part increases): 1.1.2 -> 1.1.3
* minor release (second version part increases): 1.1.3 -> 1.2.0
* major release (first version part increases): 1.2.0 -> 2.0.0

*Release steps*:
1. Make sure all dependencies are up to date (**especially Rasa SDK**)
2. Switch to the branch you want to cut the release from (`master` in case of a major / minor, the current feature branch for patch releases) 
3. Run `make release`
4. Create a PR against master or the release branch (e.g. `1.2.x`)
5. Once your PR is merged, tag a new release (this SHOULD always happen on master or release branches), e.g. using
    ```bash
    git tag 1.2.0 -m "next release"
    git push origin 1.2.0 --tags
    ```
    travis will build this tag and push a package to [pypi](https://pypi.python.org/pypi/rasa)
6. **If this is a minor release**, a new release branch should be created pointing to the same commit as the tag to allow for future patch releases, e.g.
    ```bash
    git checkout -b 1.2.x
    git push origin 1.2.x
    ```
6. Packaging the Rasa-Hydra project. For more information, please refer to this [guide](https://packaging.python.org/tutorials/packaging-projects/).
    1. Make sure you have the latest versions of setuptools and wheel installed:
        ```bash
        python3 -m pip install --user --upgrade setuptools wheel
        ```
       
    2. Bump up the version in the dialog_manager/version.py.
       
    3. Build the package locally.
        ```bash
        python3 setup.py sdist bdist_wheel
        ```
7. Upload the package to PyPI/Test PyPI.
    1. Install twine from PyPI.
       ```bash
       pip install twine
       ```

    *  PyPI
        ```bash
        python3 -m twine upload dist/*
        ```
    * Test PyPI
        ```bash
        python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
        ```