# python1
Tests usage of reticulate package with python packages numpy, pandas, matplotlib, and yfinance.

## Running the Application Locally

The four files .Rprofile, python_functions.py, server.R, and ui.R should all be placed in the R project directory.  Running locally, however, requires that the project directory also contains a .venv directory. This is referenced at the end of .Rprofile and is a virtual Python environment. The next section contains the instructions for creating it.

### Creating the .venv Directory

1. Go to https://docs.conda.io/en/latest/miniconda.html
2. Under Windows Installers, click on '(Python 3.8) Miniconda3 Windows 64-bit'. The exact version of Python is likely not critical but Python 3.8 is currently used on shinyapps.io.
3. If necessary, click Download and/or Keep to download the file to the Downloads directory.
4. Click on the downloaded file and install using the defaults. This should involve the following inputs: Next|I Agree|Just Me (recommended)|C:\\Users\\USER1\\miniconda3. The USER1 in this should be the user's name. The user can choose to install the Python directory elsewhere and use that directory in the following instructions.
5. Click Next and Install. Use the defaults and don't select 'Add Miniconda3 to PATH environment variable' or 'Register Miniconda3 as my default Python 3.8)'. Then, click Next and Finish.
6. Enter cmd to open a command window and enter the following commands:
    a. **where python** - verify the location of current python executable.
    b. **where pip** - verify the location of current of current pip executable (there may be none).
    c. **cd miniconda3** - cd to the Python installation.
    d. **Scripts\\activate** - activate miniconda3 as the current Python environment.
    e. **where python** - verify the location of current python executable.
    f. **where pip** - verify the location of current of current pip executable.
    g. **pip install virtualenv** - install the package for creating virtual Python environments.
7. Create a new R project in Rstudio if it does not already exist.
8. In the command window, cd to the home directory of the new R project and enter the following commands:
    h. **virtualenv .venv** - creates the initial .venv directory.
    i. **.venv\\Scripts\\activate**- activate .venv as the current Python environment.
    j. **where python** - verify the location of current python executable.
    k. **where pip** - verify the location of current of current pip executable.
    l. **pip install numpy pandas matplotlib yfinance** - installs required Python packages.
9. In Rstudio, click Session|Restart R, open the server.R file, and click Run App. The output will likely contain the error: *urllib3.exceptions.SSLError: Can't connect to HTTPS URL because the SSL module is not available.*
10. Copy libcrypto-1_1-x64.dll, libcrypto-1_1-x64.pdb, libssl-1_1-x64.dll, and libssl-1_1-x64.pdb
 from the miniconda3\\Library\\bin directory to the .venv\\Scripts directory
11. In RStudio, click Session[Restart R], open the server.R file, and click Run App. The output will likely contain the the error: *Error in py_call_impl: TclError: Can't find a usable init.tcl in the following directories:*
12. Copy the tcl subdirectory of the miniconda3 directory to the .venv directory.
13. In Rstudio, click Session Session[Restart R], open the server.R file, and click Run App. This should successfully run the application.
14. At present, it seems to be necessary to click Session Session[Restart R] before every run of the app in the local environment.

## Running the Application on shinyapps.io

Only the four files .Rprofile, python_functions.py, server.R, and ui.R need to be uploaded to shinyapps.io. The .venv file should not be uploaded. Shinyapps.io will create its own virtual Python environment.
