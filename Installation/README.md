# NUPIC INSTALLATION ERRORS


## SSL CERTIFICATE ERRORS
If you are getting the following error when trying to use PIP to install packages:

```
Could not fetch URL https://pypi.python.org/simple/"PkgNm"/: There was a problem confirming the ssl certificate: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661) - skipping
Could not find a version that satisfies the requirement "PkgNm" (from versions: )No matching distribution found for "PkgNm"
```

It is due to Montefiore's proxy SSL certificates.
Here are two methods to solve this issue

1. To solve on a package by package basis, just tell pip that the site is trusted

	` pip install --trusted-host pypi.python.org PkgNm `

	Replace PkgNm with the name of the Pkg you want to install.  If the package comes from another site, you will have to change the host site accordingly

2. Solve the issue for all sites, by adding the proxy certificates to pip (Valid as of 5/15/2017)

	In this git directory there is a file, MonteCertificates.pem, this is a text file which contains the SSH certificates for Monte proxies. You have to append this file to the pip certificates file, cacert.pem, which is most probably located in `%PYTHON HOME DIR%\Lib\site-packages\certifi\`. To append the new certificates, simply open both files with a text editor and copy the text from the MonteCertificates file to the bottom of the cacert file

### Caveat 1

If there is no cacert.pem file in the `\certifi\` directory you can locate it by running

`python %PYTHON HOME DIR%\Lib\site-packages\pip\_vendor\requests\certs.py`

this will output the location of the cacert.pem file

### Caveat 2
If the certificates included in the MonteCertificates.pem do not fix the problem then you need to manually export the SSL certificates.

These instructions apply to chrome but are probably similar for most browsers
* Open a new tab and go to chrome://settings OR open the chrome settings page
* In the advanced settings, under HTTP/SSL click on 'Manage certificates...'
* Go to the tab 'Intermediate Certificate Authorities'
* Export the certificates which start with Montefiore in the 'Issued To' column, using the 'DER encoded binary X.509 (.CER)' option
* Open a cmd window / terminal in the folder to which you exported the cer file
* Use the following code to convert the .cer file to a .pem file (need to have openssl installed), where FlNm is the name of the cer file

	`openssl x509 -inform der -in FlNm.cer -out FlNm.pem`

* Copy the output to the end of the cacert.pem file
* Repeat for all the Montefiore certificates
