File-to-URL converter (aka [slicer-dicer](https://www.amazon.com/dp/B0764HM9BM))
================================================================================

Why?
----
It's often necessary to get rid of bulky files by handing them over
to someone else, who enjoys piling up stuff in the basement indefinitely.
Generally, URLs can be stored in VCS and/or databases more easily than binary files.

Shut up and take my money! What exactly this service can do?
------------------------------------------------------------

This service, when deployed to a reliable hosting facility, can:

* Accept HTTP POST requests with binary file attachments
  sent by Ajax, [curl](https://curl.haxx.se/)
  or [wget](https://www.gnu.org/software/wget/);
* After a successful upload, communicate the file URL to your application
  via a callback HTTP POST request;
* Handle thousands of simultaneous requests and store millions of files without
  causing performance issues.

Pre-requisites
--------------

* A [git](https://git-scm.com/) client of your choice;
* [Python 3.7+](https://www.python.org/downloads/) with `virualenv` and `pip` commands.

Installation
------------

* Clone the repository:

  ```
  git clone git@github.com:deathtracktor/slicer-dicer.git
  ```

* Create a local Python environment:

  ```
  virtualenv .venv
  source .venv/bin/activate
  # for Windows, use .venv\Scripts\activate
  ```

* Install dependencies:

  ```
  pip install -r requirements.txt
  ```

* Start the app:

  ```
  python app.py
  ```

* Upload something (from a different terminal session):

  ```
  curl -F file=@image.jpg http://127.0.0.1:8080/upload -F callback_url=https://mysite.xyz?file=image.jpg
  ```

Environment variables
---------------------

* `BASE_URL` - base URL for the uploaded files (example: https://mysite.xyz/images)
* `DATA_PATH` - path to the root uploads directory (default: `data`)

Licensing
---------

[MIT license](https://opensource.org/licenses/MIT).