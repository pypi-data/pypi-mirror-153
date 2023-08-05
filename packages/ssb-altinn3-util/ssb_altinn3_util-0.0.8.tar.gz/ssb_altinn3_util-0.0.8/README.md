# ssb-altinn3-util
A library of handy modules and utilities that can be used and built on when integrating with Altinn 3 and SSB's Altinn 3 data collection solutions

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-altinn3-util&metric=alert_status&token=1929d7efca8af99dc89ed16e2c68d6c80cc5c1ba)](https://sonarcloud.io/summary/new_code?id=statisticsnorway_ssb-altinn3-util)

## To build package locally during development run (from root directory of project):

python setup.py install

## Testing from other Python apps

- Push the changes to a branch of `ssb-altinn3-util`
- Uninstall previous ssb-altinn3-util in the app: `pip uninstall ssb-altinn3-util`
- Add the following in your requirements.txt in the app `git+ssh://git@github.com/statisticsnorway/ssb-altinn3-util@<your_branch_name>

After the testing is finished, remember to revert the `requirements.txt` before pushing the changes!

## Releasing to PyPi

- Update version in `setup.py`
- Create a GitHub release and the pipeline will push the package to PyPi

## Running tests locally

In order to run the unittests locally things must be set up properly:
- In the project root directory run:

       pip install -e .
       pip install -r ./test/requirements-test.txt 
       
- This will install the package locally as editable (changes in code will immediately be reflected in the package) as well as the required dependencies.
- You should now be able to run the tests by running pytest from project root.
