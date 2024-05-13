# vendor_management
Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance.

## Tech Stack
**Server:** Django, Django Reast Framework

# Features and Functionalities
- 'AbstractUser' is used to customized 'Vendors' user model
- Authentication through Token
- Class based views
- Data serializations
- Business logics manipulation
- Django Unit Test

# Deployment
- Use the command URL to clone the project to your local machine:
```bash
  git clone https://github.com/nuruzz9134/vendor_management.git
```
- Change your directory to the cloned project's directory.
- Setup and activate python virtual environment
- Install Dependencies:
  ```bash
  Python==3.10.6
  Django==4.1.6
  djangorestframework==3.14.0
  ```
  those are minimum requirment to run the project.
  if any other packages installation needed like database management or other dependencies, please do install packages or modules.
- to run the test cases you should run this command (i am using django's unit test, so you does't need to install another package):
```bash
  python manage.py test
```
