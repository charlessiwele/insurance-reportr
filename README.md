# SETUP
✅ Navigate to "reportr" project folder (where Dockerfile is located)
✅ From the "reportr" project folder, run the following:
<code>
docker build -t reportr-app . && docker run --name insurance-app-1 -p 8000:8000 reportr-app
</code>

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
















docker build -t reportr-app . && docker run -p 8001:8001 reportr-app



docker build -t vaultx-app . && docker rm vaultx-app-1 && docker run --name vaultx-app-1 -p 8001:8001 vaultx-app