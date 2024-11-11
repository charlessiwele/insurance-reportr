# Application Deployment Option 1 (With Docker)
1.  Navigate to "reportr" project folder (where Dockerfile is located)
2.  From the "reportr" project folder, run the following:
- if it is the first time youre building and running this project you can run the following command
<code>docker build -t reportr-app . && docker run --name insurance-app-1 -p 8000:8000 reportr-app</code>
- if you have already/previously built and run the poject then you cann remove the current deployment instance a nd re-build and run following command:
<code>docker build -t reportr-app . &&  docker rm insurance-app-1 && docker run --name insurance-app-1 -p 8000:8000 reportr-app</code>

# Application Deployment Option 2 (Without Docker)
1.  Install python on the machine you will be running the project on
2.  Navigate to "reportr" project folder (where Dockerfile is located)
3.  Generate and activate virtual env 
4.  With virtual env activated, run <code> pip install requirements" </code>
5.  From the "reportr" project folder (where manage.py file is located), run <code> python manage.py makemigrations </code> to generate necessary migrations 
6.  From the "reportr" project folder (where manage.py file is located), run <code> python manage.py migrate </code> to generate necessary tables/models from above-generated migrations 
7.  From the "reportr" project folder (where manage.py file is located), run <code> python manage.py populateconfigdata </code> to run the management command that will generate default statuses and types required for the project to function correctly 
8.  From the "reportr" project folder (where manage.py file is located), run <code> python manage.py generatedefaultsuperuser </code> to generate a default user (admin) and password (admin)  
9.  From the "reportr" project folder (where manage.py file is located), run <code> python manage.py collectstatic </code> to copy static files to the static folder
10. From the "reportr" project folder (where manage.py file is located), run <code> python manage.py runserver </code> to start the test/local server

# GENERAL USAGE INSTRUCTIONS
1. After the setup instructions above, confirm that you have the server up running. To do this, open your browser and navigate to http://127.0.0.1:8000. You should be presented with the login
2. You can log in using the user and password generated in "generatesuperuser"
3. Once logged in, navigate to PaymentDocument model
4. Add new model instance/record and attach the test file to the file field
5. Select option to "Save and continue editing"
6. After "Save and continue editing" resolves, in the top right hand corner, you will see 2 options: 
  - "Sync Document Payments" this will populate the Payments table/model
  - "Sync Document Agents" this will populate the Agents table/model
7. Select "Sync Document Payments" link to extract all the payments from the test file and adding them to the database
8. Select "Sync Document Agents" link to extract all the agents from the test file and adding them to the database
9. Navigate to the "Payment" model to see all the new records added
10. Navigate to the "Agent" model to see all the new records added
11. Navigate to "Report" model
- Select to add new Report instance. note: Report name will already be populated
- Select the previously added PaymentDocument instance in the payments_document field
- Select a report_type option from the drop-down "report_type" field
- Save and continue editing
- In the top right hand corner, select the "Generate Reports" button. 
  -- This will generate reports based on the "report_type" option selected
- Refresh current "Report" page
- Reports will be generated and listed below the standard Report fields.
- Select the file link on any of the generated files to download and view the file contents
