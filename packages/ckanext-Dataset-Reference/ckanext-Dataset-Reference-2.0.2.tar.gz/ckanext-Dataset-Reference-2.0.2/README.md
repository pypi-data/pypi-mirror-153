# ckanext-Dataset-Reference

This CKAN extension ables CKAN users to link references to their dataset. A reference can be a publication or another dataset. The extension embeds the added references to the target dataset view as a table of citations.  

There are three ways to add a reference:
- With the DOI number or link (look at http://dx.doi.org/)
- With pasting the BibTex (http://www.bibtex.org/) citation metadata (Not implemented yet)
- Manually adding the target reference metadata. (Not implemented yet)



## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.9 | Yes    |
| earlier | No |           |



## Installation

To install ckanext-Dataset-Reference:

1. Activate your CKAN virtual environment, for example:

       > source /usr/lib/ckan/default/bin/activate
       > pip install ckanext-Dataset-Reference

OR, Clone the source and install it on the virtualenv (Suggested location: /usr/lib/ckan/default/src)
:

        git clone https://github.com/TIBHannover/ckanext-Dataset-Reference.git
        cd ckanext-Dataset-Reference
        pip install -e .
        pip install -r requirements.txt

2. Add `dataset_reference` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

3. Upgrade the CKAN database to add the plugin table:

        ckan -c /etc/ckan/default/ckan.ini db upgrade -p dataset_reference


4. Restart CKAN and supervisor. For example if you've deployed CKAN with nginx on Ubuntu:

        sudo service nginx reload
        sudo service supervisor reload




## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini  --disable-pytest-warnings  ckanext/dataset_reference/tests/


