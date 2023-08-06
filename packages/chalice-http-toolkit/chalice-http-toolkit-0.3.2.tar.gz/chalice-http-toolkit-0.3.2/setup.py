import setuptools
import os

def get_dir_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #append the file name to the list
            filelist.append(os.path.join(root,file))
    return filelist

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

tool_assets = get_dir_files("tools/assets/")

setuptools.setup(
    name="chalice-http-toolkit",
    author="Chris Lapa",
    author_email="",
    description="Several helpers for building serverless websites using Chalice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_scm_version={'write_to': 'chalice_http_toolkit/version.py', 'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    url="https://gitlab.com/chalice-http-toolkit/chalice-http-toolkit",
    project_urls={
        "Bug Tracker": "https://gitlab.com/chalice-http-toolkit/chalice-http-toolkit/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages() + ["tools"],
    data_files=[("tools/assets", tool_assets)],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=['chalice>=1.22.3',
                      'python-magic==0.4.22',
                      'requests-toolbelt==0.9.1',
                      'pytz==2021.1'],
    extras_require={
        'layered': ['Jinja2==2.10',
                    'Pillow==8.2.0']
        },
    entry_points={
        'console_scripts': ['chalice-http-toolkit=tools.chalice_http_toolkit:main'],
        }
    )