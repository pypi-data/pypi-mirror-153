#### File with proto types for Pix+ services.

In order to push changes to the `proto_pixplus_pb2.py`, be sure that:

- The `proto_pixplus.proto` file contains the changes, which were compiled **successfully**.
- New .py file is compiled and overwritten `proto_pixplus_pb2.py` module with current

Please, import needed types with an `ptype` alias
```shell
import proto_pixplus_pb2 as ptype
```

#### Deploy new version

To deploy new version, be sure you have the latest version of PyPA’s build installed:
```shell
python3 -m pip install --upgrade build
```


Go to the `/proto_pypi` folder and run next command:
```shell
python3 -m build
```

This command should output a lot of text and once completed should generate two folder in the directory:
**dist** and **proto_pixplus_pb2.egg-info**

To upload new version of the package, also be sure to update the **version** of the package. See the semantics of the versioning at *https://semver.org/*

Install **twine**, to upload all the archives under dist:
```shell
python3 -m pip install --upgrade twine
```

After, you can push new version of the package with `python3 -m twine upload --skip-existing dist/* --verbose`. You will be prompted for *username* and *password*. 

Once uploaded, you can check your new version at *https://pypi.org/manage/project/proto-pixplus-pb2/releases/*

If any issues are met, look at the complete [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
